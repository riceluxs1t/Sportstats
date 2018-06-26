from collections import defaultdict
from numpy.random import poisson
import statsmodels.api as sm
from prediction.prediction_output import ConcretePredictionOutput
from prediction.utils import get_current_elo, filter_matches


class IndependentPoissonModel(object):

    OPTIMIZATION_METHOD = 'newton'
    NUM_ITERS = 10000

    """Models goals to be scored as two independent Poisson R.Vs. """
    def predict(self, home_team, away_team):

        home_team_elo = get_current_elo(home_team)
        away_team_elo = get_current_elo(away_team)

        uA_B = self.fit_poisson(
            filter_matches(home_team),
            home_team,
            True
        ).predict([away_team_elo, 1])

        uB_A = self.fit_poisson(
            filter_matches(away_team),
            away_team,
            True
        ).predict([home_team_elo, 1])

        vA_B = self.fit_poisson(
            filter_matches(home_team),
            home_team,
            False
        ).predict([away_team_elo, 1])

        vB_A = self.fit_poisson(
            filter_matches(away_team),
            away_team,
            False
        ).predict([home_team_elo, 1])

        l_A = (uA_B + vB_A) / 2.0
        l_B = (uB_A + vA_B) / 2.0

        score_dict = self.run_simulations(l_A, l_B, self.NUM_ITERS)

        return score_dict

    def fit_poisson(self, matches, team_name, scored):
        elos = []
        num_goals = []

        for match in matches:
            if match.home_team == team_name:
                elos.append(
                    [
                        match.away_team_resulting_rating - match.away_team_rating_change,
                        1
                    ]
                )

                if scored:
                    num_goals.append(match.home_team_score)
                else:
                    num_goals.append(match.away_team_score)
            else:
                elos.append(
                    [
                        match.home_team_resulting_rating - match.home_team_rating_change,
                        1  # a0 term.
                    ]
                )

                if scored:
                    num_goals.append(match.away_team_score)
                else:
                    num_goals.append(match.home_team_score)

        poisson = sm.Poisson(num_goals, elos)
        poisson_fitted = poisson.fit(method=self.OPTIMIZATION_METHOD)

        return poisson_fitted

    def run_simulations(
        self,
        poisson_param_team_A,
        poisson_param_team_B,
        num_iters
    ):

        home_team_score_simulations = poisson(poisson_param_team_A, num_iters)
        away_team_score_simulations = poisson(poisson_param_team_B, num_iters)

        score_dict = defaultdict(int)

        for i in range(num_iters):
            score_dict[
                (
                    home_team_score_simulations[i],
                    away_team_score_simulations[i]
                )
            ] += 1

        for key in score_dict:
            score_dict[key] /= num_iters

        return score_dict


def make_prediction_output(model_outcome):
    return ConcretePredictionOutput(model_outcome)

from collections import defaultdict
from functools import reduce
from numpy.random import poisson as numpy_poisson_distribution
import statsmodels.api as sm
from prediction.prediction_output import ConcretePredictionOutput
from prediction.utils import get_current_elo, filter_matches


class IndependentPoissonModel(object):
    """Models goals to be scored as two independent Poisson R.Vs. """
    OPTIMIZATION_METHOD = 'newton'
    NUM_ITERS = 10000
    CACHE_FITTED_POISSON_MODELS = {}

    def predict(self, home_team, away_team):
        """Given a pair of teams, returns a dictionary of each possible scenarios as keys
        and their likelihoods as values. """
        home_team_poisson_param, away_team_poisson_param = (
            self.estimate_poisson_param(home_team, away_team)
        )

        score_dict = self.run_simulations(
            home_team_poisson_param,
            away_team_poisson_param,
            self.NUM_ITERS
        )

        return score_dict

    def estimate_poisson_param(self, home_team, away_team):
        """For a given pair of teams, estimate their poisson parameters as
        explained in the reference paper. Basically, code first estimates
        the four separate independent poisson parameters that measure
        the two teams' offensive and defensive strengths and use them to output the
        actual poisson parameters. """
        def compute_or_lookup_offensive_defensive_poisson_models(team_name):
            """Computes the fitted poisson distributions that represent the given
            team's offensive and defensive strengths or looks up their cached values. """
            cached_models = self.CACHE_FITTED_POISSON_MODELS.get(team_name)
            if cached_models is None:
                matches = filter_matches(team_name)
                poisson_goals_scored = self.fit_poisson_using_goals(
                    matches,
                    team_name,
                    True
                )

                poisson_goals_taken = self.fit_poisson_using_goals(
                    matches,
                    team_name,
                    False
                )

                self.CACHE_FITTED_POISSON_MODELS[team_name] = (
                    poisson_goals_scored,
                    poisson_goals_taken
                )

                cached_models = (
                    poisson_goals_scored,
                    poisson_goals_taken
                )
            return cached_models

        home_team = home_team.lower()
        away_team = away_team.lower()

        home_team_elo = get_current_elo(home_team)
        away_team_elo = get_current_elo(away_team)

        home_poisson_goals_scored, home_poisson_goals_taken = (
            compute_or_lookup_offensive_defensive_poisson_models(home_team)
        )

        away_poisson_goals_scored, away_poisson_goals_taken = (
            compute_or_lookup_offensive_defensive_poisson_models(away_team)
        )

        # compute home_team and away team's offensive and defensive strengths.
        home_team_offensive_strength = home_poisson_goals_scored.predict([away_team_elo, 1])
        home_team_defensive_strength = home_poisson_goals_taken.predict([away_team_elo, 1])

        away_team_offensive_strength = away_poisson_goals_scored.predict([home_team_elo, 1])
        away_team_defensive_strength = away_poisson_goals_taken.predict([home_team_elo, 1])

        # compute the final poisson parameters.
        home_team_poisson_param = (
          home_team_offensive_strength + away_team_defensive_strength
        ) / 2.0

        away_team_poisson_param = (
            home_team_defensive_strength + away_team_offensive_strength
        ) / 2.0

        return home_team_poisson_param, away_team_poisson_param

    def fit_poisson_using_goals(self, matches, team_name, scored):
        """fits and returns a poisson distribution using goals scored or
        allowed depending on 'scored' param. Uses the statsmodel library."""

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
        poisson_param_home_team,
        poisson_param_away_team,
        num_iters
    ):

        def reduce_func(current_dict, pair):
            home_team_score, away_team_score = pair
            current_dict[(home_team_score, away_team_score)] += 1
            return current_dict

        home_team_score_simulations = numpy_poisson_distribution(poisson_param_home_team, num_iters)
        away_team_score_simulations = numpy_poisson_distribution(poisson_param_away_team, num_iters)

        score_dict = reduce(
            reduce_func,
            zip(home_team_score_simulations, away_team_score_simulations),
            defaultdict(int)
        )

        for key in score_dict:
            score_dict[key] /= num_iters

        return score_dict


def make_prediction_output(model_outcome):
    """A constructor for a PredictionOutput of the Independent Poisson model. """
    return ConcretePredictionOutput(model_outcome)

from collections import defaultdict
from functools import reduce
from numpy.random import poisson as numpy_poisson_distribution
import statsmodels.api as sm
from prediction.prediction_output import ConcretePredictionOutput
from prediction.utils import get_current_elo, filter_matches


class IndependentPoissonModel(object):

    OPTIMIZATION_METHOD = 'newton'
    NUM_ITERS = 10000
    COUNTRY_FIT_POISSON_CACHE = {}

    """Models goals to be scored as two independent Poisson R.Vs. """
    def predict(self, home_team, away_team):

        l_A,l_B = self.getExpectation(home_team,away_team)

        score_dict = self.run_simulations(l_A, l_B, self.NUM_ITERS)

        return score_dict


    def getExpectation(self,home_team,away_team):
        """ Optimized number of DB access for fitting poisson model by
        performing only once per team"""
        home_team = home_team.lower()
        away_team = away_team.lower()

        home_team_elo = get_current_elo(home_team)
        away_team_elo = get_current_elo(away_team)
        
        # Use Cached data if already caculated
        if home_team not in self.COUNTRY_FIT_POISSON_CACHE:
            home_team_matches = filter_matches(home_team)
            home_fit_poisson_goal_scored = self.fit_poisson_using_goals(
                home_team_matches,
                home_team,
                True
            )
            home_fit_poisson_goal_taken = self.fit_poisson_using_goals(
                home_team_matches,
                home_team,
                False
            )

            # Cache Data home_team
            self.COUNTRY_FIT_POISSON_CACHE[home_team]={}
            self.COUNTRY_FIT_POISSON_CACHE[home_team]["True"] = home_fit_poisson_goal_scored
            self.COUNTRY_FIT_POISSON_CACHE[home_team]["False"] = home_fit_poisson_goal_taken

            uA_B = home_fit_poisson_goal_scored.predict([away_team_elo, 1])
            vA_B = home_fit_poisson_goal_taken.predict([away_team_elo, 1])
        else:
            # Poisson Fit for this home_team is cached
            uA_B = self.COUNTRY_FIT_POISSON_CACHE[home_team]["True"].predict([away_team_elo, 1])
            vA_B = self.COUNTRY_FIT_POISSON_CACHE[home_team]["False"].predict([away_team_elo, 1])
        
        if away_team not in self.COUNTRY_FIT_POISSON_CACHE:
            away_team_matches = filter_matches(away_team)
            away_fit_poisson_goal_scored = self.fit_poisson_using_goals(
                away_team_matches,
                away_team,
                True
            )
            away_fit_poisson_goal_taken = self.fit_poisson_using_goals(
                away_team_matches,
                away_team,
                False
            )
            # Cache Data away_team
            self.COUNTRY_FIT_POISSON_CACHE[away_team]={}
            self.COUNTRY_FIT_POISSON_CACHE[away_team]["True"] = away_fit_poisson_goal_scored
            self.COUNTRY_FIT_POISSON_CACHE[away_team]["False"] = away_fit_poisson_goal_taken

            uB_A = away_fit_poisson_goal_scored.predict([home_team_elo, 1])
            vB_A = away_fit_poisson_goal_taken.predict([home_team_elo, 1])
        else:
            # Poisson Fit for this away_team is cached
            uB_A = self.COUNTRY_FIT_POISSON_CACHE[away_team]["True"].predict([home_team_elo, 1])
            vB_A = self.COUNTRY_FIT_POISSON_CACHE[away_team]["False"].predict([home_team_elo, 1])

        l_A = (uA_B + vB_A) / 2.0
        l_B = (uB_A + vA_B) / 2.0
        return [l_A,l_B]    

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
        # print("home_team_score_simulation :",home_team_score_simulations)
        # print("away_team_score_simulations:",away_team_score_simulations)
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

"""
Sample result :
iteration 10:
1)
    {'spain': 0.5, 
    'brazil': 0.4, 
    'denmark': 0.1}
2)
    {'colombia': 0.1,
    'belgium': 0.1,
    'switzerland': 0.1,
    'france': 0.3,
    'portugal': 0.1,
    'spain': 0.3})
    
iteration 100:
    {'brazil': 0.23,
    'belgium': 0.16,
    'argentina': 0.12,
    'spain': 0.14,
    'denmark': 0.01,
    'croatia': 0.04,
    'uruguay': 0.03,
    'portugal': 0.08,
    'colombia': 0.04,
    'sweden': 0.02,
    'switzerland': 0.04,
    'mexico': 0.04,
    'france': 0.04,
    'england': 0.01})
iteration 1000:
defaultdict(int,
            {'argentina': 0.112,
             'portugal': 0.074,
             'brazil': 0.217,
             'switzerland': 0.049,
             'croatia': 0.037,
             'russia': 0.013,
             'spain': 0.183,
             'belgium': 0.066,
             'colombia': 0.091,
             'uruguay': 0.025,
             'denmark': 0.025,
             'france': 0.036,
             'mexico': 0.026,
             'sweden': 0.027,
             'england': 0.018,
             'japan': 0.001})
iteration 10000
            {'switzerland': 0.0693,
             'brazil': 0.076,
             'uruguay': 0.1076,
             'croatia': 0.0557,
             'russia': 0.0966,
             'colombia': 0.0439,
             'sweden': 0.0573,
             'argentina': 0.0559,
             'france': 0.0815,
             'belgium': 0.1315,
             'spain': 0.0201,
             'mexico': 0.0313,
             'denmark': 0.0527,
             'portugal': 0.0545,
             'england': 0.0496,
             'japan': 0.0165})

"""
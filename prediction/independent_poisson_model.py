from collections import defaultdict
from functools import reduce
from numpy.random import poisson as numpy_poisson_distribution
from numpy.random import randint
import statsmodels.api as sm
from prediction.prediction_output import ConcretePredictionOutput
from prediction.utils import get_current_elo, filter_matches


class IndependentPoissonModel(object):

    OPTIMIZATION_METHOD = 'newton'
    NUM_ITERS = 10000

    """Models goals to be scored as two independent Poisson R.Vs. """
    def predict(self, home_team, away_team):

        home_team = home_team.lower()
        away_team = away_team.lower()

        home_team_elo = get_current_elo(home_team)
        away_team_elo = get_current_elo(away_team)

        uA_B = self.fit_poisson_using_goals(
            filter_matches(home_team),
            home_team,
            True
        ).predict([away_team_elo, 1])

        uB_A = self.fit_poisson_using_goals(
            filter_matches(away_team),
            away_team,
            True
        ).predict([home_team_elo, 1])

        vA_B = self.fit_poisson_using_goals(
            filter_matches(home_team),
            home_team,
            False
        ).predict([away_team_elo, 1])

        vB_A = self.fit_poisson_using_goals(
            filter_matches(away_team),
            away_team,
            False
        ).predict([home_team_elo, 1])

        l_A = (uA_B + vB_A) / 2.0
        l_B = (uB_A + vA_B) / 2.0
        # print("l_A,l_B:",l_A,l_B)
        score_dict = self.run_simulations(l_A, l_B, self.NUM_ITERS)
        # print("score_dict",score_dict)
        return score_dict


    def getExpectation(self,home_team,away_team):
        home_team = home_team.lower()
        away_team = away_team.lower()

        home_team_elo = get_current_elo(home_team)
        away_team_elo = get_current_elo(away_team)

        uA_B = self.fit_poisson_using_goals(
            filter_matches(home_team),
            home_team,
            True
        ).predict([away_team_elo, 1])

        uB_A = self.fit_poisson_using_goals(
            filter_matches(away_team),
            away_team,
            True
        ).predict([home_team_elo, 1])

        vA_B = self.fit_poisson_using_goals(
            filter_matches(home_team),
            home_team,
            False
        ).predict([away_team_elo, 1])

        vB_A = self.fit_poisson_using_goals(
            filter_matches(away_team),
            away_team,
            False
        ).predict([home_team_elo, 1])

        l_A = (uA_B + vB_A) / 2.0
        l_B = (uB_A + vA_B) / 2.0
        return l_A,l_B


    def sample(self, num_iters):
        """ Sample 
        """
        given_round16 = [
            "uruguay","portugal",
            "france","argentina",   
            "brazil","mexico",
            "belgium","japan",
            "spain","russia",
            "croatia","denmark",
            "sweden","switzerland",
            "colombia","england"]

        winner_dict = defaultdict(int)
        
        for iteration in range(num_iters):
            print("iteration :",iteration)
            predict_final = []
            predict_qf = []
            predict_round8 = []
            for game_num in range(8):
                #Guess winner for each game in round 16
                home_team = given_round16[game_num*2]
                away_team = given_round16[game_num*2+1]
                predict_round8.append(self.getWinner(home_team,away_team))
            for game_num in range(4):
                home_team = predict_round8[game_num*2]
                away_team = predict_round8[game_num*2+1]
                predict_qf.append(self.getWinner(home_team,away_team))
            for game_num in range(2):
                home_team = predict_qf[game_num*2]
                away_team = predict_qf[game_num*2+1]
                predict_final.append(self.getWinner(home_team,away_team))
            home_team,away_team = predict_final
            winner_dict[self.getWinner(home_team,away_team)] += 1

        
        for key in winner_dict:
            winner_dict[key] /= num_iters                
        return winner_dict

    def getWinner(self,home_team,away_team):
        """Use Expectation of Poisson to get a winner of the game"""
        l_A,l_B = self.getExpectation(home_team,away_team)
        home_team_score = numpy_poisson_distribution(l_A,1)
        away_team_score = numpy_poisson_distribution(l_B,1)
        if home_team_score > away_team_score:
            return home_team
        elif home_team_score < away_team_score:
            return away_team
        else:
            #Guess score for overtime game(30 min)
            # TODO : Add factor for Player being tired
            home_team_score += numpy_poisson_distribution(l_A/3,1)
            away_team_score += numpy_poisson_distribution(l_B/3,1)
            if home_team_score > away_team_score:
                return home_team
            elif home_team_score < away_team_score:
                return away_team
            else:
                #penalty shootout : coin flip
                if randint(2):
                    return home_team
                else:
                    return away_team
    


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

"""
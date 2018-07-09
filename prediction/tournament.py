# from prediction import independent_poisson_model 
from prediction.tournament_output import ConcreteTournamentOutput
from collections import defaultdict
from numpy.random import randint
from numpy.random import poisson as numpy_poisson_distribution


class TournamentPredictionModel(object):

    def __init__(self,
        independent_poisson_model,

    ):
        self.independent_poisson_model = independent_poisson_model
        self.NUM_ITERS = 10000
        self.default_given_round16 = [
                "uruguay","portugal",
                "france","argentina",   
                "brazil","mexico",
                "belgium","japan",
                "spain","russia",
                "croatia","denmark",
                "sweden","switzerland",
                "colombia","england"]
        self.predicted_round8 = []
        self.predicted_qf = []
        self.predicted_final = [] 
        self.predicted_winner = []

    def get_num_iters(self):
        return self.NUM_ITERS

    def get_given_round16(self):
        return self.default_given_round16

    def get_tournament_probability(self):
        """ Get tournament probability for round8, qf, final, and winner"""
        if not self.predicted_winner:
            # No cached prediction. Caculated it. Error Proof.
            self.predicted_winner,self.predicted_final,self.predicted_qf,self.predicted_round8 = self.sample_tournament()

        self.convert_sample_to_probability_decimal(self.predicted_winner)
        self.convert_sample_to_probability_decimal(self.predicted_final)
        self.convert_sample_to_probability_decimal(self.predicted_qf)
        self.convert_sample_to_probability_decimal(self.predicted_round8)
        return

    def sample_tournament(self):
        """ Sample tournament for NUM_ITERS """
        model = self.independent_poisson_model
        num_iters = self.get_num_iters()
        given_round16 = self.get_given_round16()
        E_dict = defaultdict(float)
        for i in range(len(given_round16)):
            for j in range(i+1,len(given_round16)):
                team1 = min(given_round16[i],given_round16[j])
                team2 = max(given_round16[i],given_round16[j])
                E_dict[(team1,team2)] = model.getExpectation(team1,team2)                

        winner_dict = defaultdict(float)
        final_dict = defaultdict(float)
        qf_dict = defaultdict(float)
        round8_dict= defaultdict(float)
        
        for iteration in range(num_iters):
            # print("iteration:",iteration)
            predict_final = []
            predict_qf = []
            predict_round8 = []
            for game_num in range(8):
                #Guess winner for each game in round 16
                home_team = given_round16[game_num*2]
                away_team = given_round16[game_num*2+1]
                winner = self.getWinner(home_team,away_team,E_dict)
                predict_round8.append(winner)
                round8_dict[winner] += 1
            for game_num in range(4):
                home_team = predict_round8[game_num*2]
                away_team = predict_round8[game_num*2+1]
                winner = self.getWinner(home_team,away_team,E_dict)
                predict_qf.append(winner)
                qf_dict[winner] += 1
            for game_num in range(2):
                home_team = predict_qf[game_num*2]
                away_team = predict_qf[game_num*2+1]
                winner = self.getWinner(home_team,away_team,E_dict)
                predict_final.append(winner)
                final_dict[winner] +=1
            home_team, away_team = predict_final
            winner_dict[self.getWinner(home_team,away_team,E_dict)] += 1

        # print(sum(winner_dict.values())==num_iters)
        # for key in winner_dict:
        #     winner_dict[key] /= num_iters
        # print(sum(winner_dict.values())==1)        
        return winner_dict,final_dict,qf_dict,round8_dict

    def getWinner(self,home_team,away_team,E_dict):
        """ Use Expectation of Poisson to get a winner of the single game """
        team1 = min(home_team,away_team)
        team2 = max(home_team,away_team)
        l_A,l_B = E_dict[(team1,team2)]
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
        
    def get_winner_probability(self):
        if not self.predicted_winner:
            self.get_tournament_probability()
        return self.predicted_winner

    def get_final_probability(self):
        if not self.predicted_final:
            self.get_tournament_probability()
        return self.predicted_final

    def get_qf_probability(self):
        if not self.predicted_qf:
            self.get_tournament_probability()
        return self.predicted_qf

    def get_round8_probability(self):
        if not self.predicted_round8:
            self.get_tournament_probability()
        return self.predicted_round8

    def convert_sample_to_probability_decimal(self,dic):
        for key in dic:
            dic[key] = round(dic[key]/(self.NUM_ITERS),4)
        return

    def make_dic_tournament_ui(self):
        """ Return UI version dictionary : Need post processing to json. """
        result ={}
        result["1"] = self.convert_probability_to_percentage(self.predicted_winner)
        result["2"] = self.convert_probability_to_percentage(self.predicted_final)
        result["4"] = self.convert_probability_to_percentage(self.predicted_qf)
        result["8"] = self.convert_probability_to_percentage(self.predicted_round8)
        return result

    def convert_probability_to_percentage(self,dic):
        result = {}
        for key in dic:
            result[key[0].upper()+key[1:]] = str(round(dic[key]*100,1))+"%"
        return result
        

def make_tournament_prediction_output(tournament):
    """A constructor for a PredictionOutput of the tournament. """
    return ConcreteTournamentOutput(tournament)

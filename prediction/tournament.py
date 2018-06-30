from prediction import independent_poisson_model 
from prediction.tournament_output import TournamentOutput


class Tournament(object):

    NUM_ITERS = 10000
    default_given_round16 = [
            "uruguay","portugal",
            "france","argentina",   
            "brazil","mexico",
            "belgium","japan",
            "spain","russia",
            "croatia","denmark",
            "sweden","switzerland",
            "colombia","england"]
    predicted_round8 = []
    predicted_qf = []
    predicted_final = [] 
    predicted_winner = []

    def get_num_iters(self):
        return self.NUM_ITERS

    def get_given_round16(self):
        return self.default_given_round16

    def get_tournament_probability(self):
        model = independent_poisson_model.IndependentPoissonModel()
        self.predicted_winner,self.predicted_final,self.predicted_qf,self.predicted_round8 = model.sample_tournament(self) 
        self.convert_to_probability_decimal(self.predicted_winner,1)
        self.convert_to_probability_decimal(self.predicted_final,2)
        self.convert_to_probability_decimal(self.predicted_qf,4)
        self.convert_to_probability_decimal(self.predicted_round8,8)
        return
        
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

    def convert_to_probability_decimal(self,dic,num_team):
        for key in dic:
            dic[key] = round(dic[key]/(num_team*self.NUM_ITERS),4)
        return

    def make_dic_tournament_ui(self):
        result ={}
        result["1"] = self.convert_to_probability_percentage(self.predicted_winner)
        result["2"] = self.convert_to_probability_percentage(self.predicted_final)
        result["4"] = self.convert_to_probability_percentage(self.predicted_qf)
        result["8"] = self.convert_to_probability_percentage(self.predicted_round8)
        
        return result
    def convert_to_probability_percentage(self,dic):
        result = {}
        for key in dic:
            result[key[0].upper()+key[1:]] = str(round(dic[key]*100,2))+"%"
        return  result
        


def make_prediction_output(tournament):
    """A constructor for a PredictionOutput of the Independent Poisson model. """
    return TournamentOutput(tournament)



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
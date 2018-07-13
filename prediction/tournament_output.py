class TournamentPredictionOutcome(object):

    def __init__(self, tournament_prediction, num_iters):
        self.prediction = tournament_prediction
        self.num_iters = num_iters

    def get_probability_entire_tournament(self):
        return convert_probability()
    
    def get_probability_specific_round(self, _round):
        """ 
        Get interger round input and give matching round result probability 
        """
        return convert_probability(_round)

    def convert_probability(self, _round = "all", _decimal = True, _string = False):
        def caculate(round_prediction,_decimal,_string):
            round_probability = {}
            for key in round_prediction:
                round_probability[key] = round(round_prediction[key]/(self.num_iters),4)
                if not _decimal:
                    round_probability[key] = round(round_probability[key]*100,1)
                if _string:
                    round_probability[key] = str(round_probability[key])
            return round_probability
        
        if _round == "all":
            converted_probability = {}
            for each_round in self.prediction:
                converted_probability[each_round] = caculate(self.prediction[each_round],_decimal,_string)
            return converted_probability
        else:
            return caculate(self.prediction[_round],_decimal,_string)

    def make_dic_tournament_ui(self):
        """ Return UI version dictionary : Need post processing to json. """
        return convert_probability(_decimal=False, _string=True)

class PredictionOutput(object):
    """An abstract data that represents the prediction output of some model."""
    def get_outcome_prob(self, outcome):
        pass

    def get_nonzero_prob_outcomes_list(self):
        pass


class ConcretePredictionOutput(PredictionOutput):

    def __init__(self, score_dict):
        self.score_dict = score_dict

    def get_outcome_prob(self, outcome):
        if outcome in self.score_dict:
            return self.score_dict[outcome]
        else:
            return 0

    def get_nonzero_prob_outcomes_list(self):
        return list(self.score_dict.items())


class TournamentOutput(object):
    """An abstract data that represents the Tournament output of some model."""
    def get_outcome_prob(self, outcome):
        pass

    def get_nonzero_prob_outcomes_list(self):
        pass

class ConcreteTournamentOutput(TournamentOutput):

    def __init__(self, winner_dict):
        self.winner_dict = winner_dict
    
    def get_outcome_prob(self,outcome):
        if outcome in self.winner_dict:
            return self.winner_dict[outcome]
        else:
            return 0
    def get_nonzero_prob_outcomes_list(self):
        return list(self.winner_dict.items())

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
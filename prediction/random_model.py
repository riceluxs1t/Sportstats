import random
from prediction.prediction_output import ConcretePredictionOutput


class RandomModel(object):
    """A dummy model that predicts a random pair of scores for any match. """
    def predict(self, home_team, away_team):
        return {
            (random.randint(0, 3), random.randint(0, 3)): 1
        }


def make_prediction_output(model_outcome):
    return ConcretePredictionOutput(model_outcome)

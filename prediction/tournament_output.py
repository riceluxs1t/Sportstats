class TournamentOutput(object):
    """An abstract data that represents the Tournament output of some model."""
    def get_winner_prob(self, outcome):
        pass

    def get_nonzero_prob_outcomes_list(self):
        pass

class ConcreteTournamentOutput(TournamentOutput):

    def __init__(self, tournament):
        self.tournament = tournament
    
    def get_winner_prob(self,outcome):
        outcome = outcome.lower()
        if outcome in self.tournament:
            return self.tournament[outcome]
        else:
            return 0

    def get_nonzero_prob_outcomes_list(self):
        return list(self.tournament.items())

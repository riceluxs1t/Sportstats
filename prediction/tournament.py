# from prediction import independent_poisson_model 

class Tournament(object):
    def __init__(self, _games):
        self.games = _games

    def get_current_round_of_games(self):
        # e.g. return [('France', 'Belgium'), ('England', 'Croatia')]
        return self.games

    def advance(self,current_rounds_results):
        # e.g. current_rounds_results = ['France', 'England']
        # returns a new Tournament instance with [('France', 'England')] as its leaf node.
        if len(current_rounds_results)>1:
            current_rounds_results = list(zip(current_rounds_results[::2], current_rounds_results[1:][::2]))
            
        elif len(current_rounds_results) == 1:
            current_rounds_results= (current_rounds_results)
        else:
            # If advanced with no team is error return current one
            print("Can't advance with no team")
            current_rounds_results = self.games
        return Tournament(current_rounds_results)

    def get_teams(self):
        result =[]
        if not this.is_finished():
            for game in self.games:
                result.append(game[0])
                result.append(game[1])
            return result
        else:
            return list(games[0][0])


    def is_finished(self):
        if len(self.games[0]) == 1:
            return True
        else:
            return False
# from prediction import independent_poisson_model 
from prediction.tournament_output import TournamentPredictionOutcome
from collections import defaultdict
from numpy.random import randint
from numpy.random import poisson as numpy_poisson_distribution

class TournamentPredictionModel(object):
    def __init__(self, single_match_model, tournament):
        self.single_match_model = single_match_model
        self.starting_tournament = tournament
        self.expectation_of_teams = defaultdict(float)
        self.num_iters = 10000
    
    def predict(self): # returns an instance of TournamentPredictionOutcome
        prediction = {}
        round_length = len(self.starting_tournament.get_current_round_of_games())
        while round_length >= 1:
            prediction[round_length] = defaultdict(float)
            round_length /= 2
        print(prediction)            
        print(self.simulate_tournament())
        for _ in range(self.num_iters): # run 10000 simualtions
            single_iter_result = simulate_tournament()
            for round_ in single_iter_result:
                for team in round_: 
                    prediction[round_][team] += 1
        return TournamentPredictionOutcome(prediction, self.num_iters)

    def simulate_round(self,tournament):
        games = tournament.get_current_round_of_games()
        result = []
        for game in games:
            # compute some result
            home_team = game[0]
            away_team = game[1]
            result.append(self.getWinner(home_team,away_team))        
        return result, tournament.advance(result)

    def simulate_tournament(self):
        def update(_tournament_result, _result):
                # do some update however you like
                proceeding_teams = []
                for game in _result:
                    proceeding_teams.append(game[0])
                    proceeding_teams.append(game[1])
                _tournament_result[len(_result)*2] = proceeding_teams

        tournament = self.starting_tournament
        tournament_result = {}
        while not tournament.is_finished():
            # for team in tournament.get_current_round_of_games():
            round_result, tournament = self.simulate_round(tournament)
            update(tournament_result, round_result)
        return tournament_result


    def getWinner(self,home_team,away_team):
        """ Use Expectation of Poisson to get a winner of the single game """
        model = self.single_match_model
        E_dict = self.expectation_of_teams
        team1 = min(home_team,away_team)
        team2 = max(home_team,away_team)
        if (team1,team2) in E_dict:
            l_A,l_B = E_dict[(team1,team2)]
        else:
            E_dict[(team1,team2)] = model.getExpectation(team1,team2) 
            l_A,l_B = E_dict[(team1,team2)]

        home_team_score = numpy_poisson_distribution(l_A,1)
        away_team_score = numpy_poisson_distribution(l_B,s1)
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
    
    



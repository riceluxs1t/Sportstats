from core.models import RawMatch
from django.db.models import Q
import statsmodels.api as sm
from numpy.random import poisson
from collections import defaultdict


# TODO(nate): refactor this guy the hell out of it.
class IndependentPoissonModel(object):
    """Models goals to be scored as two independent Poisson R.Vs. """
    def predict(self, home_team, away_team):

        home_team_elo = self.get_current_elo(home_team)
        away_team_elo = self.get_current_elo(away_team)

        print('home elo = {0}, away_elo = {1}'.format(home_team_elo, away_team_elo))
        uA_B = self.fit_poisson(
            self.filter_matches(home_team),
            home_team,
            True
        ).predict([away_team_elo, 1])

        uB_A = self.fit_poisson(
            self.filter_matches(away_team),
            away_team,
            True
        ).predict([home_team_elo, 1])

        vA_B = self.fit_poisson(
            self.filter_matches(home_team),
            home_team,
            False
        ).predict([away_team_elo, 1])

        vB_A = self.fit_poisson(
            self.filter_matches(away_team),
            away_team,
            False
        ).predict([home_team_elo, 1])

        l_A = (uA_B + vB_A) / 2.0
        l_B = (uB_A + vA_B) / 2.0

        score_dict = self.sample(l_A, l_B)

        for key in score_dict:
            print("{3} {0}:{1} {4} = {2}%.".format(
                key[0], key[1], score_dict[key] * 100, home_team, away_team
            ))

        win, draw, lose = self.compute_win_draw_lose(score_dict)
        print("{3} Win: {0}%, Draw: {1}%, {4} Win: {2}%".format(
            win * 100, draw * 100, lose * 100, home_team, away_team))

    def sample(self, l_A, l_B, num_iters=10000):

        home_team_score_simulations = poisson(l_A, num_iters)
        away_team_score_simulations = poisson(l_B, num_iters)

        score_dict = defaultdict(int)

        for i in range(num_iters):
            score_dict[
                (
                    home_team_score_simulations[i],
                    away_team_score_simulations[i]
                )
            ] += 1

        for key in score_dict:
            score_dict[key] /= num_iters

        return score_dict

    def compute_win_draw_lose(self, score_dict):
        win = 0
        draw = 0
        lose = 0

        for key in score_dict:
            if key[0] > key[1]:
                win += score_dict[key]
            elif key[0] == key[1]:
                draw += score_dict[key]
            else:
                lose += score_dict[key]
        return win, draw, lose

    def filter_matches(self, team_name, home_advantage=False):
        return RawMatch.objects.filter(
            Q(home_team=team_name) | Q(away_team=team_name)
        ).filter(
            home_advantage=home_advantage
        )

    def fit_poisson(self, matches, team_name, scored):

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

        print(num_goals[:10])
        print(elos[:10])

        poisson = sm.Poisson(num_goals, elos)
        poisson_fitted = poisson.fit(method="newton")
        return poisson_fitted

    def get_current_elo(self, team_name):
        matches = self.filter_matches(team_name)
        most_recent_match = matches.order_by('-date')[0]
        if most_recent_match.home_team == team_name:
            return most_recent_match.home_team_resulting_rating
        else:
            return most_recent_match.away_team_resulting_rating

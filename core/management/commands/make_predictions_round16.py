from django.core.management.base import BaseCommand, CommandError
import json
import itertools
from prediction import controller, utils


class Command(BaseCommand):
    help = 'Makes a single match prediction for two given teams.'

    def process_match(self, prediction_outcome):
        win, draw, lose = utils.compute_win_draw_lose(prediction_outcome)

        score_dict_outcomes = []
        score_dict_brief = {
            'win': "{0:.1f}%".format(win * 100),
            'draw': "{0:.1f}%".format(draw * 100),
            'lose': "{0:.1f}%".format(lose * 100)
        }

        rest = 0
        for match_outcome, prob in prediction_outcome.get_nonzero_prob_outcomes_list():
            if (prob * 10000) / 100 > 1:
                home_team_score = match_outcome[0]
                away_team_score = match_outcome[1]
                rest += (prob * 10000) / 100
                score_dict_outcomes.append(
                    {
                        'outcome': "{0} - {1}".format(home_team_score, away_team_score),
                        'prob': (prob * 10000) / 100
                    }
                )
            else:
                rest += (prob * 10000) / 100

        score_dict_outcomes = sorted(
            score_dict_outcomes,
            key=lambda e: e['prob'],
            reverse=True
        )

        score_dict_outcomes = score_dict_outcomes
        for i in range(len(score_dict_outcomes)):
            x = score_dict_outcomes[i]
            x['key'] = i + 1
            x['prob'] = "{0:.1f}%".format(x['prob'])
            score_dict_outcomes[i] = x

        score_dict_outcomes.append({
            'key': len(score_dict_outcomes) + 1,
            'prob': "{0:.1f}%".format(100 - rest),
            'outcome': 'Else'
        })

        return score_dict_brief, score_dict_outcomes

    def handle(self, *args, **options):
        # just for the round of 16
        teams = [
            'Uruguay',
            'France',
            'Brazil',
            'Belgium',
            'Russia',
            'Croatia',
            'Sweden',
            'England'
        ]

        final_json_brief = {}
        final_json_outcomes = {}

        # for i in range(0, len(teams), 2):
        for home_team, away_team in itertools.permutations(teams, 2):
            dict_key = '{0}-{1}'.format(home_team, away_team)

            brief, outcomes = self.process_match(controller.predict(home_team, away_team))

            final_json_brief[dict_key] = brief
            final_json_outcomes[dict_key] = outcomes

            dict_key = '{0}-{1}'.format(away_team, home_team)
            brief, outcomes = self.process_match(controller.predict(away_team, home_team))

            final_json_brief[dict_key] = brief
            final_json_outcomes[dict_key] = outcomes

        with open('predictions_brief.json', 'w') as f:
            f.write(
                json.dumps(final_json_brief)
            )

        with open('predictions_outcomes.json', 'w') as f:
            f.write(
                json.dumps(final_json_outcomes)
            )

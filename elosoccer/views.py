from prediction import controller, utils
import json
from django.http import HttpResponse


def predict(request):

    home_team = request.GET['home_team']
    away_team = request.GET['away_team']

    prediction_outcome = controller.predict(home_team, away_team)
    win, draw, lose = utils.compute_win_draw_lose(prediction_outcome)

    score_dict_string_key = {}
    for match_outcome, prob in prediction_outcome.get_nonzero_prob_outcomes_list():

        home_team_score = match_outcome[0]
        away_team_score = match_outcome[1]

        score_dict_string_key["{0}:{1}".format(home_team_score, away_team_score)] = \
            "{0}%".format((prob * 10000) / 100)

    response = {
        'win': "{0}%".format(int(win*10000) / 100),
        'draw': "{0}%".format(int(draw*10000) / 100),
        'lose': "{0}%".format(int(lose*10000) / 100),
        'scores': score_dict_string_key
    }

    return HttpResponse(json.dumps(response), content_type='application/json')

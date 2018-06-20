from django.shortcuts import render
from prediction import controller
import json
from django.http import HttpResponse


def index(request):
    return render(request, 'index.htm')


def predict(request):

    home_team = request.GET['home_team']
    away_team = request.GET['away_team']

    current_model = controller.get_current_model()

    score_dict = current_model.predict(home_team, away_team)
    win, draw, lose = current_model.compute_win_draw_lose(score_dict)

    score_dict_string_key = {}
    for key in score_dict:
        score_dict_string_key["{0}:{1}".format(key[0], key[1])] = "{0}%".format((score_dict[key] * 10000) / 100)

    response = {
        'win': "{0}%".format(int(win*10000) / 100),
        'draw': "{0}%".format(int(draw*10000) / 100),
        'lose': "{0}%".format(int(lose*10000) / 100),
        'scores': score_dict_string_key
    }

    return HttpResponse(json.dumps(response), content_type='application/json')

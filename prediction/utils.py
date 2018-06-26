from django.db.models import Q

from core.models import RawMatch
from prediction.constants import AVERAGE_ELO


def compute_win_draw_lose(prediction_output):
    win = 0
    draw = 0
    lose = 0

    for match in prediction_output.get_nonzero_prob_outcomes_list():

        home_team_score = match[0][0]
        away_team_score = match[0][1]
        outcome_prob = match[1]

        if home_team_score > away_team_score:
            win += outcome_prob
        elif home_team_score == away_team_score:
            draw += outcome_prob
        else:
            lose += outcome_prob

    return win, draw, lose


def get_current_elo(team_name):
    matches = filter_matches(team_name)
    try:
        most_recent_match = matches.order_by('-date')[0]
        if most_recent_match.home_team == team_name:
            return most_recent_match.home_team_resulting_rating
        else:
            return most_recent_match.away_team_resulting_rating
    # TODO: catch index out of range
    except IndexError:
        return AVERAGE_ELO


def filter_matches(team_name, home_advantage=False):
    return RawMatch.objects.filter(
        Q(home_team=team_name.lower()) | Q(away_team=team_name.lower())
    ).filter(
        home_advantage=home_advantage
    )

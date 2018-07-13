from django.core.management.base import BaseCommand, CommandError
from prediction import controller


class Command(BaseCommand):
    help = 'Makes a single match prediction for two given teams.'

    def add_arguments(self, parser):
        parser.add_argument('teams', nargs='+', type=str)

    def handle(self, *args, **options):

        home_team = options['teams'][0]
        away_team = options['teams'][1]

        current_model = controller.get_current_single_match_model()
        current_model.predict(home_team, away_team)

from django.core.management.base import BaseCommand, CommandError
from core import scraper, loader


class Command(BaseCommand):
    help = 'Loads all the raw match data for year N'

    def add_arguments(self, parser):
        parser.add_argument('year', nargs='+', type=int)

    def handle(self, *args, **options):
        years = options['year']

        for year in years:
            manual_scraper = scraper.ManualScraperAdapter(year)
            matches = manual_scraper.get_match_data()
            loader.load_raw_match_data(matches)
            print('Processed {0} matches for year {1}'.format(
                len(matches),
                year
            ))

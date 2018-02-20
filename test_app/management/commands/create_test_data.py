from django.core.management.base import BaseCommand
from django_graph_api.tests.conftest import starwars_data


class Command(BaseCommand):
    help = "Loads the database with test data."

    def handle(self, *args, **options):
        print("Loading some neato Star Wars trivia into the database.")
        starwars_data(None)

from django.core.management.base import BaseCommand

from core.ingestion import ingest_consumer_csv_file


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def add_arguments(self, parser):
        parser.add_argument("file", metavar="FILE")

    def handle(self, *args, **options):
        with open(options["file"]) as f:
            ingest_consumer_csv_file(f)

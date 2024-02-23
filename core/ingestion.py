import csv

from .models import Consumer

FIELD_MAPPING = {
    "client reference no": "external_id",
    "consumer name": "consumer_name",
    "consumer address": "address",
}


def ingest_consumer_csv_file(csv_file):
    consumers = []

    reader = csv.DictReader(csv_file)

    for row in reader:
        for csv_field, model_field in FIELD_MAPPING.items():
            row[model_field] = row.pop(csv_field)
        consumers.append(Consumer(**row))
    return Consumer.objects.bulk_create(consumers)

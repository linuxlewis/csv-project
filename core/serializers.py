import codecs

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer

from .ingestion import ingest_consumer_csv_file
from .models import Consumer


class ConsumerSerializer(ModelSerializer):

    class Meta:
        model = Consumer
        fields = "__all__"


class ConsumerBulkCreateSerializer(Serializer):

    csv_file = serializers.FileField()

    def create(self, validated_data):
        consumers = ingest_consumer_csv_file(
            codecs.getreader("utf-8")(validated_data["csv_file"])
        )
        return {"success": f"{len(consumers)} ingested"}

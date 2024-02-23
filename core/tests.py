import io

import factory
import factory.faker
from django.urls import reverse
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyDecimal
from rest_framework.test import APITestCase

from .models import Consumer, StatusChoices


class ConsumerFactory(DjangoModelFactory):

    consumer_name = factory.Faker("name")
    balance = FuzzyDecimal(500.0, 30000.0)
    status = StatusChoices.IN_COLLECTION
    address = factory.Faker("address")
    ssn = factory.Faker("ssn")

    class Meta:
        model = Consumer


class ConsumerListAPITestCase(APITestCase):

    def setUp(self) -> None:
        self.url = reverse("consumer-list")
        return super().setUp()

    def test_get(self):

        ConsumerFactory.create_batch(10)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        # it should return all the results
        self.assertEqual(len(response.data["results"]), 10)

    def test_filters(self):
        ConsumerFactory(balance=500, consumer_name="John Schuster")
        ConsumerFactory(balance=100, consumer_name="Joe Brown")
        ConsumerFactory(
            status=StatusChoices.PAID_IN_FULL, balance=200, consumer_name="Sam Jones"
        )

        response = self.client.get(self.url + "?min_balance=100&max_balance=500")
        self.assertEqual(len(response.data["results"]), 3)

        response = self.client.get(self.url + "?max_balance=100")
        self.assertEqual(len(response.data["results"]), 1)

        response = self.client.get(self.url + "?consumer_name=john")
        self.assertEqual(len(response.data["results"]), 1)

        response = self.client.get(self.url + "?consumer_name=john&max_balance=500")
        self.assertEqual(len(response.data["results"]), 1)

        response = self.client.get(self.url + "?status=IN_COLLECTION")
        self.assertEqual(len(response.data["results"]), 2)

        response = self.client.get(self.url + "?status=IN_COLLECTION&consumer_name=joe")
        self.assertEqual(len(response.data["results"]), 1)


class ConsumerCreateAPITestCase(APITestCase):

    def setUp(self) -> None:
        self.url = reverse("consumer-list")
        self.file = io.StringIO(
            """client reference no,balance,status,consumer name,consumer address,ssn
ffeb5d88-e5af-45f0-9637-16ea469c58c0,59638.99,INACTIVE,Jessica Williams,"0233 Edwards Glens
Allisonhaven, HI 91491",018-79-4253
6155ee11-6eb5-4005-abc7-df2fe6c099ea,59464.79,PAID_IN_FULL,Christopher Harrison,"6791 Chang Mountain
Port Jamiehaven, UT 24171",511-96-5364
d984a3b4-d331-4857-8e6f-b44bad2567aa,48598.63,IN_COLLECTION,Peter Nichols,"USNS Smith
FPO AP 59558",648-08-4523"""
        )
        return super().setUp()

    def test_post(self):
        response = self.client.post(self.url, data={"csv_file": self.file})
        self.assertEqual(response.status_code, 201)

        # it should create consumers
        self.assertEqual(Consumer.objects.count(), 3)
        self.assertEqual(response.data["success"], "3 ingested")

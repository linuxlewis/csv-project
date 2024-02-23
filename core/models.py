from django.db import models


class StatusChoices(models.TextChoices):
    INACTIVE = ("INACTIVE", "Inactive")
    IN_COLLECTION = ("IN_COLLECTION", "In Collection")
    PAID_IN_FULL = ("PAID_IN_FULL", "Paid in full")


class Consumer(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    external_id = models.CharField(max_length=256)
    balance = models.DecimalField(decimal_places=2, max_digits=1000)
    status = models.CharField(max_length=14, choices=StatusChoices.choices)
    consumer_name = models.CharField(max_length=1024)
    ssn = models.CharField(max_length=11)
    address = models.TextField()

    class Meta:
        indexes = [
            models.Index(fields=["external_id"]),
            models.Index(fields=["balance"]),
            models.Index(fields=["status"]),
            models.Index(fields=["consumer_name"]),
        ]

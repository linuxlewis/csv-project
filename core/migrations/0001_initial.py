# Generated by Django 5.0.2 on 2024-02-23 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Consumer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("external_id", models.CharField(max_length=256)),
                ("balance", models.DecimalField(decimal_places=2, max_digits=1000)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("INACTIVE", "Inactive"),
                            ("IN_COLLECTION", "In Collection"),
                            ("PAID_IN_FULL", "Paid in full"),
                        ],
                        max_length=14,
                    ),
                ),
                ("consumer_name", models.CharField(max_length=1024)),
                ("ssn", models.CharField(max_length=11)),
                ("address", models.TextField()),
            ],
            options={
                "indexes": [
                    models.Index(
                        fields=["external_id"], name="core_consum_externa_4bc94b_idx"
                    ),
                    models.Index(
                        fields=["balance"], name="core_consum_balance_cc353d_idx"
                    ),
                    models.Index(
                        fields=["status"], name="core_consum_status_32bcae_idx"
                    ),
                    models.Index(
                        fields=["consumer_name"], name="core_consum_consume_b80ef7_idx"
                    ),
                ],
            },
        ),
    ]

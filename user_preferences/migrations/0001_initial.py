# Generated by Django 5.1.3 on 2024-11-24 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="HouseholdStaple",
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
                ("ingredient_name", models.CharField(max_length=255, unique=True)),
                ("added_on", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]

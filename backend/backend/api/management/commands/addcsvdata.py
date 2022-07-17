"""
Django command to add csv data from ingredients.csv
"""
import csv

from django.core.management.base import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    """Django command to add data to database from csv."""

    def handle(self, *args, **options):
        with open('../ingredients.csv', newline='', encoding='utf-8') as f:
            csv_reader = csv.reader(f)
            next(csv_reader)
            for row in csv_reader:
                Ingredient.objects.get_or_create(
                    name=row[0],
                    measurement_unit=row[1]
                )

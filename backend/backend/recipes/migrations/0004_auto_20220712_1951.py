# Generated by Django 2.2.28 on 2022-07-12 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_auto_20220712_1828'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredientrecipe',
            options={'ordering': ('recipe',)},
        ),
        migrations.AlterUniqueTogether(
            name='ingredientrecipe',
            unique_together=set(),
        ),
        migrations.AddConstraint(
            model_name='ingredientrecipe',
            constraint=models.UniqueConstraint(fields=('recipe', 'ingredient'), name='unique_fields'),
        ),
    ]

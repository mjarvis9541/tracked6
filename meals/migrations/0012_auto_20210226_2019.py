# Generated by Django 3.1.6 on 2021-02-26 20:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meals', '0011_meal_slug'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mealitem',
            options={'verbose_name': 'meal item', 'verbose_name_plural': 'meal items'},
        ),
    ]
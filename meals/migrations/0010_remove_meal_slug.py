# Generated by Django 3.1.6 on 2021-02-22 12:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meals', '0009_auto_20210222_1250'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meal',
            name='slug',
        ),
    ]
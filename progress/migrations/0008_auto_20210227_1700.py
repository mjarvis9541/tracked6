# Generated by Django 3.1.6 on 2021-02-27 17:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('progress', '0007_auto_20210227_1540'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='progress',
            options={
                'verbose_name': 'progress log',
                'verbose_name_plural': 'progress logs',
            },
        ),
    ]

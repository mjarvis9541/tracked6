# Generated by Django 3.1.6 on 2021-02-12 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diaries', '0003_auto_20210211_1910'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diary',
            name='datetime_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='date created'),
        ),
        migrations.AlterField(
            model_name='diary',
            name='datetime_updated',
            field=models.DateTimeField(auto_now=True, verbose_name='date updated'),
        ),
    ]

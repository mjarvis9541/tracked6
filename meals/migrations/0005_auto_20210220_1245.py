# Generated by Django 3.1.6 on 2021-02-20 12:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('meals', '0004_auto_20210220_1242'),
    ]

    operations = [
        migrations.AddField(
            model_name='meal',
            name='datetime_created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='date created'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='meal',
            name='datetime_updated',
            field=models.DateTimeField(auto_now=True, verbose_name='date updated'),
        ),
    ]

# Generated by Django 3.1.6 on 2021-02-28 14:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diaries', '0006_auto_20210220_1724'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='diary',
            options={'verbose_name': 'food diary entry', 'verbose_name_plural': 'food diary entries'},
        ),
    ]
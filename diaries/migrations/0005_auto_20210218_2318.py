# Generated by Django 3.1.6 on 2021-02-18 23:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diaries', '0004_auto_20210212_1245'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='diary',
            options={'verbose_name': 'diary entry', 'verbose_name_plural': 'diary entries'},
        ),
    ]
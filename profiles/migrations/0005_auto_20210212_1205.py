# Generated by Django 3.1.6 on 2021-02-12 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_auto_20210211_1327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='carbohydrate',
            field=models.DecimalField(decimal_places=1, max_digits=4),
        ),
        migrations.AlterField(
            model_name='profile',
            name='energy',
            field=models.IntegerField(verbose_name='energy (kcal)'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='fat',
            field=models.DecimalField(decimal_places=1, max_digits=4),
        ),
        migrations.AlterField(
            model_name='profile',
            name='fibre',
            field=models.DecimalField(decimal_places=1, max_digits=4),
        ),
        migrations.AlterField(
            model_name='profile',
            name='protein',
            field=models.DecimalField(decimal_places=1, max_digits=4),
        ),
        migrations.AlterField(
            model_name='profile',
            name='salt',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='profile',
            name='saturates',
            field=models.DecimalField(decimal_places=1, max_digits=4),
        ),
        migrations.AlterField(
            model_name='profile',
            name='sugars',
            field=models.DecimalField(decimal_places=1, max_digits=4),
        ),
    ]

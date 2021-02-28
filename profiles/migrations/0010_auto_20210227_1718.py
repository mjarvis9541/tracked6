# Generated by Django 3.1.6 on 2021-02-27 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0009_auto_20210227_1700'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='activity_level',
            field=models.CharField(
                blank=True,
                choices=[
                    ('SD', 'Sedentary'),
                    ('LA', 'Lightly Active'),
                    ('MA', 'Moderately Active'),
                    ('VA', 'Very Active'),
                    ('EA', 'Extra Active'),
                ],
                help_text='\n        <ul>\n        <li>Sedentary - Little to no exercise.</li>        <li>Light Activity - Exercise 1 to 2 days a week.</li>        <li>Moderate Activity - Exercise 3 to 5 days a week.</li>        <li>High Activity - Exercise 6 to 7 days a week.</li>        <li>Very High Activity - Exercise 6 to 7 days a week, and a physical job.</li>        </ul>\n        ',
                max_length=2,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name='profile',
            name='calculation_method',
            field=models.CharField(
                blank=True,
                choices=[
                    ('REC', 'Recommended'),
                    ('PER', 'Percent'),
                    ('GRA', 'Grams'),
                    ('CUS', 'Custom'),
                ],
                editable=False,
                max_length=3,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name='profile',
            name='carbohydrate',
            field=models.DecimalField(
                decimal_places=1,
                default=260,
                max_digits=4,
                verbose_name='carbohydrate (g)',
            ),
        ),
        migrations.AlterField(
            model_name='profile',
            name='fat',
            field=models.DecimalField(decimal_places=1, default=70, max_digits=4, verbose_name='fat (g)'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='fibre',
            field=models.DecimalField(decimal_places=1, default=30, max_digits=4, verbose_name='fibre (g)'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='goal',
            field=models.CharField(
                blank=True,
                choices=[
                    ('LW', 'Lose Fat'),
                    ('MW', 'Maintain Weight'),
                    ('GW', 'Build Muscle'),
                ],
                help_text='\n        <ul>\n        <li>Lose Fat.</li>        <li>Maintain Weight.</li>        <li>Gain Muscle.</li>        </ul>\n        ',
                max_length=2,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name='profile',
            name='goal_weight',
            field=models.DecimalField(
                blank=True,
                decimal_places=1,
                help_text="Set a goal weight and we'll estimate how long it'll take for you to reach it.",
                max_digits=4,
                null=True,
                verbose_name='goal weight (kg)',
            ),
        ),
        migrations.AlterField(
            model_name='profile',
            name='protein',
            field=models.DecimalField(decimal_places=1, default=50, max_digits=4, verbose_name='protein (g)'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='salt',
            field=models.DecimalField(decimal_places=2, default=6, max_digits=5, verbose_name='salt (g)'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='saturates',
            field=models.DecimalField(decimal_places=1, default=20, max_digits=4, verbose_name='saturates (g)'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='sugars',
            field=models.DecimalField(decimal_places=1, default=90, max_digits=4, verbose_name='sugars (g)'),
        ),
    ]

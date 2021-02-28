# Generated by Django 3.1.6 on 2021-02-27 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0008_auto_20210227_1540'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='activity_level',
            field=models.CharField(
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
        migrations.AddField(
            model_name='profile',
            name='calculation_method',
            field=models.CharField(
                choices=[
                    ('REC', 'Recommended'),
                    ('PER', 'Percent'),
                    ('GRA', 'Grams'),
                    ('CUS', 'Custom'),
                ],
                max_length=3,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name='profile',
            name='goal',
            field=models.CharField(
                choices=[
                    ('LW', 'Lose Fat'),
                    ('MW', 'Maintain Weight'),
                    ('GW', 'Build Muscle'),
                ],
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
                max_digits=4,
                null=True,
                verbose_name='goal weight (kg)',
            ),
        ),
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(
                blank=True,
                default='images/default.jpg',
                null=True,
                upload_to='images/profile_pictures',
                verbose_name='profile picture',
            ),
        ),
    ]

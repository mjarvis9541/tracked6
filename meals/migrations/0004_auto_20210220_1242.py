# Generated by Django 3.1.6 on 2021-02-20 12:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0010_auto_20210218_2318'),
        ('meals', '0003_auto_20210218_2318'),
    ]

    operations = [
        migrations.AddField(
            model_name='meal',
            name='item_10',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='meal_items_10', to='food.food'),
        ),
        migrations.AddField(
            model_name='meal',
            name='item_10_quantity',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True),
        ),
        migrations.AddField(
            model_name='meal',
            name='item_6',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='meal_items_6', to='food.food'),
        ),
        migrations.AddField(
            model_name='meal',
            name='item_6_quantity',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True),
        ),
        migrations.AddField(
            model_name='meal',
            name='item_7',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='meal_items_7', to='food.food'),
        ),
        migrations.AddField(
            model_name='meal',
            name='item_7_quantity',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True),
        ),
        migrations.AddField(
            model_name='meal',
            name='item_8',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='meal_items_8', to='food.food'),
        ),
        migrations.AddField(
            model_name='meal',
            name='item_8_quantity',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True),
        ),
        migrations.AddField(
            model_name='meal',
            name='item_9',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='meal_items_9', to='food.food'),
        ),
        migrations.AddField(
            model_name='meal',
            name='item_9_quantity',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True),
        ),
        migrations.AlterField(
            model_name='meal',
            name='description',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddConstraint(
            model_name='meal',
            constraint=models.UniqueConstraint(fields=('user', 'name'), name='unique_meal_name'),
        ),
    ]
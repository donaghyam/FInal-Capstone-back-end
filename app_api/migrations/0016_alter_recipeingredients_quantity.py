# Generated by Django 4.0.5 on 2022-06-13 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_api', '0015_alter_recipeingredients_quantity_alter_steps_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipeingredients',
            name='quantity',
            field=models.DecimalField(decimal_places=3, max_digits=4),
        ),
    ]

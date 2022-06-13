# Generated by Django 4.0.5 on 2022-06-10 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipeingredients',
            name='quantity',
            field=models.DecimalField(decimal_places=3, max_digits=4),
        ),
        migrations.AlterField(
            model_name='recipes',
            name='abv',
            field=models.DecimalField(decimal_places=3, max_digits=5),
        ),
        migrations.AlterField(
            model_name='recipes',
            name='batch_volume',
            field=models.DecimalField(decimal_places=3, max_digits=5),
        ),
        migrations.AlterField(
            model_name='recipes',
            name='final_gravity',
            field=models.DecimalField(decimal_places=4, max_digits=5),
        ),
        migrations.AlterField(
            model_name='recipes',
            name='mash_ph',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='recipes',
            name='pre_boil_volume',
            field=models.DecimalField(decimal_places=3, max_digits=5),
        ),
        migrations.AlterField(
            model_name='recipes',
            name='starting_gravity',
            field=models.DecimalField(decimal_places=4, max_digits=5),
        ),
    ]

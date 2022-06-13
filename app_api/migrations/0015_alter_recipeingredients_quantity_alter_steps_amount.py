# Generated by Django 4.0.5 on 2022-06-13 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_api', '0014_alter_useringredients_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipeingredients',
            name='quantity',
            field=models.DecimalField(decimal_places=2, max_digits=4),
        ),
        migrations.AlterField(
            model_name='steps',
            name='amount',
            field=models.DecimalField(decimal_places=1, max_digits=4, null=True),
        ),
    ]
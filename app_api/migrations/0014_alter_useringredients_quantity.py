# Generated by Django 4.0.5 on 2022-06-10 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_api', '0013_alter_useringredients_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useringredients',
            name='quantity',
            field=models.IntegerField(),
        ),
    ]

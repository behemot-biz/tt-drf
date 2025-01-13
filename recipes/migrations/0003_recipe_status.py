# Generated by Django 4.2.16 on 2025-01-11 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_ingredient_measurement_remove_recipe_ingredients_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='status',
            field=models.CharField(choices=[('pending_publish', 'Pending Publish'), ('published', 'Published'), ('pending_delete', 'Pending Delete')], default='published', max_length=20),
        ),
    ]

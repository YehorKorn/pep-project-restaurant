# Generated by Django 4.2 on 2023-05-06 11:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('meal', '0004_rename_cooker_cook'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meal',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='meals', to='meal.category'),
        ),
    ]

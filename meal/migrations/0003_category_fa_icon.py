# Generated by Django 4.2 on 2023-06-28 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meal', '0002_alter_meal_name_alter_meal_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='fa_icon',
            field=models.CharField(default='fa-hamburger', max_length=25),
            preserve_default=False,
        ),
    ]
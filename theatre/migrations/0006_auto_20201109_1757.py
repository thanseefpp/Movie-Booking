# Generated by Django 3.1.2 on 2020-11-09 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theatre', '0005_upcomingmovies'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nowshowingmovies',
            name='trailer_link',
            field=models.URLField(max_length=500),
        ),
        migrations.AlterField(
            model_name='upcomingmovies',
            name='trailer_link',
            field=models.URLField(max_length=500),
        ),
    ]

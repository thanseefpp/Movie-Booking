# Generated by Django 3.1.3 on 2020-12-16 19:11

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('theatre', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='nowshowingmovies',
            name='show_date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='nowshowingmovies',
            name='release_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='nowshowingmovies',
            name='show_time',
            field=models.TimeField(),
        ),
    ]
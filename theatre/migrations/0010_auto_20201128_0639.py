# Generated by Django 3.1.3 on 2020-11-28 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theatre', '0009_nowshowingmovies_dealer'),
    ]

    operations = [
        migrations.AddField(
            model_name='screen',
            name='executive_price',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='screen',
            name='normal_price',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='screen',
            name='premium_price',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='screen',
            name='vip_price',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
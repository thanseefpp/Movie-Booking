# Generated by Django 3.1.3 on 2020-12-06 10:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('theatre', '0018_auto_20201206_1009'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookingaddress',
            name='movies',
        ),
        migrations.RemoveField(
            model_name='bookingaddress',
            name='seatSelect',
        ),
    ]
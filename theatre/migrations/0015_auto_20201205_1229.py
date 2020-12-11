# Generated by Django 3.1.3 on 2020-12-05 12:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('theatre', '0014_bookingaddress'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booked',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_orderd', models.DateTimeField(auto_now_add=True)),
                ('complete', models.BooleanField(default=False, null=True)),
                ('transaction_id', models.CharField(max_length=200, null=True)),
                ('order_status', models.CharField(default='Success', max_length=200, null=True)),
                ('paid_amount', models.DecimalField(decimal_places=2, max_digits=8)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=300, null=True)),
                ('phone_number', models.CharField(max_length=300, null=True)),
                ('first_name', models.CharField(max_length=300, null=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='BookingAddress',
        ),
        migrations.AddField(
            model_name='booked',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='theatre.customer'),
        ),
        migrations.AddField(
            model_name='booked',
            name='seatSelect',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='theatre.seatselected'),
        ),
    ]
# Generated by Django 3.1.3 on 2020-12-21 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='contents',
            field=models.CharField(max_length=2000, null=True),
        ),
    ]

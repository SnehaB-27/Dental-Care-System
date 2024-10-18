# Generated by Django 5.1.2 on 2024-10-14 16:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_page', '0003_slotavailability'),
    ]

    operations = [
        migrations.AddField(
            model_name='slotavailability',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='date',
            field=models.DateField(),
        ),
    ]

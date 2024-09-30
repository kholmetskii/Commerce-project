# Generated by Django 4.2.16 on 2024-09-30 22:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_listing_last_bid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bid',
            old_name='bid_time',
            new_name='time_of_posting',
        ),
        migrations.RemoveField(
            model_name='bid',
            name='bid_amount',
        ),
        migrations.AddField(
            model_name='bid',
            name='amount',
            field=models.FloatField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]

# Generated by Django 4.1.3 on 2022-11-09 10:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_bid_time'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bid',
            old_name='time',
            new_name='posted_on',
        ),
    ]
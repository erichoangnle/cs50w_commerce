# Generated by Django 4.1.3 on 2022-11-09 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_rename_posted_on_bid_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='time',
            field=models.TimeField(null=True),
        ),
        migrations.AddField(
            model_name='listing',
            name='time',
            field=models.TimeField(null=True),
        ),
    ]
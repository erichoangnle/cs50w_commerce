# Generated by Django 4.1.3 on 2022-11-07 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_listing_watchlist_delete_listings_bids_bid_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='watchlist',
            name='love',
            field=models.CharField(max_length=5, null=True),
        ),
    ]

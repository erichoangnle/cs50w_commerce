# Generated by Django 4.1.3 on 2022-11-09 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_rename_bids_bid_rename_categories_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='time',
            field=models.TimeField(null=True),
        ),
    ]

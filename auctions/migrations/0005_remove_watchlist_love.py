# Generated by Django 4.1.3 on 2022-11-07 14:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_watchlist_love'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='watchlist',
            name='love',
        ),
    ]

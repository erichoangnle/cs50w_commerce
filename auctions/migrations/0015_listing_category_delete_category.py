# Generated by Django 4.1.3 on 2022-11-10 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_alter_won_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='category',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]

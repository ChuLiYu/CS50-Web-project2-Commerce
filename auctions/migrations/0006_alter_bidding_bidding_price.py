# Generated by Django 4.1.3 on 2022-11-22 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0005_alter_listing_start_bid"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bidding",
            name="bidding_price",
            field=models.FloatField(null=True),
        ),
    ]

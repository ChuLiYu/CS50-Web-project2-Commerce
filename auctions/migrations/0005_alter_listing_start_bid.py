# Generated by Django 4.1.3 on 2022-11-22 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0004_alter_listing_creator_id_alter_listing_img_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="listing",
            name="start_bid",
            field=models.FloatField(null=True),
        ),
    ]
# Generated by Django 4.1.3 on 2022-11-28 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0010_alter_listing_img_alter_watchlist_creator_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="listing",
            name="img",
            field=models.ImageField(blank=True, null=True, upload_to="images"),
        ),
    ]

# Generated by Django 4.1.3 on 2022-12-19 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0014_alter_listing_img"),
    ]

    operations = [
        migrations.AlterField(
            model_name="listing",
            name="img",
            field=models.ImageField(blank=True, null=True, upload_to="image"),
        ),
    ]

# Generated by Django 4.1.3 on 2022-11-22 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0002_bidding_listing_alter_user_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="listing",
            name="category",
            field=models.TextField(choices=[("A", "AAA"), ("B", "BBB")], max_length=64),
        ),
    ]
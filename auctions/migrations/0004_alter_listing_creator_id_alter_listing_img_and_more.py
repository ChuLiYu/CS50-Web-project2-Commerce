# Generated by Django 4.1.3 on 2022-11-22 10:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0003_alter_listing_category"),
    ]

    operations = [
        migrations.AlterField(
            model_name="listing",
            name="creator_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="listing_user_id",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="listing",
            name="img",
            field=models.ImageField(blank=True, null=True, upload_to=""),
        ),
        migrations.AlterField(
            model_name="listing",
            name="img_link",
            field=models.URLField(blank=True, null=True),
        ),
    ]

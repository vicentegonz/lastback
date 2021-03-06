# Generated by Django 3.2 on 2021-06-07 23:55

import datetime

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("operations", "0004_serviceindicator"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="kpi",
            name="timestamp",
        ),
        migrations.AddField(
            model_name="kpi",
            name="category",
            field=models.CharField(default=None, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="kpi",
            name="date",
            field=models.DateField(default=datetime.date.today, verbose_name="date"),
        ),
        migrations.AddField(
            model_name="kpi",
            name="metadata",
            field=models.JSONField(default=dict),
        ),
    ]

# Generated by Django 3.2 on 2021-06-14 23:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("operations", "0006_product"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="kpi",
            name="metadata",
        ),
        migrations.AddField(
            model_name="kpi",
            name="units",
            field=models.CharField(max_length=255, null=True),
        ),
    ]

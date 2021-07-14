# Generated by Django 3.2 on 2021-07-05 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("operations", "0008_auto_20210615_0317"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="serviceindicator",
            name="name",
        ),
        migrations.RemoveField(
            model_name="serviceindicator",
            name="value",
        ),
        migrations.AddField(
            model_name="serviceindicator",
            name="amount_bathroom",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="serviceindicator",
            name="amount_experience",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="serviceindicator",
            name="amount_kindness",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="serviceindicator",
            name="amount_nps",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="serviceindicator",
            name="amount_quality",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="serviceindicator",
            name="amount_speed",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="serviceindicator",
            name="amount_waiting_time",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="serviceindicator",
            name="bathroom",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="serviceindicator",
            name="experience",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="serviceindicator",
            name="kindness",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="serviceindicator",
            name="nps",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="serviceindicator",
            name="quality",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="serviceindicator",
            name="speed",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="serviceindicator",
            name="waiting_time",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
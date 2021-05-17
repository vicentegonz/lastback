# Generated by Django 3.2 on 2021-05-14 22:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import backend.common.queries


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_user_role"),
    ]

    operations = [
        migrations.CreateModel(
            name="Device",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "android_id",
                    models.CharField(max_length=255, null=True, unique=True),
                ),
                ("ios_id", models.CharField(max_length=255, null=True, unique=True)),
                (
                    "expo_push_token",
                    models.CharField(max_length=255, null=True, unique=True),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="devices",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="device",
            constraint=models.CheckConstraint(
                check=backend.common.queries.ExtendedQ(
                    backend.common.queries.ExtendedQ(
                        ("android_id__isnull", False),
                        backend.common.queries.ExtendedQ(
                            _negated=True, ios_id__isnull=False
                        ),
                    ),
                    backend.common.queries.ExtendedQ(
                        backend.common.queries.ExtendedQ(
                            _negated=True, android_id__isnull=False
                        ),
                        ("ios_id__isnull", False),
                    ),
                    _connector="OR",
                ),
                name="exactly_one_os_id",
            ),
        ),
    ]

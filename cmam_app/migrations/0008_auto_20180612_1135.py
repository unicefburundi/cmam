# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [("cmam_app", "0007_auto_20180329_1121")]

    operations = [
        migrations.AlterModelOptions(name="facility", options={"ordering": ("name",)}),
        migrations.AlterModelOptions(
            name="patientreports", options={"ordering": ("facility",)}
        ),
        migrations.AlterModelOptions(
            name="reporter", options={"ordering": ("phone_number", "facility__name")}
        ),
        migrations.AddField(
            model_name="facilitytypeproduct",
            name="functional",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="product",
            name="functional",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="reporter",
            name="functional",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="stock",
            name="functional",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="temporary",
            name="functional",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="user",
            name="functional",
            field=models.BooleanField(default=True),
        ),
    ]

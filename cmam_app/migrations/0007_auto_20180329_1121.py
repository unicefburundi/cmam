# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ("bdiadmin", "0014_cds_functional"),
        ("cmam_app", "0006_facility_functional"),
    ]

    operations = [
        migrations.AddField(
            model_name="facility",
            name="cds",
            field=models.ForeignKey(blank=True, to="bdiadmin.CDS", null=True),
        ),
        migrations.AddField(
            model_name="facility",
            name="district",
            field=models.ForeignKey(blank=True, to="bdiadmin.District", null=True),
        ),
        migrations.AddField(
            model_name="facility",
            name="province",
            field=models.ForeignKey(blank=True, to="bdiadmin.Province", null=True),
        ),
    ]

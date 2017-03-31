# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cmam_app', '0003_patientreports'),
    ]

    operations = [
        migrations.AddField(
            model_name='patientreports',
            name='facility',
            field=models.ForeignKey(blank=True, to='cmam_app.Facility', null=True),
        ),
        migrations.AlterField(
            model_name='patientreports',
            name='date_of_first_week_day',
            field=models.DateField(default=b'2016-10-24'),
        ),
    ]

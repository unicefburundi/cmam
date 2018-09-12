# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cmam_app', '0004_auto_20161024_1027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientreports',
            name='date_of_first_week_day',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]

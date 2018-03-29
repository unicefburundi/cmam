# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cmam_app', '0005_auto_20170319_1401'),
    ]

    operations = [
        migrations.AddField(
            model_name='facility',
            name='functional',
            field=models.BooleanField(default=True),
        ),
    ]

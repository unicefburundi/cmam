# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [("bdiadmin", "0013_auto_20170319_1415")]

    operations = [
        migrations.AddField(
            model_name="cds", name="functional", field=models.BooleanField(default=True)
        )
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cmam_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='incomingpatientsreport',
            old_name='transfert_interne',
            new_name='transfert_interne_i',
        ),
        migrations.RenameField(
            model_name='outgoingpatientsreport',
            old_name='transfert_interne',
            new_name='transfert_interne_o',
        ),
    ]

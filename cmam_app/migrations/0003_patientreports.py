# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [("cmam_app", "0002_auto_20161004_1049")]

    operations = [
        migrations.CreateModel(
            name="PatientReports",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("week", models.CharField(default="", max_length=5)),
                ("total_debut_semaine", models.IntegerField(default=0)),
                ("ptb", models.IntegerField(default=0)),
                ("oedemes", models.IntegerField(default=0)),
                ("rechute", models.IntegerField(default=0)),
                ("readmission", models.IntegerField(default=0)),
                ("transfert_interne_i", models.IntegerField(default=0)),
                ("date_of_first_week_day", models.DateField(auto_now=True)),
                ("gueri", models.IntegerField(default=0)),
                ("deces", models.IntegerField(default=0)),
                ("abandon", models.IntegerField(default=0)),
                ("non_repondant", models.IntegerField(default=0)),
                ("transfert_interne_o", models.IntegerField(default=0)),
            ],
        )
    ]

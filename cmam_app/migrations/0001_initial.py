# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Facility",
            fields=[
                (
                    "id_facility",
                    models.CharField(max_length=10, serialize=False, primary_key=True),
                ),
                ("name", models.CharField(max_length=50)),
            ],
            options={"ordering": ("id_facility",)},
        ),
        migrations.CreateModel(
            name="FacilityType",
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
                ("name", models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name="FacilityTypeProduct",
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
                ("site_measuring_unit", models.CharField(max_length=40)),
                ("priority_in_sms", models.IntegerField()),
                ("can_be_fractioned", models.BooleanField()),
                ("facility_type", models.ForeignKey(to="cmam_app.FacilityType")),
            ],
            options={"ordering": ("priority_in_sms",)},
        ),
        migrations.CreateModel(
            name="IncomingPatientsReport",
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
                ("total_debut_semaine", models.IntegerField(default=0)),
                ("ptb", models.IntegerField(default=0)),
                ("oedemes", models.IntegerField(default=0)),
                ("rechute", models.IntegerField(default=0)),
                ("readmission", models.IntegerField(default=0)),
                ("transfert_interne", models.IntegerField(default=0)),
                ("date_of_first_week_day", models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name="OutgoingPatientsReport",
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
                ("gueri", models.IntegerField(default=0)),
                ("deces", models.IntegerField(default=0)),
                ("abandon", models.IntegerField(default=0)),
                ("non_repondant", models.IntegerField(default=0)),
                ("transfert_interne", models.IntegerField(default=0)),
                ("date_of_first_week_day", models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name="Product",
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
                ("designation", models.CharField(max_length=40)),
                ("general_measuring_unit", models.CharField(max_length=40)),
                ("dose_par_semaine", models.FloatField()),
                ("quantite_en_stock_central", models.FloatField(default=0.0)),
            ],
            options={"ordering": ("designation",)},
        ),
        migrations.CreateModel(
            name="ProductsReceptionReport",
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
                ("quantite_recue", models.FloatField(default=0.0)),
                ("produit", models.ForeignKey(to="cmam_app.Product")),
            ],
        ),
        migrations.CreateModel(
            name="ProductStockReport",
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
                ("quantite_en_stock", models.FloatField(default=0.0)),
                ("product", models.ForeignKey(to="cmam_app.Product")),
            ],
        ),
        migrations.CreateModel(
            name="ProductsTranferReport",
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
                ("quantite_donnee", models.FloatField(default=0.0)),
                ("produit", models.ForeignKey(to="cmam_app.Product")),
            ],
        ),
        migrations.CreateModel(
            name="Reception",
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
                ("date_de_reception", models.DateField()),
            ],
            options={"ordering": ("date_de_reception",)},
        ),
        migrations.CreateModel(
            name="Report",
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
                ("reporting_date", models.DateField()),
                ("text", models.CharField(max_length=200)),
                ("category", models.CharField(max_length=100)),
                ("facility", models.ForeignKey(to="cmam_app.Facility")),
            ],
            options={"ordering": ("reporting_date",)},
        ),
        migrations.CreateModel(
            name="Reporter",
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
                ("phone_number", models.CharField(max_length=20)),
                ("supervisor_phone_number", models.CharField(max_length=20)),
                ("facility", models.ForeignKey(to="cmam_app.Facility")),
            ],
            options={"ordering": ("phone_number",)},
        ),
        migrations.CreateModel(
            name="Sortie",
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
                ("date_de_sortie", models.DateField()),
                ("destination", models.ForeignKey(to="cmam_app.Facility")),
                ("report", models.ForeignKey(to="cmam_app.Report")),
            ],
            options={"ordering": ("date_de_sortie",)},
        ),
        migrations.CreateModel(
            name="Stock",
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
                ("quantity", models.FloatField(default=0.0)),
                ("id_facility", models.ForeignKey(to="cmam_app.Facility")),
                ("product", models.ForeignKey(to="cmam_app.Product")),
            ],
        ),
        migrations.CreateModel(
            name="StockOutReport",
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
                ("quantite_restante", models.FloatField(default=0.0)),
                ("produit", models.ForeignKey(to="cmam_app.Product")),
                ("report", models.ForeignKey(to="cmam_app.Report")),
            ],
        ),
        migrations.CreateModel(
            name="StockReport",
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
                ("date_of_first_week_day", models.DateField()),
                ("report", models.ForeignKey(to="cmam_app.Report")),
            ],
        ),
        migrations.CreateModel(
            name="Temporary",
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
                ("phone_number", models.CharField(max_length=20)),
                ("supervisor_phone_number", models.CharField(max_length=20)),
                ("facility", models.ForeignKey(to="cmam_app.Facility")),
            ],
        ),
        migrations.CreateModel(
            name="User",
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
                ("nom", models.CharField(max_length=50)),
                ("prenom", models.CharField(max_length=50)),
                ("login", models.CharField(max_length=50)),
                ("password", models.CharField(max_length=50)),
                ("e_mail_address", models.CharField(max_length=50)),
                ("facility", models.ForeignKey(to="cmam_app.Facility")),
            ],
            options={"ordering": ("nom",)},
        ),
        migrations.AddField(
            model_name="reception",
            name="report",
            field=models.ForeignKey(to="cmam_app.Report"),
        ),
        migrations.AddField(
            model_name="productstranferreport",
            name="sortie",
            field=models.ForeignKey(to="cmam_app.Sortie"),
        ),
        migrations.AddField(
            model_name="productstockreport",
            name="stock_report",
            field=models.ForeignKey(to="cmam_app.StockReport"),
        ),
        migrations.AddField(
            model_name="productsreceptionreport",
            name="reception",
            field=models.ForeignKey(to="cmam_app.Reception"),
        ),
        migrations.AddField(
            model_name="outgoingpatientsreport",
            name="report",
            field=models.ForeignKey(to="cmam_app.Report"),
        ),
        migrations.AddField(
            model_name="incomingpatientsreport",
            name="report",
            field=models.ForeignKey(to="cmam_app.Report"),
        ),
        migrations.AddField(
            model_name="facilitytypeproduct",
            name="product",
            field=models.ForeignKey(to="cmam_app.Product"),
        ),
        migrations.AddField(
            model_name="facility",
            name="facility_level",
            field=models.ForeignKey(to="cmam_app.FacilityType"),
        ),
        migrations.AlterUniqueTogether(
            name="facilitytypeproduct",
            unique_together=set([("facility_type", "priority_in_sms")]),
        ),
    ]

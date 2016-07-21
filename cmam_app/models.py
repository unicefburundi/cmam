from django.db import models

# Create your models here.

class FacilityType(models.Model):
	''' In this model we will store sites types '''
	name = models.CharField(max_length=40)

	def __unicode__(self):
		return self.name

class Product(models.Model):
	''' This model will be used to store products (provided in CMAM project) informations '''
	designation = models.CharField(max_length=40)
	general_measuring_unit = models.CharField(max_length=40)
	dose_par_semaine = models.FloatField()
	quantite_en_stock_central = models.FloatField(default=0.0)

	def __unicode__(self):
		return self.designation

	class Meta:
		ordering = ('designation',)

class FacilityTypeProduct(models.Model):
	''' With this model, we will specify which products are used at a given facility level '''
	facility_type = models.ForeignKey(FacilityType)
	product = models.ForeignKey(Product)
	site_measuring_unit = models.CharField(max_length=40)
	priority_in_sms = models.IntegerField()
	can_be_fractioned = models.BooleanField()

	class Meta:
		unique_together = ('facility_type', 'priority_in_sms',)
		ordering = ('priority_in_sms',)

	def __unicode__(self):
		return "{0}".format(self.priority_in_sms)

class Facility(models.Model):
	''' A facility can be a STA, SST, etc '''
	id_facility = models.CharField(primary_key=True, max_length=10)
	name = models.CharField(max_length=50)
	facility_level = models.ForeignKey(FacilityType)

	def __unicode__(self):
		return self.name

	class Meta:
		ordering = ('id_facility',)

class Stock(models.Model):
	''' With this model, it will be possible to know the quantity of a given product which is in a given facility '''
	id_facility = models.ForeignKey(Facility)
	product = models.ForeignKey(Product)
	quantity = models.FloatField(default=0.0)

	def __unicode__(self):
		return "Quantity of {0} at {1}".format(self.product.designation, self.id_facility.name)

class Reporter(models.Model):
	'''In this model, we will store reporters'''
	facility = models.ForeignKey(Facility)
	phone_number = models.CharField(max_length=20)
	supervisor_phone_number = models.CharField(max_length=20)

	def __unicode__(self):
		return self.phone_number

	class Meta:
		ordering = ('phone_number',)

class User(models.Model):
	facility = models.ForeignKey(Facility)
	nom = models.CharField(max_length=50)
	prenom = models.CharField(max_length=50)
	login = models.CharField(max_length=50)
	password = models.CharField(max_length=50)
	e_mail_address = models.CharField(max_length=50)

	def __unicode__(self):
		return self.nom

	class Meta:
		ordering = ('nom',)

class Report(models.Model):
	''' In this model, we will store all reports sent by reporters '''
	facility = models.ForeignKey(Facility)
	reporting_date = models.DateField()
	text = models.CharField(max_length=200)
	category = models.CharField(max_length=100)

	def __unicode__(self):
		return self.text

	class Meta:
		ordering = ('reporting_date',)

class Sortie(models.Model):
	''' If there is a report of products sent from one facility to an other, we store in this model the date
	of that operation and the destination '''
	report = models.ForeignKey(Report)
	date_de_sortie = models.DateField()
	destination = models.ForeignKey(Facility)

	def __unicode__(self):
		return "On {0} , products sent operation to {1} done".format(self.date_de_sortie, self.destination.name)

	class Meta:
		ordering = ('date_de_sortie',)

class Reception(models.Model):
	''' If there is a report on products reception, we store in this model the reception date '''
	report = models.ForeignKey(Report)
	date_de_reception = models.DateField()

	def __unicode__(self):
		return " {0} ".format(self.date_de_reception)

	class Meta:
		ordering = ('date_de_reception',)

class StockOutReport(models.Model):
	''' Informations given in a stock out report are stored in this model '''
	report = models.ForeignKey(Report)
	produit = models.ForeignKey(Product)
	quantite_restante = models.FloatField(default=0.0)

	def __unicode__(self):
		return "{0} => Quantite restante : {1}".format(self.produit.designation, self.quantite_restante)

class ProductsReceptionReport(models.Model):
	''' If there is products reception report, we store in this model quantity received of each product '''
	reception = models.ForeignKey(Reception)
	produit = models.ForeignKey(Product)
	quantite_recue = models.FloatField(default=0.0)

	def __unicode__(self):
		return self.produit.designation

class ProductsTranferReport(models.Model):
	''' If there is a transfer report, each transfered product and its quantity are mentioned in this model '''
	sortie = models.ForeignKey(Sortie)
	produit = models.ForeignKey(Product)
	quantite_donnee = models.FloatField(default=0.0)

	def __unicode__(self):
		return self.produit.designation

class IncomingPatientsReport(models.Model):
	''' In this model, we put patient numbers of different categories of patients received in a week '''
	report = models.ForeignKey(Report)
	total_debut_semaine = models.IntegerField()
	ptb = models.IntegerField()
	oedemes = models.IntegerField()
	rechute = models.IntegerField()
	readmission = models.IntegerField()
	transfert_interne = models.IntegerField()
	date_of_first_week_day = models.DateField()

	def __unicode__(self):
		return "{0} | {1} | ...".format(self.total_debut_semaine, self.ptb)

class OutgoingPatientsReport(models.Model):
	''' In this model, we put patient numbers of different categories of patients who are not on the program since next week '''
	report = models.ForeignKey(Report)
	gueri = models.IntegerField()
	deces = models.IntegerField()
	abandon = models.IntegerField()
	non_repondant = models.IntegerField()
	transfert_interne = models.IntegerField(default=0)
	date_of_first_week_day = models.DateField()

	def __unicode__(self):
		return "{0} | {1} | ...".format(self.gueri, self.deces)

class StockReport(models.Model):
	''' In this model, we record any stock report. Different quantities of different products are stored in the ProductStockReport model'''
	report = models.ForeignKey(Report)
	date_of_first_week_day = models.DateField()

	def __unicode__(self):
		return "{0}".format(self.date_of_first_week_day)

class ProductStockReport(models.Model):
	stock_report = models.ForeignKey(StockReport)
	product = models.ForeignKey(Product)
	quantite_en_stock = models.FloatField(default=0.0)

	def __unicode__(self):
		return "{0} : {1} | ...".format(self.product.designation, self.quantite_en_stock)

class Temporary(models.Model):
    '''
    This model will be used to temporary store a reporter who doesn't finish his self registration
    '''
    facility = models.ForeignKey(Facility)
    phone_number = models.CharField(max_length=20)
    supervisor_phone_number = models.CharField(max_length=20)

    def __unicode__(self):
        return self.phone_number


from cmam_app.models import *
from django.db.models import Q
import re
import datetime
import requests
import json
from django.conf import settings


def send_sms_through_rapidpro(args):
	''' This function sends messages through rapidpro. Contact(s) and the message to send to them must be in args['data'] '''
	url = 'https://api.rapidpro.io/api/v1/broadcasts.json'
	token = getattr(settings,'TOKEN','')

	data = args['data']

	response = requests.post(url, headers={'Content-type': 'application/json', 'Authorization': 'Token %s' % token}, data = json.dumps(data))



def check_number_of_values(args):
	#This function checks if the message sent is composed by an expected number of values
	print("==len(args['text'].split(' '))==")
	print(len(args['text'].split(' ')))
	print(args['text'].split(' '))

	#Let's identify the number of active products
	'''active_products = Product.objects.filter(is_in_use = True)
	if len(active_products) < 1:
		args['valide'] = False
		args['info_to_contact'] = "Exception. Aucun produit n est active dans le systeme. Veuillez contacter l administrateur de ce systeme"
		return

	number_of_active_products = active_products.count()

	args['number_of_active_products'] = number_of_active_products
'''

	#Each message category starts with some mandatory values which are same for all sites
	number_of_common_values = 0	

	if(args['message_type']=='SELF_REGISTRATION' or args['message_type']=='SELF_REGISTRATION_M'):
		if len(args['text'].split(' ')) < 3:
			args['valide'] = False
			args['info_to_contact'] = "Erreur. Vous avez envoye peu de valeurs. Pour corriger, veuillez reenvoyer un message corrige et commencant par le mot cle "+args['mot_cle']
		if len(args['text'].split(' ')) > 3:
			args['valide'] = False
			args['info_to_contact'] = "Erreur. Vous avez envoye beaucoup de valeurs. Pour corriger, veuillez reenvoyer un message corrige et commencant par le mot cle "+args['mot_cle']
		if len(args['text'].split(' ')) == 3:
			args['valide'] = True
			args['info_to_contact'] = "Le nombre de valeurs envoye est correct."
	if(args['message_type']=='STOCK_RECU' or args['message_type']=='STOCK_RECU_M'):
		number_of_common_values = 2
		number_of_mandatory_values = number_of_common_values + number_of_active_products
		if len(args['text'].split(' ')) < number_of_mandatory_values:
			args['valide'] = False
			args['info_to_contact'] = "Erreur. Vous avez envoye peu de valeurs. Pour corriger, veuillez reenvoyer un message corrige et commencant par le mot cle "+args['mot_cle']
		if len(args['text'].split(' ')) > number_of_mandatory_values:
			args['valide'] = False
			args['info_to_contact'] = "Erreur. Vous avez envoye beaucoup de valeurs. Pour corriger, veuillez reenvoyer un message corrige et commencant par le mot cle "+args['mot_cle']
		if len(args['text'].split(' ')) == number_of_mandatory_values:
			args['valide'] = True
			args['info_to_contact'] = "Le nombre de valeurs envoye est correct."
	if(args['message_type']=='STOCK_SORTI' or args['message_type']=='STOCK_SORTI_M'):
		number_of_common_values = 3
		number_of_mandatory_values = number_of_common_values + number_of_active_products
		if len(args['text'].split(' ')) < number_of_mandatory_values:
			args['valide'] = False
			args['info_to_contact'] = "Erreur. Vous avez envoye peu de valeurs. Pour corriger, veuillez reenvoyer un message corrige et commencant par le mot cle "+args['mot_cle']
		if len(args['text'].split(' ')) > number_of_mandatory_values:
			args['valide'] = False
			args['info_to_contact'] = "Erreur. Vous avez envoye beaucoup de valeurs. Pour corriger, veuillez reenvoyer un message corrige et commencant par le mot cle "+args['mot_cle']
		if len(args['text'].split(' ')) == number_of_mandatory_values:
			args['valide'] = True
			args['info_to_contact'] = "Le nombre de valeurs envoye est correct."
	if(args['message_type']=='RUPTURE' or args['message_type']=='RUPTURE_M'):
		if len(args['text'].split(' ')) < 3:
			args['valide'] = False
			args['info_to_contact'] = "Erreur. Vous avez envoye peu de valeurs. Pour corriger, veuillez reenvoyer un message corrige et commencant par le mot cle "+args['mot_cle']
		if len(args['text'].split(' ')) > 3:
			args['valide'] = False
			args['info_to_contact'] = "Erreur. Vous avez envoye beaucoup de valeurs. Pour corriger, veuillez reenvoyer un message corrige et commencant par le mot cle "+args['mot_cle']
		if len(args['text'].split(' ')) == 3:
			args['valide'] = True
			args['info_to_contact'] = "Le nombre de valeurs envoye est correct."
	if(args['message_type']=='BALANCE' or args['message_type']=='BALANCE_M'):
		number_of_common_values = 2
		number_of_mandatory_values = number_of_common_values + number_of_active_products
		if len(args['text'].split(' ')) < number_of_mandatory_values:
			args['valide'] = False
			args['info_to_contact'] = "Erreur. Vous avez envoye peu de valeurs. Pour corriger, veuillez reenvoyer un message corrige et commencant par le mot cle "+args['mot_cle']
		if len(args['text'].split(' ')) > number_of_mandatory_values:
			args['valide'] = False
			args['info_to_contact'] = "Erreur. Vous avez envoye beaucoup de valeurs. Pour corriger, veuillez reenvoyer un message corrige et commencant par le mot cle "+args['mot_cle']
		if len(args['text'].split(' ')) == number_of_mandatory_values:
			args['valide'] = True
			args['info_to_contact'] = "Le nombre de valeurs envoye est correct."
	if(args['message_type']=='ADMISSION' or args['message_type']=='ADMISSION_M'):
		if len(args['text'].split(' ')) < 8:
			args['valide'] = False
			args['info_to_contact'] = "Erreur. Vous avez envoye peu de valeurs. Pour corriger, veuillez reenvoyer un message corrige et commencant par le mot cle "+args['mot_cle']
		if len(args['text'].split(' ')) > 8:
			args['valide'] = False
			args['info_to_contact'] = "Erreur. Vous avez envoye beaucoup de valeurs. Pour corriger, veuillez reenvoyer un message corrige et commencant par le mot cle "+args['mot_cle']
		if len(args['text'].split(' ')) == 8:
			args['valide'] = True
			args['info_to_contact'] = "Le nombre de valeurs envoye est correct."
	if(args['message_type']=='SORTI' or args['message_type']=='SORTI_M'):
		if args['facility'].facility_level == 'CDS':
			if len(args['text'].split(' ')) < 7:
				args['valide'] = False
				args['info_to_contact'] = "Erreur. Vous avez envoye peu de valeurs. Pour corriger, veuillez reenvoyer un message corrige et commencant par le mot cle "+args['mot_cle']
			if len(args['text'].split(' ')) > 7:
				args['valide'] = False
				args['info_to_contact'] = "Erreur. Vous avez envoye beaucoup de valeurs. Pour corriger, veuillez reenvoyer un message corrige et commencant par le mot cle "+args['mot_cle']
			if len(args['text'].split(' ')) == 7:
				args['valide'] = True
				args['info_to_contact'] = "Le nombre de valeurs envoye est correct"
		else:
			if len(args['text'].split(' ')) < 6:
				args['valide'] = False
				args['info_to_contact'] = "Erreur. Vous avez envoye peu de valeurs. Pour corriger, veuillez reenvoyer un message corrige et commencant par le mot cle "+args['mot_cle']
			if len(args['text'].split(' ')) > 6:
				args['valide'] = False
				args['info_to_contact'] = "Erreur. Vous avez envoye beaucoup de valeurs. Pour corriger, veuillez reenvoyer un message corrige et commencant par le mot cle "+args['mot_cle']
			if len(args['text'].split(' ')) == 6:
				args['valide'] = True
				args['info_to_contact'] = "Le nombre de valeurs envoye est correct"



def check_if_is_reporter(args):
	''' This function checks if the contact who sent the current message is a reporter '''
	concerned_reporter = Reporter.objects.filter(phone_number = args['phone'])
	if len(concerned_reporter) < 1:
		#This person is not in the list of reporters
		args['valide'] = False
		args['info_to_contact'] = "Erreur. Vous ne vous etes pas enregistre pour pouvoir donner des rapports. Veuillez vous enregistrer en envoyant le message d enregistrement commencant par REG"
		return 

	one_concerned_reporter = concerned_reporter[0]

	if not one_concerned_reporter.facility:
		#The CDS of this reporter is not known
		args['valide'] = False
		args['info_to_contact'] = "Exception. Votre site n est pas enregistre dans le systeme. Veuillez contacter l administrateur du systeme"
		return

	args['the_sender'] =  one_concerned_reporter
	args['facility'] = one_concerned_reporter.facility
	args['valide'] = True
	args['info_to_contact'] = " Le bureau d affectation de ce rapporteur est connu "



def check_date_is_valid(args):
	''' This function checks if a given date is valid '''
	given_date = ""

	#Let's put the value to check in 'given_date' variable
	if(args['message_type']=='STOCK_RECU' or args['message_type']=='STOCK_SORTI' or args['message_type']=='BALANCE' or args['message_type']=='ADMISSION' or args['message_type']=='SORTI' or args['message_type']=='STOCK_RECU_M' or args['message_type']=='STOCK_SORTI_M' or args['message_type']=='BALANCE_M' or args['message_type']=='ADMISSION_M' or args['message_type']=='SORTI_M'):
		given_date = args['text'].split(' ')[1]

	print("------------------given_date-------------------")
	print(given_date)
 
	if not given_date:
		args['valide'] = False
		args['info_to_contact'] = "Exception. Pas de date trouvee pour la verification."
		return

	#expression = r'^((0[1-9])|([1-2][0-9])|(3[01]))-((0[1-9])|(1[0-2]))-[0-9]{4}$'
	expression = r'^((0[1-9])|([1-2][0-9])|(3[01]))((0[1-9])|(1[0-2]))[0-9]{2}$'
	if re.search(expression, given_date) is None:
		args['valide'] = False
		args['info_to_contact'] = "Erreur. La date indiquee n est pas valide. Verifier si vous avez mis chaque valeur dans sa place. Pour corriger, reenvoyez un message commencant par "+args['mot_cle']
		return


	sent_date = given_date[0:2]+"-"+given_date[2:4]+"-20"+given_date[4:]

	sent_date_without_dash = sent_date.replace("-","")
	try:
		date_sent = datetime.datetime.strptime(sent_date_without_dash, "%d%m%Y").date()
	except:
		args['valide'] = False
		args['info_to_contact'] = "Erreur. La date indiquee n est pas valide. Verifier si vous avez mis chaque valeur dans sa place. Pour corriger, reenvoyez un message commencant par "+args['mot_cle']
		return

	args['sent_date'] =  date_sent

	if date_sent > datetime.datetime.now().date():
		#The reporter can not report for a future date
		args['valide'] = False
		args['info_to_contact'] = "Erreur. La date indiquee n est pas encore arrivee. Pour corriger, veuillez reenvoyer un message corrige et commencant par le mot cle "+args['mot_cle']
		return


def check_date_is_monday(args):
	''' This function checks if the given date is for the first day of a week '''
	given_date = ""

	#Let's put the value to check in 'given_date' variable
		
	if(args['message_type']=='STOCK_RECU'):
		given_date = args['text'].split(' ')[1]
	if(args['message_type']=='STOCK_SORTI'):
		given_date = args['text'].split(' ')[1]
	if(args['message_type']=='BALANCE'):
		given_date = args['text'].split(' ')[1]
	if(args['message_type']=='ADMISSION'):
		given_date = args['text'].split(' ')[1]
	if(args['message_type']=='SORTI'):
		given_date = args['text'].split(' ')[1]


	if(args['message_type']=='BALANCE_M'):
		given_date = args['text'].split(' ')[1]
	if(args['message_type']=='ADMISSION_M'):
		given_date = args['text'].split(' ')[1]
	if(args['message_type']=='SORTI_M'):
		given_date = args['text'].split(' ')[1]
 
	if not given_date:
		args['valide'] = False
		args['info_to_contact'] = "Exception. Pas de date trouvee pour la verification."
		return


	sent_date = given_date[0:2]+"-"+given_date[2:4]+"-20"+given_date[4:]

	sent_date_without_dash = sent_date.replace("-","")
	date_sent = ""
	try:
		date_sent = datetime.datetime.strptime(sent_date_without_dash, "%d%m%Y").date()
	except:
		args['valide'] = False
		args['info_to_contact'] = "Erreur. La date indiquee n est pas valide. Verifier si vous avez mis chaque valeur dans sa place. Pour corriger, reenvoyez un message commencant par "+args['mot_cle']
		return
	
	the_day = date_sent.weekday()

	if the_day == 0:
		args['valide'] = True
		args['info_to_contact'] = "La date envoyee est pour lundi"
	else:
		args['valide'] = False
		args['info_to_contact'] = "Erreur. La date envoyee n est pas pour lundi. Pour corriger, reenvoyez un message corrige et commencant par le mot cle "+args['mot_cle']

def check_is_float(args):
	''' This function checks if a given value is a float '''

	expression = r'^([0-9]+.[0-9]+)$|^([0-9]+)$|^([0-9]+,[0-9]+)$'

	value_to_check = args['value_to_check']

	if re.search(expression, value_to_check) is None:
		args['valide'] = False
		args['info_to_contact'] = "Erreur. La valeur envoyee en position "+str(args['position'])+" n est pas valide. Pour corriger,  reenvoyez un message corrige et commencant par le mot cle "+args['mot_cle']
	else:
		args['remaining_quantity'] = value_to_check
		args['valide'] = True
		args['info_to_contact'] = "La valeur envoyee en position "+str(args['position'])+" est valide."

	
	




def check_is_int(args):
	''' This function checks if a given value is an int '''

	expression = r'^[0-9]+$'
	
	value_to_check = args['value_to_check']

	if re.search(expression, value_to_check) is None:
		args['valide'] = False
		args['info_to_contact'] = "Erreur. La valeur envoyee en position "+str(args['position'])+" n est pas valide. Pour corriger,  reenvoyez un message corrige et commencant par le mot cle "+args['mot_cle']
	else:
		args['valide'] = True
		args['info_to_contact'] = "La valeur envoyee en position "+str(args['position'])+" est valide."
	 


def check_facility_code_is_valid(args):
	''' This function checks if the value contained in args['facility_code'] is a facility code and not the facility of the reporter'''
	facilities = Facility.objects.filter(id_facility = args['facility_code'])
	if len(facilities) < 1:
		args['valide'] = False
		#args['info_to_contact'] = "Erreur. Le code envoye en position "+str(args['position'])+" n est pas enregistre dans le systeme."
		args['info_to_contact'] = "Erreur. Le code du site que vous venez d envoyer n est pas enregistre dans le systeme. Pour corriger,  reenvoyez un message corrige et commencant par le mot cle "+args['mot_cle']
	else:
		args['valide'] = True
		args['info_to_contact'] = "Le code envoye existe dans le systeme."
		
		args['destination_facility'] = facilities[0]

		#Let's check if the facility code is not the code of the facility of the contact who is reporting
		
		if(args['facility'].id_facility == args['facility_code']):
			args['valide'] = False
			args['info_to_contact'] = "Erreur. Vous avez mis le code de l etablissement sur lequel vous etes affectes. Pour corriger,  reenvoyez un message corrige et commencant par le mot cle "+args['mot_cle']
		else:
			args['valide'] = True
			args['info_to_contact'] = "Le code mis est valide."


def check_is_product_name(args):
	''' This function checks if the value in args['product_name'] is a product name '''
	products = Product.objects.all()
	product_names = []

	if len(products) < 1:
		args['valide'] = False
		args['info_to_contact'] = "Exception. Aucun produit n est enregistre dans le systeme. Veuillez contacter l administrateur du systeme"
	else:
		#Let's store all product names in a list. We put those names in capital letters
		for product in products:
			product_names.append(product.designation.upper())

	sent_name = args['product_name'].upper()

	if sent_name not in product_names:
		args['valide'] = False
		args['info_to_contact'] = "Erreur. Le nom du produit envoye n est pas valide. Pour corriger, reenvoyez un message corrige et commencant par le mot cle "+args['mot_cle']
	else:
		args['sent_name'] = sent_name
		args['valide'] = True
		args['info_to_contact'] = "Le nom du produit envoye a ete reconnu par le systeme."

def check_values_validity(args):
	''' This function checks if values sent are valid '''
	

	if(args['message_type']=='RUPTURE' or args['message_type']=='RUPTURE_M'):
		#Let's check if the value in the position number 1 is a product name
		args['product_name'] =  args['text'].split(' ')[1]
		args['position'] = 1
		check_is_product_name(args)
		if not args['valide']:
			return
		#Let's check if the value in the position number 2 is a float
		args['value_to_check'] =  args['text'].split(' ')[2]
		args['position'] = 2
		check_is_float(args)
		if not args['valide']:
			return
 
	

	if(args['message_type']=='ADMISSION' or args['message_type']=='ADMISSION_M'):
		#Let's check if the value in the position number 1 is a date
		args['value_to_check'] =  args['text'].split(' ')[1]
		args['position'] = 1
		check_date_is_valid(args)
		if not args['valide']:
			return
		#Let's check if the value in the position number 1 is a date of monday
		args['value_to_check'] =  args['text'].split(' ')[1]
		args['position'] = 1
		check_date_is_monday(args)
		if not args['valide']:
			return
		#Let's check if the value in the position number 2 is an int
		args['value_to_check'] =  args['text'].split(' ')[2]
		args['position'] = 2		
		check_is_int(args)
		if not args['valide']:
			return
		#Let's check if the value in the position number 3 is an int
		args['value_to_check'] =  args['text'].split(' ')[3]
		args['position'] = 3
		check_is_int(args)
		if not args['valide']:
			return
		#Let's check if the value in the position number 4 is an int
		args['value_to_check'] =  args['text'].split(' ')[4]
		args['position'] = 4
		check_is_int(args)
		if not args['valide']:
			return
		#Let's check if the value in the position number 5 is an int
		args['value_to_check'] =  args['text'].split(' ')[5]
		args['position'] = 5
		check_is_int(args)
		if not args['valide']:
			return
		#Let's check if the value in the position number 6 is an int
		args['value_to_check'] =  args['text'].split(' ')[6]
		args['position'] = 6
		check_is_int(args)
		if not args['valide']:
			return
		#Let's check if the value in the position number 6 is an int
		args['value_to_check'] =  args['text'].split(' ')[7]
		args['position'] = 7
		check_is_int(args)
		if not args['valide']:
			return


	if(args['message_type']=='SORTI' or args['message_type']=='SORTI_M'):
		#Let's check if the value in the position number 1 is a date
		args['value_to_check'] =  args['text'].split(' ')[1]
		args['position'] = 1
		check_date_is_valid(args)
		if not args['valide']:
			return
		#Let's check if the value in the position number 1 is a date of monday
		args['value_to_check'] =  args['text'].split(' ')[1]
		args['position'] = 1
		check_date_is_monday(args)
		if not args['valide']:
			return
		#Let's check if the value in the position number 2 is an int
		args['value_to_check'] =  args['text'].split(' ')[2]
		args['position'] = 2		
		check_is_int(args)
		if not args['valide']:
			return
		#Let's check if the value in the position number 3 is an int
		args['value_to_check'] =  args['text'].split(' ')[3]
		args['position'] = 3
		check_is_int(args)
		if not args['valide']:
			return
		#Let's check if the value in the position number 4 is an int
		args['value_to_check'] =  args['text'].split(' ')[4]
		args['position'] = 4
		check_is_int(args)
		if not args['valide']:
			return
		#Let's check if the value in the position number 5 is an int
		args['value_to_check'] =  args['text'].split(' ')[5]
		args['position'] = 5
		check_is_int(args)
		if not args['valide']:
			return

		if args['facility'].facility_level == 'CDS':
			#Let's check if the value in the position number 6 is an int
			args['value_to_check'] =  args['text'].split(' ')[6]
			args['position'] = 6
			check_is_int(args)
		

'''
def check_products_reports_values_validity(args):
	#This function checks if values sent for products quantities are valid

	
	#The value at the indice 1 is always a date. Let's check if it is valide
	if(args['message_type']=='STOCK_RECU' or args['message_type']=='STOCK_RECU_M' or args['message_type']=='STOCK_SORTI' or args['message_type']=='STOCK_SORTI_M' or args['message_type']=='BALANCE' or args['message_type']=='BALANCE_M'):
		#Let's check if the value in the position number 1 is a date
		args['value_to_check'] =  args['text'].split(' ')[1]
		args['position'] = 1
		check_date_is_valid(args)
		if not args['valide']:
			return
		if(args['message_type']=='BALANCE' or args['message_type']=='BALANCE_M'):
			args['position'] = 1
			check_date_is_monday(args)
			if not args['valide']:
				return

	#For the stock sent from one site to an other, let's check if the given site code is valide
	if(args['message_type']=='STOCK_SORTI' or args['message_type']=='STOCK_SORTI_M'):
		args['facility_code'] =  args['text'].split(' ')[2]
		args['position'] = 2		
		check_facility_code_is_valid(args)
		if not args['valide']:
			return


	number_of_active_products = args['number_of_active_products']

	
	#Let's check if products priorities starts from 1 to the end without skip any number
	#If we identify a value which is not correct, we will put false in ok variable
	ok = True
	priority = 1

	while(priority <= number_of_active_products and ok == True):
		concerned_product = Product.objects.filter(is_in_use = True, priorite_dans_sms = priority)
		if(len(concerned_product) < 1):
			args['valide'] = False
			args['info_to_contact'] = "Exception. Pas de produit de priorite '"+priority+"' active. Veuillez contacter l administrateur de ce systeme"
			ok = False
		priority = priority + 1

	if (ok == False):
		return


	
	#Let's identify if numbers are correct
	if(args['message_type']=='STOCK_RECU' or args['message_type']=='STOCK_RECU_M' or args['message_type']=='BALANCE' or args['message_type']=='BALANCE_M'):
		#Products values starts at the indice 2
		print("#Products values starts at the indice 2")
		first_product_indice = 2

	if(args['message_type']=='STOCK_SORTI' or args['message_type']=='STOCK_SORTI_M'):
		#Products values starts at the indice 3
		print("#Products values starts at the indice 3")
		first_product_indice = 3

	ok = True
	priority = 1
	indice = first_product_indice

	while(priority <= number_of_active_products and ok == True):
		args['value_to_check'] =  args['text'].split(' ')[indice]
		args['position'] = indice

		print("------------INDICE----------")
		print(indice)
		
		product = Product.objects.filter(is_in_use = True, priorite_dans_sms = priority)[0]
		
		if(product.can_be_fractioned == True):
			#This value can be fractioned
			check_is_float(args)
		else:
			#This value can not be fractioned
			check_is_int(args)

		if(args['valide'] == False):
			ok = False
			args['valide'] = False
			args['info_to_contact'] = "Erreur. La valeur envoyee pour le produit '"+product.designation+"' n est pas valide. Pour corriger, reenvoyez un message corrige et commencant par le mot cle "+args['mot_cle']
		
		priority = priority + 1
		indice = indice + 1
#======================reporters self registration==================================
'''

def check_facility(args):
	''' This function checks if the facility code sent by the reporter exists '''
	the_facility_code = args['text'].split(' ')[1]
	concerned_facility = Facility.objects.filter(id_facility = the_facility_code)
	if (len(concerned_facility) > 0):
		args['valide'] = True
		args['info_to_contact'] = "Le code (STA ou SST ou ...) envoye est reconnu."
	else:
		args['valide'] = False
		args['info_to_contact'] = "Erreur. Le code envoye n est pas associe a un site. Pour corriger, reenvoyez un message corrige et commencant par le mot cle "+args['mot_cle']

def check_supervisor_phone_number(args):
	''' This function checks if the phone number of the supervisor is well written '''
	the_supervisor_phone_number = args['text'].split(' ')[2]
	the_supervisor_phone_number_no_space = the_supervisor_phone_number.replace(" ", "")
	expression = r'^(\+?(257)?)((62)|(79)|(71)|(76))([0-9]{6})$'
	print(the_supervisor_phone_number_no_space)
	if re.search(expression, the_supervisor_phone_number_no_space) is None:
		#The phone number is not well written
		args['valide'] = False
		args['info_to_contact'] = "Erreur. Le numero de telephone du superviseur n est pas bien ecrit. Pour corriger, veuillez reenvoyer un message corrige et commencant par le mot cle REG"
	else:
		args['valide'] = True
		args['info_to_contact'] = "Le numero de telephone du superviseur est bien ecrit."



def save_temporary_the_reporter(args):
	same_existing_temp = Temporary.objects.filter(phone_number = args['phone'])
	if len(same_existing_temp) > 0:
		same_existing_temp = same_existing_temp[0]
		same_existing_temp.delete()
		args['valide'] = False
		args['info_to_contact'] = "Vous devriez envoyer le numero de telephone de votre superviseur seulement. Recommencer par RG ..."
	else:
		the_phone_number = args['phone']

		the_facility_code = args['text'].split(' ')[1]

		facility = Facility.objects.filter(id_facility = the_facility_code)
		if len(facility) > 0:
			the_concerned_facility = facility[0]

			the_supervisor_phone_number = args['text'].split(' ')[2]
			the_supervisor_phone_number_no_space = the_supervisor_phone_number.replace(" ", "")

			if len(the_supervisor_phone_number_no_space) == 8:
				the_supervisor_phone_number_no_space = "+257"+the_supervisor_phone_number_no_space
			if len(the_supervisor_phone_number_no_space) == 11:
				the_supervisor_phone_number_no_space = "+"+the_supervisor_phone_number_no_space

			Temporary.objects.create(phone_number = the_phone_number, facility = the_concerned_facility, supervisor_phone_number = the_supervisor_phone_number_no_space)
			args['valide'] = True
			args['info_to_contact'] = "Veuillez reenvoyer seulement le numero de telephone de votre superviseur s il vous plait."


def check_has_already_session(args):
	'''This function checks if this contact has a session'''
	same_existing_temp = Temporary.objects.filter(phone_number = args['phone'])
	if len(same_existing_temp) > 0:
		same_existing_temp = same_existing_temp[0]
		same_existing_temp.delete()
		args['valide'] = False
		args['info_to_contact'] = "Vous devriez envoyer le numero de telephone de votre superviseur seulement."
	else:
		args['valide'] = True
		args['info_to_contact'] = "Ok."

def temporary_record_reporter(args):
	'''This function is used to record temporary a reporter'''
	
	if(args['text'].split(' ')[0].upper() == 'REG'):
		args['mot_cle'] = 'REG'
		
		#Because REG is used to do the self registration and not the update, if the phone user sends a message starting with REG and 			#he/she is already a reporter, we don't allow him/her to continue
		check_if_is_reporter(args)
		if(args['valide'] == True):
			#This contact is already a reporter and can't do the registration the second time
			args['info_to_contact'] = "Erreur. Vous vous etes deja enregistre. Si vous voulez modifier votre site d affectation ou le numero de telephone de votre superviseur, envoyer le message commencant par le mot cle 'REGM'"
			return
	
	if(args['text'].split(' ')[0].upper() == 'REGM'):
		args['mot_cle'] = 'REGM'

	#Let's check if this contact has an existing session
	check_has_already_session(args)
	if not args['valide']:
		return



	#Let's check if the message sent is composed by an expected number of values
	check_number_of_values(args)
	if not args['valide']:
		return



	#Let's check if the code of STA or SST ... is valid
	check_facility(args)
	if not args['valide']:
		return



	#Let's check is the supervisor phone number is valid
	check_supervisor_phone_number(args)
	if not args['valide']:
		return

	#La ligne ci dessous ne peut pas fonctionner sur les instance Anonimise de RapidPro
	#Let's check if the contact didn't send his/her number in the place of the supervisor number
	#check_supervisor_phone_number_not_for_this_contact(args)
	#if not args['valide']:
		#return

	#Let's temporary save the reporter
	save_temporary_the_reporter(args)


def complete_registration(args):
	the_sup_phone_number = args['text']
	the_sup_phone_number_without_spaces = the_sup_phone_number.replace(" ", "")

	the_existing_temp = Temporary.objects.filter(phone_number = args['phone'])

	if len(the_existing_temp) < 1:
		args['valide'] = False
		args['info_to_contact'] = "Votre message n est pas considere."
	else:
		the_one_existing_temp = the_existing_temp[0]


		#if (the_one_existing_temp.supervisor_phone_number == the_sup_phone_number_without_spaces):
		if (the_sup_phone_number_without_spaces in the_one_existing_temp.supervisor_phone_number) and (len(the_sup_phone_number_without_spaces) >= 8):
			#The confirmation of the phone number of the supervisor pass


			#Let's check if this contact is not registered with this CDS and this supervisor Phone number
			#If it is the case, this contact is doing an unnecessary registration
			check_duplication = Reporter.objects.filter(phone_number = the_one_existing_temp.phone_number, facility = the_one_existing_temp.facility, supervisor_phone_number = the_one_existing_temp.supervisor_phone_number)
			if len(check_duplication) > 0:
				#Already registered and nothing to update
				args['valide'] = False
				args['info_to_contact'] = "Erreur. Vous vous etes deja enregistre sur ce site et avec ce numero de telephone du superviseur. Envoyer un message bien ecrit et commencant par un mot cle valide ou X pour fermer la session"
				the_one_existing_temp.delete()
				return

			check_duplication = ''


			#Let's check if the contact wants to update his facility
			check_duplication = Reporter.objects.filter(~Q(facility = the_one_existing_temp.facility), phone_number = the_one_existing_temp.phone_number, supervisor_phone_number = the_one_existing_temp.supervisor_phone_number)
			if len(check_duplication) > 0:
				#this contact wants to update his facility
				check_duplication = check_duplication[0]
				check_duplication.facility = the_one_existing_temp.facility
				check_duplication.save()
				args['valide'] = True
				args['info_to_contact'] = "Modification reussie. Votre nouveau site d affectation est : "+the_one_existing_temp.facility.name
				the_one_existing_temp.delete()
				return

			check_duplication = ''



			#Let's check if the contact wants to update the phone number of his supervisor
			check_duplication = Reporter.objects.filter(~Q(supervisor_phone_number = the_one_existing_temp.supervisor_phone_number), phone_number = the_one_existing_temp.phone_number, facility = the_one_existing_temp.facility)
			if len(check_duplication) > 0:
				#this contact wants to update the phone number of his supervisor
				check_duplication = check_duplication[0]
				check_duplication.supervisor_phone_number = the_one_existing_temp.supervisor_phone_number
				check_duplication.save()
				args['valide'] = True
				args['info_to_contact'] = "Modification reussie. Le nouveau numero de telephone de votre superviseur est : "+the_one_existing_temp.supervisor_phone_number+""
				the_one_existing_temp.delete()
				return

			check_duplication = ''



			#Let's check if the contact wants to update both the CDS and the phone number of his supervisor
			check_duplication = Reporter.objects.filter(~Q(facility = the_one_existing_temp.facility), ~Q(supervisor_phone_number = the_one_existing_temp.supervisor_phone_number), phone_number = the_one_existing_temp.phone_number)
			if len(check_duplication) > 0:
				#this contact wants to update the phone number of his supervisor
				check_duplication = check_duplication[0]
				check_duplication.facility = the_one_existing_temp.facility
				check_duplication.supervisor_phone_number = the_one_existing_temp.supervisor_phone_number
				check_duplication.save()
				args['valide'] = True
				args['info_to_contact'] = "Modification reussie. Le nouveau numero de telephone de votre superviseur est '"+the_one_existing_temp.supervisor_phone_number+"' et votre nouveau site d affectation est '"+the_one_existing_temp.facility.name+"'"
				the_one_existing_temp.delete()
				return


			#This contact is doing a first registration. Let's record him/her
			Reporter.objects.create(phone_number = the_one_existing_temp.phone_number,facility = the_one_existing_temp.facility, supervisor_phone_number = the_one_existing_temp.supervisor_phone_number)
			the_one_existing_temp.delete()
			args['valide'] = True
			args['info_to_contact'] = "Enregistrement reussi. Si vous voulez modifier le code de votre site d affectation ou le numero de telephone de votre superviseur, veuillez utiliser le mot cle REGM"
		else:
			the_one_existing_temp.delete()
			args['valide'] = False
			args['info_to_contact'] = "Erreur. Vous avez envoye le numero de telephone de votre superviseur de differentes manieres. Pour corriger, veuillez reenvoyer le message commencant par le mot cle REG"


#-----------------------------------------------------------------









'''
#-----------------------------STOCK RECEIVED------------------------------------
#RECORD
def record_stock_received(args):
	This function records a report about medicines received

	args['mot_cle'] = 'SRC'

	#Let's check if the message sent is composed by an expected number of values
	check_number_of_values(args)
	print(args['valide'])
	if not args['valide']:
		return

	#Let's check if the person who send this message is a reporter
	check_if_is_reporter(args)
	print(args['valide'])
	if not args['valide']:
		return

	#Let's check if the values sent are valid
	#check_values_validity(args)
	check_products_reports_values_validity(args)
	print(args['valide'])
	if not args['valide']:
		return

	#Let's save the report
	the_created_report = Report.objects.create(facility = args['facility'], reporting_date = datetime.datetime.now().date(), text = args['text'], category = 'STOCK_RECU')


	the_created_reception = Reception.objects.create(report = the_created_report, date_de_reception = args['sent_date'])


	priority = 1

	message_to_send = "Enregistrement reussie. Vous venez de rapporter le stock recu comme suit : "

	while ((priority <= (len(args['text'].split(' ')) - 2)) and (priority > 0)):
		#We record each beneficiary number
		value = args['text'].split(' ')[priority+1]
		value = value.replace(",",".")

		concerned_product = Product.objects.filter(priorite_dans_sms = priority)

		if len(concerned_product) < 1:
			priority = 0
			args['valide'] = False
			args['info_to_contact'] = "Exception. Un produit d une priorite donnee n a pas ete trouve. Veuiller informer l administrateur du systeme."

		the_concerned_product = concerned_product[0]

		if priority == 1:
			message_to_send = message_to_send+""+the_concerned_product.designation+"="+value
		else:
			message_to_send = message_to_send+", "+the_concerned_product.designation+"="+value

		product_reception_record = ProductsReceptionReport.objects.create(reception = the_created_reception, produit = the_concerned_product, quantite_recue = value)

		priority = priority + 1

	args['info_to_contact'] = message_to_send

	second_msg_to_sent = "Si vous voulez corriger ce rapport du stock recu que vous venez d envoyer, envoyer un message corrige et commencant par SRCM"


	#The below code will be uncommented in order to send the second sms after the first one
	
	#the_contact_phone_number = "tel:"+args['the_sender'].phone_number
	#data = {"urns": [the_contact_phone_number],"text": args['info_to_contact']}
	#args['data'] = data
	#send_sms_through_rapidpro(args)

	#args['info_to_contact'] = second_msg_to_sent

'''

'''
#MODIFY
def modify_stock_received(args):
	#This function modifies a report about medicines received

	args['mot_cle'] = 'SRCM'

	#Let's check if the message sent is composed by an expected number of values
	check_number_of_values(args)
	print(args['valide'])
	if not args['valide']:
		return

	#Let's check if the person who send this message is a reporter
	check_if_is_reporter(args)
	print(args['valide'])
	if not args['valide']:
		return

	#Let's check if the values sent are valid
	#check_values_validity(args)
	check_products_reports_values_validity(args)
	print(args['valide'])
	if not args['valide']:
		return

	#======================================>
	#Let's check if this facility sent this kind of report at this date and delete it if there is one
	the_same_reception = Reception.objects.filter(date_de_reception = args['sent_date'], report__facility = args['facility']).order_by('id').reverse()
	if len(the_same_reception) < 1:
		args['valide'] = False
		args['info_to_contact'] = "Erreur. Aucune modification faite car aucun rapport de reception des produits n a ete enregistre avec la date que vous venez d envoyer. Pour corriger, veuillez reenvoyer un message corrige et commencant par le mot cle "+args['mot_cle']
		return

	the_last_same_reception = the_same_reception[0]
	the_related_report = the_last_same_reception.report
	the_related_report.delete()
	#======================================>


	#Let's save the report
	the_created_report = Report.objects.create(facility = args['facility'], reporting_date = datetime.datetime.now().date(), text = args['text'], category = 'STOCK_RECU')


	the_created_reception = Reception.objects.create(report = the_created_report, date_de_reception = args['sent_date'])


	priority = 1

	message_to_send = "Modification reussie. Vous venez de rapporter le stock recu comme suit : "

	while ((priority <= (len(args['text'].split(' ')) - 2)) and (priority > 0)):
		#We record each beneficiary number
		value = args['text'].split(' ')[priority+1]
		value = value.replace(",",".")

		concerned_product = Product.objects.filter(priorite_dans_sms = priority)

		if len(concerned_product) < 1:
			priority = 0
			args['valide'] = False
			args['info_to_contact'] = "Exception. Un produit d une priorite donnee n a pas ete trouve. Veuiller informer l administrateur du systeme."

		the_concerned_product = concerned_product[0]

		if priority == 1:
			message_to_send = message_to_send+""+the_concerned_product.designation+"="+value
		else:
			message_to_send = message_to_send+", "+the_concerned_product.designation+"="+value

		product_reception_record = ProductsReceptionReport.objects.create(reception = the_created_reception, produit = the_concerned_product, quantite_recue = value)

		priority = priority + 1

	args['info_to_contact'] = message_to_send
#--------------------------------------------------------------------------------------
'''






'''
#------------------------------SENT STOCK---------------------------------------
#RECORD
def record_sent_stock(args):
	#This function records a report about medicines sent from one facility to an other
	
	args['mot_cle'] = 'SST'

	#Let's check if the message sent is composed by an expected number of values
	check_number_of_values(args)
	print(args['valide'])
	if not args['valide']:
		return

	#Let's check if the person who send this message is a reporter
	check_if_is_reporter(args)
	print(args['valide'])
	if not args['valide']:
		return

	#Let's check if the values sent are valid
	#check_values_validity(args)
	check_products_reports_values_validity(args)
	print(args['valide'])
	if not args['valide']:
		return

	#Let's save the report
	the_created_report = Report.objects.create(facility = args['facility'], reporting_date = datetime.datetime.now().date(), text = args['text'], category = 'STOCK_SORTI')


	the_created_Sortie = Sortie.objects.create(report = the_created_report, date_de_sortie = args['sent_date'], destination = args['destination_facility'])


	priority = 1

	message_to_send = "Enregistrement reussie. Vous venez de rapporter la sortie des produits vers '"+args['destination_facility'].name+"' comme suit : "

	while ((priority <= (len(args['text'].split(' ')) - 3)) and (priority > 0)):
		#Let's record each product transfered
		value = args['text'].split(' ')[priority+2]
		value = value.replace(",",".")

		concerned_product = Product.objects.filter(priorite_dans_sms = priority)

		if len(concerned_product) < 1:
			priority = 0
			args['valide'] = False
			args['info_to_contact'] = "Exception. Un produit d une priorite donnee n a pas ete trouve. Veuiller informer l administrateur du systeme."
			return

		the_concerned_product = concerned_product[0]

		if priority == 1:
			message_to_send = message_to_send+""+the_concerned_product.designation+"="+value
		else:
			message_to_send = message_to_send+", "+the_concerned_product.designation+"="+value

		product_out_record = ProductsTranferReport.objects.create(sortie = the_created_Sortie, produit = the_concerned_product, quantite_donnee = value)

		priority = priority + 1

	args['info_to_contact'] = message_to_send

	second_msg_to_sent = "Si vous voulez corriger ce rapport du stock sorti que vous venez d envoyer, envoyer un message corrige et commencant par SSTM"



	#The below code will be uncommented in order to send the second sms after the first one
	
	#the_contact_phone_number = "tel:"+args['the_sender'].phone_number
	#data = {"urns": [the_contact_phone_number],"text": args['info_to_contact']}
	#args['data'] = data
	#send_sms_through_rapidpro(args)

	#args['info_to_contact'] = second_msg_to_sent
	
'''

'''
#MODIFY
def modify_sent_stock(args):
	#This function records a report about medicines sent from one facility to an other

	args['mot_cle'] = 'SSTM'

	#Let's check if the message sent is composed by an expected number of values
	check_number_of_values(args)
	print(args['valide'])
	if not args['valide']:
		return

	#Let's check if the person who send this message is a reporter
	check_if_is_reporter(args)
	print(args['valide'])
	if not args['valide']:
		return

	#Let's check if the values sent are valid
	#check_values_validity(args)
	check_products_reports_values_validity(args)
	print(args['valide'])
	if not args['valide']:
		return


	#======================================>
	#Let's check if this facility sent this kind of report at this date and delete it if there is one
	the_same_out_report = Sortie.objects.filter(date_de_sortie = args['sent_date'], destination = args['destination_facility'], report__facility = args['facility']).order_by('id').reverse()
	if len(the_same_out_report) < 1:
		args['valide'] = False
		args['info_to_contact'] = "Erreur. Aucune modification faite car aucun rapport de sortie des produits n a ete enregistre avec la date et la destination que vous venez d envoyer. Pour corriger, veuillez reenvoyer un message corrige et commencant par le mot cle "+args['mot_cle']
		return

	the_last_same_out_report = the_same_out_report[0]
	the_related_report = the_last_same_out_report.report
	the_related_report.delete()
	#======================================>


	#Let's save the report
	the_created_report = Report.objects.create(facility = args['facility'], reporting_date = datetime.datetime.now().date(), text = args['text'], category = 'STOCK_SORTI')


	the_created_Sortie = Sortie.objects.create(report = the_created_report, date_de_sortie = args['sent_date'], destination = args['destination_facility'])


	priority = 1

	message_to_send = "Modification reussie. Vous venez de rapporter la sortie des produits vers '"+args['destination_facility'].name+"' comme suit : "

	while ((priority <= (len(args['text'].split(' ')) - 3)) and (priority > 0)):
		#We record each beneficiary number
		value = args['text'].split(' ')[priority+2]
		value = value.replace(",",".")

		concerned_product = Product.objects.filter(priorite_dans_sms = priority)

		if len(concerned_product) < 1:
			priority = 0
			args['valide'] = False
			args['info_to_contact'] = "Exception. Un produit d une priorite donnee n a pas ete trouve. Veuiller informer l administrateur du systeme."

		the_concerned_product = concerned_product[0]

		if priority == 1:
			message_to_send = message_to_send+""+the_concerned_product.designation+"="+value
		else:
			message_to_send = message_to_send+", "+the_concerned_product.designation+"="+value

		product_out_record = ProductsTranferReport.objects.create(sortie = the_created_Sortie, produit = the_concerned_product, quantite_donnee = value)

		priority = priority + 1

	args['info_to_contact'] = message_to_send
#--------------------------------------------------------------------------------------
'''





'''
#-------------------------------A STOCK OUT------------------------------------
#RECORD
def record_stock_out(args):
	#This function records a report about a stock out of a medicine

	args['mot_cle'] = 'RUP'

	#Let's check if the message sent is composed by an expected number of values
	check_number_of_values(args)
	print(args['valide'])
	if not args['valide']:
		return

	#Let's check if the person who send this message is a reporter
	check_if_is_reporter(args)
	print(args['valide'])
	if not args['valide']:
		return

	#Let's check if the values sent are valid
	check_values_validity(args)
	print(args['valide'])
	if not args['valide']:
		return

	#Let's save the report
	the_created_report = Report.objects.create(facility = args['facility'], reporting_date = datetime.datetime.now().date(), text = args['text'], category = 'RUPTURE')


	#Let's identify the concerned product
	the_concerned_product = Product.objects.filter(designation = args['sent_name'])

	if len(the_concerned_product) < 1:
		args['valide'] = False
		args['info_to_contact'] = "Exception. Un produit du nom donnee non trouve."
		return

	the_concerned_product = the_concerned_product[0]

	product_out_of_stock = StockOutReport.objects.create(report = the_created_report, produit = the_concerned_product, quantite_restante = args['remaining_quantity'])

	args['info_to_contact'] = "Enregistrement reussie. Vous venez de rapporter une rupture du stock pour le produit '"+the_concerned_product.designation+"'. La quantite restante est "+args['remaining_quantity']+"."
	
	#The below message message will be sent to the supervisor
	args['info_to_supervisor'] = "Une rupture du stock pour le produit '"+the_concerned_product.designation+"' est signalee au site '"+args['facility'].name+"'. La quantite restante est "+args['remaining_quantity']+"."

	second_msg_to_sent = "Si vous voulez corriger ce rapport de rupture du stock que vous venez d envoyer, envoyer un message corrige et commencant par RUPM"



	#The below code will be uncommented in order to send the second sms after the first one
	
	#the_contact_phone_number = "tel:"+args['the_sender'].phone_number
	#data = {"urns": [the_contact_phone_number],"text": args['info_to_contact']}
	#args['data'] = data
	#send_sms_through_rapidpro(args)

	#args['info_to_contact'] = second_msg_to_sent
'''	

'''
#MODIFY
def modify_stock_out(args):
	#This function modifies a report about a stock out of a medicine

	args['mot_cle'] = 'RUPM'

	#Let's check if the message sent is composed by an expected number of values
	check_number_of_values(args)
	print(args['valide'])
	if not args['valide']:
		return

	#Let's check if the person who send this message is a reporter
	check_if_is_reporter(args)
	print(args['valide'])
	if not args['valide']:
		return

	#Let's check if the values sent are valid
	check_values_validity(args)
	print(args['valide'])
	if not args['valide']:
		return

	#Let's identify the concerned product
	the_concerned_product = Product.objects.filter(designation = args['sent_name'])

	if len(the_concerned_product) < 1:
		args['valide'] = False
		args['info_to_contact'] = "Exception. Un produit du nom donnee non trouve."
		return

	the_concerned_product = the_concerned_product[0]

	#======================================>
	#Let's check if this facility sent this kind of report at this date and delete it if there is one
	the_same_stock_out_report = StockOutReport.objects.filter(report__facility = args['facility']).order_by('id').reverse()
	if len(the_same_stock_out_report) < 1:
		args['valide'] = False
		args['info_to_contact'] = "Erreur. Aucune modification faite car aucun rapport de rupture de stock n a ete enregistre par votre site."
		return

	the_last_same_stock_out_report = the_same_stock_out_report[0]
	the_related_report = the_last_same_stock_out_report.report
	the_related_report.delete()
	#======================================>


	#Let's save the report
	the_created_report = Report.objects.create(facility = args['facility'], reporting_date = datetime.datetime.now().date(), text = args['text'], category = 'RUPTURE')


	product_out_of_stock = StockOutReport.objects.create(report = the_created_report, produit = the_concerned_product, quantite_restante = args['remaining_quantity'])

	args['info_to_contact'] = "Modification reussie. Vous venez de rapporter une rupture du stock pour le produit '"+the_concerned_product.designation+"'. La quantite restante est "+args['remaining_quantity']+"."

	args['info_to_supervisor'] = "Modification. Une rupture de stock est signalee au site '"+args['facility'].name+"' pour le produit "+the_concerned_product.designation+". La quantite restante est "+args['remaining_quantity']
#-------------------------------------------------------------------------------------
'''





'''
#--------------------------------CURRENT STOCK----------------------------------
#RECORD
def record_current_stock(args):
	#This function records a report about current quantities of medicines

	args['mot_cle'] = 'BAL'

	#Let's check if the message sent is composed by an expected number of values
	check_number_of_values(args)
	print(args['valide'])
	if not args['valide']:
		return

	#Let's check if the person who send this message is a reporter
	check_if_is_reporter(args)
	print(args['valide'])
	if not args['valide']:
		return

	#Let's check if the values sent are valid
	#check_values_validity(args)
	check_products_reports_values_validity(args)
	print(args['valide'])
	if not args['valide']:
		return

	#Let's check if this facility have not finished to give this report
	the_existing_same_report = StockReport.objects.filter(date_of_first_week_day = args['sent_date'], report__facility = args['facility'])
	if len(the_existing_same_report) > 0:
		args['valide'] = False
		args['info_to_contact'] = "Erreur. Un rapport pour cette semaine avez ete enregistre. Pour le modifier, veuillez envoyer un message de modification commencant par le mot cle "+args['mot_cle']+"M"
		return

	#Let's save the report
	the_created_report = Report.objects.create(facility = args['facility'], reporting_date = datetime.datetime.now().date(), text = args['text'], category = 'BALANCE')


	the_created_stock_report = StockReport.objects.create(report = the_created_report, date_of_first_week_day = args['sent_date'])


	priority = 1

	message_to_send = "Enregistrement reussie. Vous venez de rapporter l etat du stock comme suit : "

	while ((priority <= (len(args['text'].split(' ')) - 2)) and (priority > 0)):
		#We record each beneficiary number
		value = args['text'].split(' ')[priority+1]
		value = value.replace(",",".")

		concerned_product = Product.objects.filter(priorite_dans_sms = priority)

		if len(concerned_product) < 1:
			priority = 0
			args['valide'] = False
			args['info_to_contact'] = "Exception. Un produit d une priorite donnee n a pas ete trouve. Veuiller informer l administrateur du systeme."

		the_concerned_product = concerned_product[0]

		if priority == 1:
			message_to_send = message_to_send+""+the_concerned_product.designation+" : "+value
		else:
			message_to_send = message_to_send+", "+the_concerned_product.designation+" : "+value

		product_stock_record = ProductStockReport.objects.create(stock_report = the_created_stock_report, product = the_concerned_product, quantite_en_stock = value)

		priority = priority + 1

	args['info_to_contact'] = message_to_send

	second_msg_to_sent = "Si vous voulez corriger ce rapport de l etat du stock que vous venez d envoyer, envoyer un message corrige et commencant par BALM"


	#The below code will be uncommented in order to send the second sms after the first one
	
	#the_contact_phone_number = "tel:"+args['the_sender'].phone_number
	#data = {"urns": [the_contact_phone_number],"text": args['info_to_contact']}
	#args['data'] = data
	#send_sms_through_rapidpro(args)

	#args['info_to_contact'] = second_msg_to_sent
'''

'''
#MODIFY
def modify_current_stock(args):
	#This function modifies a report about current quantities of medicines

	args['mot_cle'] = 'BALM'

	#Let's check if the message sent is composed by an expected number of values
	check_number_of_values(args)
	print(args['valide'])
	if not args['valide']:
		return

	#Let's check if the person who send this message is a reporter
	check_if_is_reporter(args)
	print(args['valide'])
	if not args['valide']:
		return

	#Let's check if the values sent are valid
	#check_values_validity(args)
	check_products_reports_values_validity(args)
	print(args['valide'])
	if not args['valide']:
		return

	#Let's check if this facility have finished to give this report
	the_existing_same_report = StockReport.objects.filter(date_of_first_week_day = args['sent_date'], report__facility = args['facility'])
	if len(the_existing_same_report) < 1:
		args['valide'] = False
		args['info_to_contact'] = "Erreur. Aucune modification faite car aucun rapport sur la situation du stock n avez ete donne par votre site avec la date que vous venez d envoyer."
		return

	#If that site have finished to give this report, let s delete it and create the new one
	the_one_existing_same_report = the_existing_same_report[0]
	the_related_report = the_one_existing_same_report.report
	the_related_report.delete()

	#Let's save the new report
	the_created_report = Report.objects.create(facility = args['facility'], reporting_date = datetime.datetime.now().date(), text = args['text'], category = 'BALANCE')


	the_created_stock_report = StockReport.objects.create(report = the_created_report, date_of_first_week_day = args['sent_date'])


	priority = 1

	message_to_send = "Modification reussie. Vous venez de rapporter l etat du stock comme suit : "

	while ((priority <= (len(args['text'].split(' ')) - 2)) and (priority > 0)):
		#We record each beneficiary number
		value = args['text'].split(' ')[priority+1]
		value = value.replace(",",".")

		concerned_product = Product.objects.filter(priorite_dans_sms = priority)

		if len(concerned_product) < 1:
			priority = 0
			args['valide'] = False
			args['info_to_contact'] = "Exception. Un produit d une priorite donnee n a pas ete trouve. Veuiller informer l administrateur du systeme."

		the_concerned_product = concerned_product[0]

		if priority == 1:
			message_to_send = message_to_send+""+the_concerned_product.designation+"="+value
		else:
			message_to_send = message_to_send+", "+the_concerned_product.designation+"="+value

		product_stock_record = ProductStockReport.objects.create(stock_report = the_created_stock_report, product = the_concerned_product, quantite_en_stock = value)

		priority = priority + 1

	args['info_to_contact'] = message_to_send
#--------------------------------------------------------------------------------------
'''





'''
#---------------------------------NUMBERS OF PATIENTS SERVED--------------------
#RECORD
def record_patient_served(args):
	#This function records a report about number of patient served in a given week

	args['mot_cle'] = 'ADM'

	#Let's check if the message sent is composed by an expected number of values
	check_number_of_values(args)
	print(args['valide'])
	if not args['valide']:
		return

	#Let's check if the person who send this message is a reporter
	check_if_is_reporter(args)
	print(args['valide'])
	if not args['valide']:
		return

	#Let's check if the values sent are valid
	check_values_validity(args)
	print(args['valide'])
	if not args['valide']:
		return

	#Let's check if this facility have not finished to give this report
	the_existing_same_report = IncomingPatientsReport.objects.filter(date_of_first_week_day = args['sent_date'], report__facility = args['facility'])
	if len(the_existing_same_report) > 0:
		args['valide'] = False
		args['info_to_contact'] = "Erreur. Un rapport pour cette semaine avez ete enregistre. Pour le modifier, veuillez envoyer un message de modification commencant par le mot cle "+args['mot_cle']+"M"
		return
	
	#Let's save the report
	the_created_report = Report.objects.create(facility = args['facility'], reporting_date = datetime.datetime.now().date(), text = args['text'], category = 'ADMISSION')


	incoming_patients_report = IncomingPatientsReport.objects.create(report = the_created_report, total_debut_semaine = args['text'].split(' ')[2], ptb = args['text'].split(' ')[3], oedemes = args['text'].split(' ')[4], rechute = args['text'].split(' ')[5], readmission = args['text'].split(' ')[6], transfert_interne = args['text'].split(' ')[7], date_of_first_week_day = args['sent_date'])

	args['info_to_contact'] = "Enregistrement reussie. Vous venez de rapporter les admissions comme suit : TDS="+args['text'].split(' ')[2]+", PTB="+args['text'].split(' ')[3]+", Oedemes="+args['text'].split(' ')[4]+", Rechute="+args['text'].split(' ')[5]+", Readmission="+args['text'].split(' ')[6]+", TI="+args['text'].split(' ')[7]+""


	second_msg_to_sent = "Si vous voulez corriger ce rapport des admissions que vous venez d envoyer, envoyer un message corrige et commencant par ADMM"



	#The below code will be uncommented in order to send the second sms after the first one
	
	#the_contact_phone_number = "tel:"+args['the_sender'].phone_number
	#data = {"urns": [the_contact_phone_number],"text": args['info_to_contact']}
	#args['data'] = data
	#send_sms_through_rapidpro(args)

	#args['info_to_contact'] = second_msg_to_sent
	



	
	#Let's check if the reported number of outgoing patient is not inferior to the reported number of patients who were in that site. 

	outgoing_patients_report_for_that_week = OutgoingPatientsReport.objects.filter(date_of_first_week_day = args['sent_date'], report__facility =args['facility'])

	if(len(outgoing_patients_report_for_that_week) > 0):
		#It means that this site have given the outgoing patient report for that week
		outgoing_patients_report_for_that_week = outgoing_patients_report_for_that_week[0]
		
		all_outgoing_patient_for_that_week = outgoing_patients_report_for_that_week.gueri+outgoing_patients_report_for_that_week.deces+outgoing_patients_report_for_that_week.abandon + outgoing_patients_report_for_that_week.non_repondant +outgoing_patients_report_for_that_week.transfert_interne


		all_incoming_patient_for_that_week = float(args['text'].split(' ')[2]) + float(args['text'].split(' ')[3]) + float(args['text'].split(' ')[4]) + float(args['text'].split(' ')[5]) + float(args['text'].split(' ')[6]) + float(args['text'].split(' ')[7])

		print("===============================")
		print("OUT")
		print(all_outgoing_patient_for_that_week)
		print("IN")
		print(all_incoming_patient_for_that_week)
		print("===============================")


		if(all_outgoing_patient_for_that_week > all_incoming_patient_for_that_week):
			#If the reported out going patients number is super to the reported incoming patient number for a given week, the
			#system should alert the concerned persons
			print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
			print("Message to the supervisor")
			args['info_to_supervisor'] = "Probable erreur. Au site '"+args['facility'].name+"', le total des decharges rapporte est superieur au total des admissions rapporte pour la semaine commencee a la date suivante : "+str(args['sent_date'])
			print("Probable erreur. Au site '"+args['facility'].name+"', le total des decharges rapporte est superieur au total des admissions rapporte pour la semaine commencee a la date suivante : "+str(args['sent_date'])+"")

			print("Message to the contact")
			args['an_alert_message_to_contact'] = "Probable erreur. Le total des decharges rapporte est superieur au total des admissions rapporte pour la semaine commencee a la date suivante : "+str(args['sent_date'])+". Verfier si les chiffres envoyes sont corrects"
			print("Probable erreur. Le total des decharges rapporte est superieur au total des admissions rapporte pour la semaine commencee a la date suivante : "+str(args['sent_date'])+". Verfier si les chiffres envoyes sont corrects")
			print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")




			#The bolow code is for sending alert messages in case of outgoing patient number greater than the total patient number
			
			#the_contact_phone_number = "tel:"+args['the_sender'].phone_number
			#data = {"urns": [the_supervisor_phone_number],"text": args['info_to_supervisor']}
			#args['data'] = data
			#send_sms_through_rapidpro(args)

			#the_supervisor_phone_number = "tel:"+args['the_sender'].supervisor_phone_number
			#data = {"urns": [the_contact_phone_number],"text": args['an_alert_message_to_contact']}
			#args['data'] = data
			#send_sms_through_rapidpro(args)
'''
			
'''
#MODIFY
def modify_patient_served(args):
	#This function modifies a report about number of patient served in a given week

	args['mot_cle'] = 'ADMM'

	#Let's check if the message sent is composed by an expected number of values
	check_number_of_values(args)
	print(args['valide'])
	if not args['valide']:
		return

	#Let's check if the person who send this message is a reporter
	check_if_is_reporter(args)
	print(args['valide'])
	if not args['valide']:
		return

	#Let's check if the values sent are valid
	check_values_validity(args)
	print(args['valide'])
	if not args['valide']:
		return

	#Let's check if this facility have finished to give this report
	the_existing_same_report = IncomingPatientsReport.objects.filter(date_of_first_week_day = args['sent_date'], report__facility = args['facility'])
	if len(the_existing_same_report) < 1:
		args['valide'] = False
		args['info_to_contact'] = "Erreur. Aucune modification faite car aucun rapport commencant par le mot cle 'ADM' n avez ete donne par votre site avec la date que vous venez d envoyer."
		return
	
	#If this site have finished to gie this report, let's delete it and create the new one
	the_one_existing_same_report = the_existing_same_report[0]
	the_related_report = the_one_existing_same_report.report
	the_related_report.delete()

	#Let's save the report
	the_created_report = Report.objects.create(facility = args['facility'], reporting_date = datetime.datetime.now().date(), text = args['text'], category = 'ADMISSION')


	incoming_patients_report = IncomingPatientsReport.objects.create(report = the_created_report, total_debut_semaine = args['text'].split(' ')[2], ptb = args['text'].split(' ')[3], oedemes = args['text'].split(' ')[4], rechute = args['text'].split(' ')[5], readmission = args['text'].split(' ')[6], transfert_interne = args['text'].split(' ')[7], date_of_first_week_day = args['sent_date'])

	args['info_to_contact'] = "Modification reussie. Vous venez de rapporter les admissions comme suit : TDS="+args['text'].split(' ')[2]+", PTB="+args['text'].split(' ')[3]+", Oedemes="+args['text'].split(' ')[4]+", Rechute="+args['text'].split(' ')[5]+", Readmission="+args['text'].split(' ')[6]+", TI="+args['text'].split(' ')[7]+""






	#Let's check if the reported number of outgoing patient is not inferior to the reported number of patients who were in that site. 

	outgoing_patients_report_for_that_week = OutgoingPatientsReport.objects.filter(date_of_first_week_day = args['sent_date'], report__facility =args['facility'])

	if(len(outgoing_patients_report_for_that_week) > 0):
		#It means that this site have given the outgoing patient report for that week
		outgoing_patients_report_for_that_week = outgoing_patients_report_for_that_week[0]
		
		all_outgoing_patient_for_that_week = outgoing_patients_report_for_that_week.gueri+outgoing_patients_report_for_that_week.deces+outgoing_patients_report_for_that_week.abandon + outgoing_patients_report_for_that_week.non_repondant +outgoing_patients_report_for_that_week.transfert_interne


		all_incoming_patient_for_that_week = float(args['text'].split(' ')[2]) + float(args['text'].split(' ')[3]) + float(args['text'].split(' ')[4]) + float(args['text'].split(' ')[5]) + float(args['text'].split(' ')[6]) + float(args['text'].split(' ')[7])

		print("===============================")
		print("OUT")
		print(all_outgoing_patient_for_that_week)
		print("IN")
		print(all_incoming_patient_for_that_week)
		print("===============================")


		if(all_outgoing_patient_for_that_week > all_incoming_patient_for_that_week):
			#If the reported out going patients number is super to the reported incoming patient number for a given week, the
			#system should alert the concerned persons
			print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
			print("Message to the supervisor")
			args['info_to_supervisor'] = "Probable erreur. Au site '"+args['facility'].name+"', le total des decharges rapporte est superieur au total des admissions rapporte pour la semaine commencee a la date suivante : "+str(args['sent_date'])
			print("Probable erreur. Au site '"+args['facility'].name+"', le total des decharges rapporte est superieur au total des admissions rapporte pour la semaine commencee a la date suivante : "+str(args['sent_date'])+"")

			print("Message to the contact")
			args['an_alert_message_to_contact'] = "Probable erreur. Le total des decharges rapporte est superieur au total des admissions rapporte pour la semaine commencee a la date suivante : "+str(args['sent_date'])+". Verfier si les chiffres envoyes sont corrects"
			print("Probable erreur. Le total des decharges rapporte est superieur au total des admissions rapporte pour la semaine commencee a la date suivante : "+str(args['sent_date'])+". Verfier si les chiffres envoyes sont corrects")
			print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")



			#The bolow code is for sending alert messages in case of outgoing patient number greater than the total patient number
			
			#the_contact_phone_number = "tel:"+args['the_sender'].phone_number
			#data = {"urns": [the_supervisor_phone_number],"text": args['info_to_supervisor']}
			#args['data'] = data
			#send_sms_through_rapidpro(args)

			#the_supervisor_phone_number = "tel:"+args['the_sender'].supervisor_phone_number
			#data = {"urns": [the_contact_phone_number],"text": args['an_alert_message_to_contact']}
			#args['data'] = data
			#send_sms_through_rapidpro(args)

#--------------------------------------------------------------------------------------
'''




'''
#--------------------------------OUT GOING PATIENTS-----------------------------
#RECORD
def record_out_going_patients(args):
	#This function records a report about patients taken out of the program in a given week

	args['mot_cle'] = 'SRT'

	#Let's check if the person who send this message is a reporter
	check_if_is_reporter(args)
	print(args['valide'])
	if not args['valide']:
		return	


	#Let's check if the message sent is composed by an expected number of values
	check_number_of_values(args)
	print(args['valide'])
	if not args['valide']:
		return


	#Let's check if the values sent are valid
	check_values_validity(args)
	print(args['valide'])
	if not args['valide']:
		return

	#Let's check if this facility have not finished to give this report
	the_existing_same_report = OutgoingPatientsReport.objects.filter(date_of_first_week_day = args['sent_date'], report__facility = args['facility'])
	if len(the_existing_same_report) > 0:
		args['valide'] = False
		args['info_to_contact'] = "Erreur. Un rapport pour cette semaine avez ete enregistre. Pour le modifier, veuillez envoyer un message de modification commencant par le mot cle "+args['mot_cle']+"M"
		return

	#Let's save the report
	the_created_report = Report.objects.create(facility = args['facility'], reporting_date = datetime.datetime.now().date(), text = args['text'], category = 'SORTI')


	if args['facility'].facility_level == 'CDS':
		out_patients_report = OutgoingPatientsReport.objects.create(report = the_created_report, gueri = args['text'].split(' ')[2], deces = args['text'].split(' ')[3], abandon = args['text'].split(' ')[4], non_repondant = args['text'].split(' ')[5], transfert_interne = args['text'].split(' ')[6], date_of_first_week_day = args['sent_date'])

		args['info_to_contact'] = "Enregistrement reussie. Vous venez de rapporter les sorties des patients comme suit : Gueri="+args['text'].split(' ')[2]+", Deces="+args['text'].split(' ')[3]+", Abandons="+args['text'].split(' ')[4]+", Non repondant="+args['text'].split(' ')[5]+", Transfert interne="+args['text'].split(' ')[6]
	else:
		out_patients_report = OutgoingPatientsReport.objects.create(report = the_created_report, gueri = args['text'].split(' ')[2], deces = args['text'].split(' ')[3], abandon = args['text'].split(' ')[4], non_repondant = args['text'].split(' ')[5], date_of_first_week_day = args['sent_date'])

		args['info_to_contact'] = "Enregistrement reussie. Vous venez de rapporter les sorties des patients comme suit : TAS="+args['text'].split(' ')[2]+", Deces="+args['text'].split(' ')[3]+", Abandons="+args['text'].split(' ')[4]+", Non repondant="+args['text'].split(' ')[5]


	second_msg_to_sent = "Si vous voulez corriger ce rapport de sortie des patients que vous venez d envoyer, envoyer un message corrige et commencant par SRTM"




	#The below code will be uncommented in order to send the second sms after the first one
	
	#the_contact_phone_number = "tel:"+args['the_sender'].phone_number
	#data = {"urns": [the_contact_phone_number],"text": args['info_to_contact']}
	#args['data'] = data
	#send_sms_through_rapidpro(args)

	#args['info_to_contact'] = second_msg_to_sent
	



	#Let's check if the reported number of outgoing patient is not inferior to the reported number of patients who were in that site. 

	incoming_patients_report_for_that_week = IncomingPatientsReport.objects.filter(date_of_first_week_day = args['sent_date'], report__facility =args['facility'])

	if(len(incoming_patients_report_for_that_week) > 0):
		#It means that this site have given the incoming patient report for that week
		incoming_patients_report_for_that_week = incoming_patients_report_for_that_week[0]
		
		all_incoming_patient_for_that_week = incoming_patients_report_for_that_week.total_debut_semaine + incoming_patients_report_for_that_week.ptb + incoming_patients_report_for_that_week.oedemes + incoming_patients_report_for_that_week.rechute + incoming_patients_report_for_that_week.readmission + incoming_patients_report_for_that_week.transfert_interne


		all_outgoing_patient_for_that_week = float(args['text'].split(' ')[2]) + float(args['text'].split(' ')[3]) + float(args['text'].split(' ')[4]) + float(args['text'].split(' ')[5])


		if(all_outgoing_patient_for_that_week > all_incoming_patient_for_that_week):
			#If the reported out going patients number is super to the reported incoming patient number for a given week, the
			#system should alert the concerned persons
			print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
			print("Message to the supervisor")
			args['info_to_supervisor'] = "Probable erreur. Au site '"+args['facility'].name+"', le total des decharges rapporte est superieur au total des admissions rapporte pour la semaine commencee a la date suivante : "+str(args['sent_date'])
			print("Probable erreur. Au site '"+args['facility'].name+"', le total des decharges rapporte est superieur au total des admissions rapporte pour la semaine commencee a la date suivante : "+str(args['sent_date'])+"")

			print("Message to the contact")
			args['an_alert_message_to_contact'] = "Probable erreur. Le total des decharges rapporte est superieur au total des admissions rapporte pour la semaine commencee a la date suivante : "+str(args['sent_date'])+". Verfier si les chiffres envoyes sont corrects"
			print("Probable erreur. Le total des decharges rapporte est superieur au total des admissions rapporte pour la semaine commencee a la date suivante : "+str(args['sent_date'])+". Verfier si les chiffres envoyes sont corrects")
			print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")




			#The bolow code is for sending alert messages in case of outgoing patient number greater than the total patient number
			
			the_contact_phone_number = "tel:"+args['the_sender'].phone_number
			data = {"urns": [the_supervisor_phone_number],"text": args['info_to_supervisor']}
			args['data'] = data
			send_sms_through_rapidpro(args)

			the_supervisor_phone_number = "tel:"+args['the_sender'].supervisor_phone_number
			data = {"urns": [the_contact_phone_number],"text": args['an_alert_message_to_contact']}
			args['data'] = data
			send_sms_through_rapidpro(args)

'''

'''
#MODIFY
def modify_out_going_patients(args):
	#This function modifies a report about patients taken out of the program in a given week

	args['mot_cle'] = 'SRTM'

	#Let's check if the person who send this message is a reporter
	check_if_is_reporter(args)
	print(args['valide'])
	if not args['valide']:
		return	


	#Let's check if the message sent is composed by an expected number of values
	check_number_of_values(args)
	print(args['valide'])
	if not args['valide']:
		return


	#Let's check if the values sent are valid
	check_values_validity(args)
	print(args['valide'])
	if not args['valide']:
		return

	#Let's check if this facility have finished to give this report
	the_existing_same_report = OutgoingPatientsReport.objects.filter(date_of_first_week_day = args['sent_date'], report__facility = args['facility'])
	if len(the_existing_same_report) < 1:
		args['valide'] = False
		args['info_to_contact'] = "Erreur. Aucune modification faite car aucun rapport commencant par le mot cle 'SRT' n avez ete donne par votre site avec la date que vous venez d envoyer."
		return

	#If this site have finished to gie this report, let's delete it and create the new one
	the_one_existing_same_report = the_existing_same_report[0]
	the_related_report = the_one_existing_same_report.report
	the_related_report.delete()


	#Let's save the report
	the_created_report = Report.objects.create(facility = args['facility'], reporting_date = datetime.datetime.now().date(), text = args['text'], category = 'SORTI')


	if args['facility'].facility_level == 'CDS':
		out_patients_report = OutgoingPatientsReport.objects.create(report = the_created_report, gueri = args['text'].split(' ')[2], deces = args['text'].split(' ')[3], abandon = args['text'].split(' ')[4], non_repondant = args['text'].split(' ')[5], transfert_interne = args['text'].split(' ')[6], date_of_first_week_day = args['sent_date'])

		args['info_to_contact'] = "Modification reussie. Vous venez de rapporter les sorties des patients comme suit : Gueri="+args['text'].split(' ')[2]+", Deces="+args['text'].split(' ')[3]+", Abandons="+args['text'].split(' ')[4]+", Non repondant="+args['text'].split(' ')[5]+", Transfert interne="+args['text'].split(' ')[6]
	else:
		out_patients_report = OutgoingPatientsReport.objects.create(report = the_created_report, gueri = args['text'].split(' ')[2], deces = args['text'].split(' ')[3], abandon = args['text'].split(' ')[4], non_repondant = args['text'].split(' ')[5], date_of_first_week_day = args['sent_date'])

		args['info_to_contact'] = "Modification reussie. Vous venez de rapporter les sorties des patients comme suit : TAS="+args['text'].split(' ')[2]+", Deces="+args['text'].split(' ')[3]+", Abandons="+args['text'].split(' ')[4]+", Non repondant="+args['text'].split(' ')[5]


	#Let's check if the reported number of outgoing patient is not inferior to the reported number of patients who were in that site. 

	incoming_patients_report_for_that_week = IncomingPatientsReport.objects.filter(date_of_first_week_day = args['sent_date'], report__facility =args['facility'])

	if(len(incoming_patients_report_for_that_week) > 0):
		#It means that this site have given the incoming patient report for that week
		incoming_patients_report_for_that_week = incoming_patients_report_for_that_week[0]
		
		all_incoming_patient_for_that_week = incoming_patients_report_for_that_week.total_debut_semaine + incoming_patients_report_for_that_week.ptb + incoming_patients_report_for_that_week.oedemes + incoming_patients_report_for_that_week.rechute + incoming_patients_report_for_that_week.readmission + incoming_patients_report_for_that_week.transfert_interne


		all_outgoing_patient_for_that_week = float(args['text'].split(' ')[2]) + float(args['text'].split(' ')[3]) + float(args['text'].split(' ')[4]) + float(args['text'].split(' ')[5])

		
		if(all_outgoing_patient_for_that_week > all_incoming_patient_for_that_week):
			#If the reported out going patients number is super to the reported incoming patient number for a given week, the
			#system should alert the concerned persons
			print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
			print("Message to the supervisor")
			args['info_to_supervisor'] = "Probable erreur. Au site '"+args['facility'].name+"', le total des decharges rapporte est superieur au total des admissions rapporte pour la semaine commencee a la date suivante : "+args['sent_date']
			print("Probable erreur. Au site '"+args['facility'].name+"', le total des decharges rapporte est superieur au total des admissions rapporte pour la semaine commencee a la date suivante : "+args['sent_date']+"")

			print("Message to the contact")
			args['an_alert_message_to_contact'] = "Probable erreur. Le total des decharges rapporte est superieur au total des admissions rapporte pour la semaine commencee a la date suivante : "+args['sent_date']+". Verfier si les chiffres envoyes sont corrects"
			print("Probable erreur. Le total des decharges rapporte est superieur au total des admissions rapporte pour la semaine commencee a la date suivante : "+args['sent_date']+". Verfier si les chiffres envoyes sont corrects")
			print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")




			#The bolow code is for sending alert messages in case of outgoing patient number greater than the total patient number
			
			#the_contact_phone_number = "tel:"+args['the_sender'].phone_number
			#data = {"urns": [the_supervisor_phone_number],"text": args['info_to_supervisor']}
			#args['data'] = data
			#send_sms_through_rapidpro(args)

			#the_supervisor_phone_number = "tel:"+args['the_sender'].supervisor_phone_number
			#data = {"urns": [the_contact_phone_number],"text": args['an_alert_message_to_contact']}
			#args['data'] = data
			#send_sms_through_rapidpro(args)
'''
			
			
#--------------------------------------------------------------------------------------

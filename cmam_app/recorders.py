from cmam_app.models import *
from django.db.models import Q
import re
import datetime
import requests
import json
from django.conf import settings



def check_number_of_values(args):
	#This function checks if the message sent is composed by an expected number of values
	print("==len(args['text'].split(' '))==")
	print(len(args['text'].split(' ')))
	print(args['text'].split(' '))
	if(args['message_type']=='SELF_REGISTRATION'):
		if len(args['text'].split(' ')) < 3:
			args['valide'] = False
			args['info_to_contact'] = "Vous avez envoye peu de valeurs. Veuillez reenvoyer le message corrige."
		if len(args['text'].split(' ')) > 3:
			args['valide'] = False
			args['info_to_contact'] = "Vous avez envoye beaucoup de valeurs. Veuillez reenvoyer le message corrige."
		if len(args['text'].split(' ')) == 3:
			args['valide'] = True
			args['info_to_contact'] = "Le nombre de valeurs envoye est correct."
	if(args['message_type']=='STOCK_RECU'):
		if len(args['text'].split(' ')) < 6:
			args['valide'] = False
			args['info_to_contact'] = "Vous avez envoye peu de valeurs. Veuillez reenvoyer le message corrige."
		if len(args['text'].split(' ')) > 6:
			args['valide'] = False
			args['info_to_contact'] = "Vous avez envoye beaucoup de valeurs. Veuillez reenvoyer le message corrige."
		if len(args['text'].split(' ')) == 6:
			args['valide'] = True
			args['info_to_contact'] = "Le nombre de valeurs envoye est correct."
	if(args['message_type']=='STOCK_SORTI'):
		if len(args['text'].split(' ')) < 7:
			args['valide'] = False
			args['info_to_contact'] = "Vous avez envoye peu de valeurs. Veuillez reenvoyer le message corrige."
		if len(args['text'].split(' ')) > 7:
			args['valide'] = False
			args['info_to_contact'] = "Vous avez envoye beaucoup de valeurs. Veuillez reenvoyer le message corrige."
		if len(args['text'].split(' ')) == 7:
			args['valide'] = True
			args['info_to_contact'] = "Le nombre de valeurs envoye est correct."
	if(args['message_type']=='RUPTURE'):
		if len(args['text'].split(' ')) < 3:
			args['valide'] = False
			args['info_to_contact'] = "Vous avez envoye peu de valeurs. Veuillez reenvoyer le message corrige."
		if len(args['text'].split(' ')) > 3:
			args['valide'] = False
			args['info_to_contact'] = "Vous avez envoye beaucoup de valeurs. Veuillez reenvoyer le message corrige."
		if len(args['text'].split(' ')) == 3:
			args['valide'] = True
			args['info_to_contact'] = "Le nombre de valeurs envoye est correct."
	if(args['message_type']=='BALANCE'):
		if len(args['text'].split(' ')) < 6:
			args['valide'] = False
			args['info_to_contact'] = "Vous avez envoye peu de valeurs. Veuillez reenvoyer le message corrige."
		if len(args['text'].split(' ')) > 6:
			args['valide'] = False
			args['info_to_contact'] = "Vous avez envoye beaucoup de valeurs. Veuillez reenvoyer le message corrige."
		if len(args['text'].split(' ')) == 6:
			args['valide'] = True
			args['info_to_contact'] = "Le nombre de valeurs envoye est correct."
	if(args['message_type']=='ADMISSION'):
		if len(args['text'].split(' ')) < 8:
			args['valide'] = False
			args['info_to_contact'] = "Vous avez envoye peu de valeurs. Veuillez reenvoyer le message corrige."
		if len(args['text'].split(' ')) > 8:
			args['valide'] = False
			args['info_to_contact'] = "Vous avez envoye beaucoup de valeurs. Veuillez reenvoyer le message corrige."
		if len(args['text'].split(' ')) == 8:
			args['valide'] = True
			args['info_to_contact'] = "Le nombre de valeurs envoye est correct."
	if(args['message_type']=='SORTI'):
		if len(args['text'].split(' ')) < 9:
			args['valide'] = False
			args['info_to_contact'] = "Vous avez envoye peu de valeurs. Veuillez reenvoyer le message corrige."
		if len(args['text'].split(' ')) > 9:
			args['valide'] = False
			args['info_to_contact'] = "Vous avez envoye beaucoup de valeurs. Veuillez reenvoyer le message corrige."
		if len(args['text'].split(' ')) == 9:
			args['valide'] = True
			args['info_to_contact'] = "Le nombre de valeurs envoye est correct."



def check_if_is_reporter(args):
	''' This function checks if the contact who sent the current message is a reporter '''
	concerned_reporter = Reporter.objects.filter(phone_number = args['phone'])
	if len(concerned_reporter) < 1:
		#This person is not in the list of reporters
		args['valide'] = False
		args['info_to_contact'] = "Erreur. Vous ne vous etes pas enregistre pour pouvoir donner des rapports."
		return

	one_concerned_reporter = concerned_reporter[0]

	if not one_concerned_reporter.facility:
		#The CDS of this reporter is not known
		args['valide'] = False
		args['info_to_contact'] = "Erreur. Votre CDS n est pas connu dans le systeme."
		return

	args['the_sender'] =  one_concerned_reporter
	args['facility'] = one_concerned_reporter.facility
	args['valide'] = True
	args['info_to_contact'] = " Le bureau d affectation de ce rapporteur est connu "



def check_date_is_valid(args):
	''' This function checks if a given date is valid '''
	given_date = ""

	#Let's put the value to check in 'given_date' variable
		
	if(args['message_type']=='STOCK_RECU'):
		given_date = args['text'].split(' ')[1]
	if(args['message_type']=='STOCK_SORTI'):
		given_date = args['text'].split(' ')[2]
	if(args['message_type']=='BALANCE'):
		given_date = args['text'].split(' ')[1]
	if(args['message_type']=='ADMISSION'):
		given_date = args['text'].split(' ')[1]
	if(args['message_type']=='SORTI'):
		given_date = args['text'].split(' ')[1]
 
	if not given_date:
		args['valide'] = False
		args['info_to_contact'] = "Exception. Pas de date trouvee pour la verification."
		return

	#expression = r'^((0[1-9])|([1-2][0-9])|(3[01]))-((0[1-9])|(1[0-2]))-[0-9]{4}$'
	expression = r'^((0[1-9])|([1-2][0-9])|(3[01]))((0[1-9])|(1[0-2]))[0-9]{2}$'
	if re.search(expression, given_date) is None:
		args['valide'] = False
		args['info_to_contact'] = "Erreur. La date indiquee n est pas valide."
		return


	sent_date = given_date[0:2]+"-"+given_date[2:4]+"-20"+given_date[4:]

	sent_date_without_dash = sent_date.replace("-","")
	try:
		date_sent = datetime.datetime.strptime(sent_date_without_dash, "%d%m%Y").date()
	except:
		args['valide'] = False
		args['info_to_contact'] = "Erreur. La date indiquee n est pas valide."
		return

	args['sent_date'] =  date_sent

	if date_sent > datetime.datetime.now().date():
		#The reporter can not report for a future date
		args['valide'] = False
		args['info_to_contact'] = "Erreur. La date indiquee n est pas encore arrivee."
		return




def check_is_float(args):
	''' This function checks if a given value is a float '''

	expression = r'^([0-9]+.[0-9]+)|([0-9]+)$'

	value_to_check = args['value_to_check']

	if re.search(expression, value_to_check) is None:
		args['valide'] = False
		args['info_to_contact'] = "Erreur. La valeur envoyee en position "+str(args['position'])+" n est pas valide."
	else:
		args['valide'] = True
		args['info_to_contact'] = "La valeur envoyee en position "+str(args['position'])+" est valide."

	
	




def check_is_int(args):
	''' This function checks if a given value is an int '''

	expression = r'^[0-9]+$'
	
	value_to_check = args['value_to_check']

	if re.search(expression, value_to_check) is None:
		args['valide'] = False
		args['info_to_contact'] = "Erreur. La valeur envoyee en position "+str(args['position'])+" n est pas valide."
	else:
		args['valide'] = True
		args['info_to_contact'] = "La valeur envoyee en position "+str(args['position'])+" est valide."
	 



def check_values_validity(args):
	''' This function checks if values sent are valid '''
	if(args['message_type']=='STOCK_RECU'):
		#Let's check if the value in the position number 1 is a date
		args['value_to_check'] =  args['text'].split(' ')[1]
		args['position'] = 1 
		check_date_is_valid(args)
		if not args['valide']:
			return
		#Let's check if the value in the position number 2 is a float
		args['value_to_check'] =  args['text'].split(' ')[2]
		args['position'] = 2
		check_is_float(args)
		if not args['valide']:
			return
		#Let's check if the value in the position number 3 is a float
		args['value_to_check'] =  args['text'].split(' ')[3]
		args['position'] = 3
		check_is_float(args)
		if not args['valide']:
			return
		#Let's check if the value in the position number 4 is a float
		args['value_to_check'] =  args['text'].split(' ')[4]
		args['position'] = 4
		check_is_float(args)
		if not args['valide']:
			return
		#Let's check if the value in the position number 5 is a float
		args['value_to_check'] =  args['text'].split(' ')[5]
		args['position'] = 5
		check_is_float(args)
		if not args['valide']:
			return
		

	if(args['message_type']=='STOCK_SORTI'):
		#Let's check if the value in the position number 1 is a facility code and not the code of the current facility

		#Let's check if the value in the position number 2 is a date
		args['value_to_check'] =  args['text'].split(' ')[2]
		args['position'] = 2		
		check_date_is_valid(args)
		if not args['valide']:
			return
		#Let's check if the value in the position number 3 is a float
		args['value_to_check'] =  args['text'].split(' ')[3]
		args['position'] = 3
		check_is_float(args)
		if not args['valide']:
			return
		#Let's check if the value in the position number 4 is a float
		args['value_to_check'] =  args['text'].split(' ')[4]
		args['position'] = 4
		check_is_float(args)
		if not args['valide']:
			return
		#Let's check if the value in the position number 5 is a float
		args['value_to_check'] =  args['text'].split(' ')[5]
		args['position'] = 5
		check_is_float(args)
		if not args['valide']:
			return
		#Let's check if the value in the position number 6 is a float
		args['value_to_check'] =  args['text'].split(' ')[6]
		args['position'] = 6
		check_is_float(args)
		if not args['valide']:
			return

	if(args['message_type']=='RUPTURE'):
		#Let's check if the value in the position number 1 is a product name

		#Let's check if the value in the position number 2 is a float
		args['value_to_check'] =  args['text'].split(' ')[2]
		args['position'] = 2
		check_is_float(args)
		if not args['valide']:
			return

	if(args['message_type']=='BALANCE'):
		#Let's check if the value in the position number 1 is a date
		args['value_to_check'] =  args['text'].split(' ')[1]
		args['position'] = 1
		check_date_is_valid(args)
		if not args['valide']:
			return
		#Let's check if the value in the position number 2 is a float
		args['value_to_check'] =  args['text'].split(' ')[2]
		args['position'] = 2		
		check_is_float(args)
		if not args['valide']:
			return
		#Let's check if the value in the position number 3 is a float
		args['value_to_check'] =  args['text'].split(' ')[3]
		args['position'] = 3
		check_is_float(args)
		if not args['valide']:
			return
		#Let's check if the value in the position number 4 is a float
		args['value_to_check'] =  args['text'].split(' ')[4]
		args['position'] = 4
		check_is_float(args)
		if not args['valide']:
			return
		#Let's check if the value in the position number 5 is a float
		args['value_to_check'] =  args['text'].split(' ')[5]
		args['position'] = 5
		check_is_float(args)
		if not args['valide']:
			return

	if(args['message_type']=='ADMISSION'):
		#Let's check if the value in the position number 1 is a date
		args['value_to_check'] =  args['text'].split(' ')[1]
		args['position'] = 1
		check_date_is_valid(args)
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


	if(args['message_type']=='SORTI'):
		#Let's check if the value in the position number 1 is a date
		args['value_to_check'] =  args['text'].split(' ')[1]
		args['position'] = 1
		check_date_is_valid(args)
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
		#Let's check if the value in the position number 7 is an int
		args['value_to_check'] =  args['text'].split(' ')[7]
		args['position'] = 7
		check_is_int(args)
		if not args['valide']:
			return
		#Let's check if the value in the position number 7 is an int
		args['value_to_check'] =  args['text'].split(' ')[8]
		args['position'] = 8
		check_is_int(args)
		if not args['valide']:
			return

#======================reporters self registration==================================


def check_facility(args):
	''' This function checks if the facility code sent by the reporter exists '''
	the_facility_code = args['text'].split(' ')[1]
	concerned_facility = Facility.objects.filter(id_facility = the_facility_code)
	if (len(concerned_facility) > 0):
		args['valide'] = True
		args['info_to_contact'] = "Le code (STA ou SST ou ...) envoye est reconnu."
	else:
		args['valide'] = False
		args['info_to_contact'] = "Le code (STA ou SST ou ...) envoye n est pas enregistre dans le systeme."

def check_supervisor_phone_number(args):
	''' This function checks if the phone number of the supervisor is well written '''
	the_supervisor_phone_number = args['text'].split(' ')[2]
	the_supervisor_phone_number_no_space = the_supervisor_phone_number.replace(" ", "")
	expression = r'^(\+?(257)?)((62)|(79)|(71)|(76))([0-9]{6})$'
	print(the_supervisor_phone_number_no_space)
	if re.search(expression, the_supervisor_phone_number_no_space) is None:
		#The phone number is not well written
		args['valide'] = False
		args['info_to_contact'] = "Le numero de telephone du superviseur n est pas bien ecrit."
	else:
		args['valide'] = True
		args['info_to_contact'] = "Le numero de telephone du superviseur est bien ecrit."

'''
def check_supervisor_phone_number_not_for_this_contact(args):
	'This function checks if the contact didn't send his/her phone number in the place of the supervisor phone number'
	print("args['phone']")
	print(args['phone'])
	print("args['phone'][4:]")
	print(args['phone'][4:])
	print("args['text'].split(' ')[2]")
	print(args['text'].split(' ')[2])
	if args['phone'] == args['text'].split(' ')[2] or args['phone'][4:] == args['text'].split(' ')[2]:
		args['valide'] = False
		args['info_to_contact'] = "Erreur. Le numero de telephone du superviseur ne peut pas etre le tien."
	else:
		args['valide'] = True
		args['info_to_contact'] = "Le numero de telephone du superviseur est bien note."
'''

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
			args['info_to_contact'] = "Merci. Veuillez confirmer le numero de telephone du superviseur s il vous plait."


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
				args['info_to_contact'] = "Erreur. Vous etes deja enregistre sur ce code et avec le meme numero de telephone du superviseur. Envoyer votre rapport ou X pour sortir."
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
				args['info_to_contact'] = "Mise a jour du bureau d affectation reussie. Votre nouveau bureau est : "+the_one_existing_temp.facility.name
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
				args['info_to_contact'] = "Mise a jour reussie. Le nouveau numero de telephone de votre superviseur est : "+the_one_existing_temp.supervisor_phone_number+". Merci."
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
				args['info_to_contact'] = "Mise a jour reussie. Le nouveau numero de votre superviseur est : "+the_one_existing_temp.supervisor_phone_number+" et le nouveau centre d affectation est :"+the_one_existing_temp.facility.name
				the_one_existing_temp.delete()
				return


			#This contact is doing a first registration. Let's record him/her
			Reporter.objects.create(phone_number = the_one_existing_temp.phone_number,facility = the_one_existing_temp.facility, supervisor_phone_number = the_one_existing_temp.supervisor_phone_number)
			the_one_existing_temp.delete()
			args['valide'] = True
			args['info_to_contact'] = "Vous vous etes enregistre correctement."
		else:
			the_one_existing_temp.delete()
			args['valide'] = False
			args['info_to_contact'] = "Vous avez envoye le numero de telephone du superviseur de differentes manieres. Veuillez reenvoyer le message commencant par rg. Merci"



#-----------------------------------------------------------------










#-----------------------------RECORD STOCK RECEIVED------------------------------------

def record_stock_received(args):
	''' This function records a report about medicines received '''
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
#--------------------------------------------------------------------------------------








#------------------------------RECORD SENT STOCK---------------------------------------

def record_sent_stock(args):
	''' This function records a report about medicines sent from one facility to an other '''
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
#--------------------------------------------------------------------------------------







#-------------------------------RECORD A STOCK OUT------------------------------------

def record_stock_out(args):
	''' This function records a report about a stock out of a medicine '''
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
#-------------------------------------------------------------------------------------







#--------------------------------RECORD CURRENT STOCK----------------------------------

def record_current_stock(args):
	''' This function records a report about current quantities of medicines '''
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
#--------------------------------------------------------------------------------------







#---------------------------------RECORD NUMBERS OF PATIENTS SERVED--------------------

def record_patient_served(args):
	''' This function records a report about number of patient served in a given week '''
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
#--------------------------------------------------------------------------------------






#--------------------------------RECORD OUT GOING PATIENTS-----------------------------

def record_out_going_patients(args):
	''' This function records a report about patients taken out of the program in a given week '''
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
#--------------------------------------------------------------------------------------

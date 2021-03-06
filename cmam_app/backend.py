from jsonview.decorators import json_view
from django.views.decorators.csrf import csrf_exempt
import re
from django.conf import settings
from cmam_app.models import Temporary
from recorders import *
import urllib
import json


def identify_message(args):
    """ This function identifies which kind of message this message is. """
    incoming_prefix = args["text"].split(" ")[0].upper()
    if args["text"].split(" ")[0].upper() in getattr(settings, "KNOWN_PREFIXES", ""):
        # Prefixes and related meanings are stored in the dictionary "KNOWN_PREFIXES"
        args["message_type"] = getattr(settings, "KNOWN_PREFIXES", "")[incoming_prefix]
    else:
        args["message_type"] = "UNKNOWN_MESSAGE"


def check_session(args):
    """This function checks if there is an already created session"""
    reporter_phone_number = args["phone"]
    concerned_reporter = Temporary.objects.filter(phone_number=reporter_phone_number)
    if len(concerned_reporter) < 1:
        args["has_session"] = False
    else:
        args["has_session"] = True


def eliminate_unnecessary_spaces(args):
    """This function eliminate unnecessary spaces in an the incoming message"""
    the_incoming_message = args["results"]["rapport1"]["input"]
    print("The text before sub             " + the_incoming_message)
    # the_new_message = re.sub(' +',' ',the_incoming_message)

    # Messages from RapidPro comes with spaces replaced by '+'
    # Let's replace those '+' (one or more) by one space
    the_new_message = re.sub("[+]+", " ", the_incoming_message)

    #  Find any comma
    the_new_message = urllib.unquote_plus(the_new_message)

    # Let's eliminate spaces at the begining and the end of the message
    the_new_message = the_new_message.strip()
    print("The text after sub              " + the_new_message)
    args["text"] = the_new_message
    print("The text after sub args['text'] " + args["text"])


def byteify(input):
    if isinstance(input, dict):
        return {byteify(key): byteify(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode("utf-8")
    else:
        return input


@csrf_exempt
@json_view
def handel_rapidpro_request(request):
    """This function receives requests sent by RapidPro.
    This function send json data to RapidPro as a response."""
    # We will put all data sent by RapidPro in this variable
    incoming_data = {}

    # Let's put all the incoming data in the dictionary 'incoming_data'
    incoming_data = byteify(json.loads(request.body))

    # Let's assume that the incoming data is valid
    incoming_data["valide"] = True
    incoming_data["info"] = "The default information."

    # Because RapidPro sends the contact phone number in the format "tel:+12345678925"
    # let's get it from incomming_data
    incoming_data["phone"] = incoming_data["contact"]["urn"].replace("tel:", "")

    # Let's instantiate the variable this function will return
    response = {}

    # Let's eliminate unnecessary spaces in the incoming message
    eliminate_unnecessary_spaces(incoming_data)

    incoming_data["info_to_supervisor"] = False

    # Let's check which kind of message this message is.
    identify_message(incoming_data)

    if incoming_data["message_type"] == "UNKNOWN_MESSAGE":
        # Let's check if this contact is confirming his phone number
        # It means that he has an already created session
        check_session(incoming_data)
        if not (incoming_data["has_session"]):
            # This contact doesn't have an already created session
            response["ok"] = False
            response[
                "info_to_contact"
            ] = "Le mot qui commence votre message n est pas reconnu par le systeme. Reenvoyez votre message en commencant par un mot cle valide."
            return response
        else:
            # This contact is confirming the phone number of his supervisor
            complete_registration(incoming_data)
            # response['ok'] = False
            response["ok"] = incoming_data["valide"]
            response["info_to_contact"] = incoming_data["info_to_contact"]
            return response

    if (
        incoming_data["message_type"] == "SELF_REGISTRATION"
        or incoming_data["message_type"] == "SELF_REGISTRATION_M"
    ):
        # The contact who sent the current message is doing self registration
        # in the group of reporters
        temporary_record_reporter(incoming_data)
    if incoming_data["message_type"] == "STOCK_RECU":
        # This contact is reporing a reception of medicines at his/her facility
        record_stock_received(incoming_data)
    if incoming_data["message_type"] == "STOCK_SORTI":
        # This contact is reporting a trensfer of medicines from his facility
        # to an other facility
        record_sent_stock(incoming_data)
    if incoming_data["message_type"] == "RUPTURE":
        # This contact is reporting a stock out of a medicine
        record_stock_out(incoming_data)
    if incoming_data["message_type"] == "BALANCE":
        # This contact is reporting the remaining quantities of medicines
        record_current_stock(incoming_data)
    if incoming_data["message_type"] == "ADMISSION":
        # This contact is reporting numbers of patients received in a given week
        record_patient_served(incoming_data)
    if incoming_data["message_type"] == "SORTI":
        # This contact is reporting numbers of patients no longer followed
        # by this facility since a given week
        record_out_going_patients(incoming_data)

    if incoming_data["message_type"] == "STOCK_RECU_M":
        # This contact is reporing a reception of medicines at his/her facility
        modify_stock_received(incoming_data)
    if incoming_data["message_type"] == "STOCK_SORTI_M":
        # This contact is reporting a trensfer of medicines from his facility
        # to an other facility
        modify_sent_stock(incoming_data)
    if incoming_data["message_type"] == "RUPTURE_M":
        # This contact is reporting a stock out of a medicine
        modify_stock_out(incoming_data)
    if incoming_data["message_type"] == "BALANCE_M":
        # This contact is reporting the remaining quantities of medicines
        modify_current_stock(incoming_data)
    if incoming_data["message_type"] == "ADMISSION_M":
        # This contact is reporting numbers of patients received in a given week
        modify_patient_served(incoming_data)
    if incoming_data["message_type"] == "SORTI_M":
        # This contact is reporting numbers of patients no longer followed by
        # this facility since a given week
        modify_out_going_patients(incoming_data)

    if incoming_data["valide"]:
        # The message have been recorded
        response["ok"] = True
    else:
        # The message haven't been recorded
        response["ok"] = False

    response["info_to_contact"] = incoming_data["info_to_contact"]

    if incoming_data["info_to_supervisor"]:
        response["info_to_supervisors"] = incoming_data["info_to_supervisor"]

    return response

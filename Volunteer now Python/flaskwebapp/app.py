from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

account = "AC9979a3d41a31d5acae3d55cf9a816529"
token = "17d5401a2b667a9a8863b47d76cd66e5"

admin_numbers = {"19412501194"}
senders = []
volunteers = []
Hosts = []
message = ""

class Message:
    def __init__(self, sender, text):
        self.number = sender
        self.text = text

class Sender:
    def __init__(self, sender, text):
        self.number = sender
        self.__texts = []
        self.events = []
        self.__texts.append(text)
        
    #getters
    def get_number(self):
        return self.number
    
    def get_text(self):
        return self.text
    
    #setters
    def set_number(self, number):
        self.number = number
    
    def append_text(self, text):
        self.__texts.append(text)


class Volunteer(Sender):
    """_summary_: We have our volunteer class, which will be used to store all the information about the volunteer.
    """
    def __init__(self):
        # initialize variables
        self.full_name = None
        self.events = []
        self.hours = []

    # getters
    def get_phone_number(self):
        return self.phone_number

    def get_full_name(self):
        return self.full_name
    
    def get_events(self):
        return self.events
    
    def get_hours(self):
        return self.hours
    
    # setters
    def set_phone_number(self, phone_number):
        self.phone_number = phone_number
    
    def set_full_name(self, full_name):
        self.full_name = full_name

    def set_events(self, events):
        self.events = events

    def set_hours(self, hours):
        self.hours = hours

class Host(Sender):
    """_summary_: We have our host class, which will be used to store all the information about the host.
    """
    def __init__(self):
        # initialize variables
        self.organization = None
        self.dates = []
        self.hours_available = []

    # getters
    def get_phone_number(self):
        return self.phone_number

    def get_organization(self):
        return self.organization
    
    def get_events(self):
        return self.events
    
    def get_dates(self):
        return self.dates

    def get_hours_available(self):
        return self.hours_available

    # setters
    def set_phone_number(self, phone_number):
        self.phone_number = phone_number
    
    def set_organization(self, organization):
        self.organization = organization
    
    def set_events(self, events):
        self.events = events
    
    def set_dates(self, dates):
        self.dates = dates

    def set_hours_available(self, hours_available):
        self.hours_available = hours_available

def message_processing(message):
    """_summary_: This function will process the message that the user sends to the bot.
    if the message is a new number, we will add them to the list of senders and append their
    message in texts. If the message is not a new number, we will append the message to the list of texts.

    Args:
        message (_type_): A message containing the text and the number of the sender.
    """
    if message.number in senders.number:
        # If the number is in the list of senders, we will append the message to the list of texts
        message.number.append_text(message.text)
    else:
        # If the number is not in the list of senders, we will add them to the list of senders and append their message in texts
        senders.append(message.number)
        message.number.append_text(message.text)



def volunteer_prompt(sender):
    # If new number is not in the list of volunteers, add them to the list
        if sender.number not in volunteers.phone_numbers:
            # Create a new volunteer object
            sender.number = Volunteer()
            volunteers.append(sender.number)

            message = ("Thank you for volunteering! Please enter your full name.")
            return
        elif sender.number in volunteers.phone_numbers:
            # If the volunteer is already in the list, we will ask them to enter their full name
            # If the volunteer has already entered their full name, we will ask them to enter their events
            if sender.number.full_name == None:
                sender.number.full_name = sender.text
                message = ("Thank you! Please enter the events you would like to volunteer for.")
                return
            elif sender.number.full_name != None:
                if sender.number.events == None:
                    sender.number.events = sender.text
                    message = ("Thank you! Please enter the hours you would like to volunteer for.")
                    return
                elif sender.number.events != None:
                    if sender.number.hours == None:
                        sender.number.hours = sender.text
                        message = ("Thank you! You have been added to the list of volunteers.")
                        return
                    elif sender.number.hours != None:
                        message = ("You have already entered your information.")
                        return
        
        

def host_prompt(sender):
    # If new number is not in the list of Hosts, add them to the list if they get approved by the admin
    if sender.number not in Hosts.number:
        # Saves as sender object until approved by admin
        sender.number = Sender()
        senders.append(sender.number)

        message = "Thank you for hosting! Please enter your organization name. After you have entered your " \
            "organization name, you will be contacted by an admin to verify your information."

        return
    elif sender.number in senders.number:
        if sender.__texts[-2] == "Host":

            message = "Thank you for submitting your organization name. You will be " \
                "contacted by an admin to verify your information."

def add_host_promt(sent_message):
    pass;



@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    """Send a dynamic reply to an incoming text message"""

    # Start our TwiML response
    resp = MessagingResponse()

    # Add a message so we can use message.number and message.text
    message = message(request.values.get('From', None), request.values.get('Body', None))

    #  process the message
    message_processing(message)


    # If the user is a volunteer they text volunteer to our number
    if message.text == 'Volunteer':
        volunteer_prompt(message)
        resp.message(message)
        return str(resp)
    
    # If the user is a volunteer they text volunteer to our number
    elif message.text == 'Host':
        host_prompt(message)
        resp.message(message)
        return str(resp)
    
    elif message.text == 'Add Host' and message.number in admin_numbers:
        add_host_promt(message)
    # If the user hasnt typed either volunteer or host, they are prompted to do so
    else:
        message = "Please text Volunteer or Host"
        resp.message(message)
        return str(resp)

    del message

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8080', debug=True)
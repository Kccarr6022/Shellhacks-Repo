from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

volunteers = []
Hosts = []
message = ""

class sender:
    def __init__(self, sender, text):
        self.phone_number = sender
        self.text = text
        
    #getters
    def get_number(self):
        return self.number
    
    def get_text(self):
        return self.text
    
    #setters
    def set_number(self, number):
        self.number = number
    
    def set_text(self, text):
        self.text = text


class Volunteer(sender):
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

class Host(sender):
    """_summary_: We have our host class, which will be used to store all the information about the host.
    """
    def __init__(self):
        # initialize variables
        self.organization = None
        self.events = []
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


def volunteer_prompt(sent_message):
    # If new number is not in the list of volunteers, add them to the list
        if sent_message.number not in volunteers.phone_numbers:
            # Create a new volunteer object
            sent_message.number = Volunteer()

            message = ("Thank you for volunteering! Please enter your full name.")
            return
        elif sent_message.number in volunteers.phone_numbers:
            # If the volunteer is already in the list, we will ask them to enter their full name
            # If the volunteer has already entered their full name, we will ask them to enter their events
            if sent_message.number.full_name == None:
                sent_message.number.full_name = sent_message.text
                message = ("Thank you! Please enter the events you would like to volunteer for.")
                return
            elif sent_message.number.full_name != None:
                if sent_message.number.events == None:
                    sent_message.number.events = sent_message.text
                    message = ("Thank you! Please enter the hours you would like to volunteer for.")
                    return
                elif sent_message.number.events != None:
                    if sent_message.number.hours == None:
                        sent_message.number.hours = sent_message.text
                        message = ("Thank you! You have been added to the list of volunteers.")
                        return
                    elif sent_message.number.hours != None:
                        message = ("You have already entered your information.")
                        return
        
        

def host_prompt(sent_message):
    # If new number is not in the list of Hosts, add them to the list if they get approved by the admin
    if sent_message.number not in Hosts.phone_numbers:
        # Create a new Host object
        sent_message.number = Host()

        message = ("Thank you for hosting! Please enter your organization name.")
        return




@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    """Send a dynamic reply to an incoming text message"""

    # Start our TwiML response
    resp = MessagingResponse()

    # Add a message so we can use message.number and message.text
    message = sender(request.values.get('From', None), request.values.get('Body', None))

    # If the user is a volunteer they text volunteer to our number
    if message.text == 'Volunteer':
        volunteer_prompt(message)
    
    # If the user is a volunteer they text volunteer to our number
    elif message.text == 'Host':
        host_prompt(message)
    
    # If the user hasnt typed either volunteer or host, they are prompted to do so
    else:
        message = "Please text Volunteer or Host"

    # Add a message
    resp.message(message)


    return str(resp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8080', debug=True)
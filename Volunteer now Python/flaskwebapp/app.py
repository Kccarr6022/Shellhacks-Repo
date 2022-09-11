from flask import Flask, request, redirect, render_template
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

class Message:
    def __init__(self, phone_number, text):
        self.phone_number = phone_number # string
        self.text = text # string

        #getters
        def get_phone_number(self):
            return self.phone_number

        def get_text(self):
            return self.text
        
        #setters
        def set_phone_number(self, phone_number):
            self.phone_number = phone_number
        
        def set_text(self, text):
            self.text = text

class Sender: # id = phone number
    def __init__(self, phone_number, first_text):
        self.phone_number = phone_number  #string
        self.__texts = [first_text]  #list of strings
        self.events = []  # list of strings)  
        
    #getters
    def get_phone_number(self):
        return self.phone_number
    
    def get_texts(self):
        return self.__texts
    
    #setters
    def set_phone_number(self, phone_number):
        self.phone_number = phone_number
    
    def append_text(self, text):
        self.__texts.append(text)


class Volunteer(Sender):
    """_summary_: We have our volunteer class, which will be used to store all the information about the volunteer.
    """
    def __init__(self):
        # initialize variables
        self.phone_number = ""
        self.full_name = None # string
        self.events = [] # list of strings
        self.hours = [] # list of ints

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
        self.phone_number = ""
        self.organization = None # string
        self.dates = [] # list of strings
        self.hours_available = [] # list of ints

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

senders = [ Sender("+19412501194", "Sender") ]
volunteers = [ Volunteer() ] # List of Volunteer Objects
hosts = [ Host() ] # List of Host Objects


def message_processing(recieved_message):
    """_summary_: This function will process the message that the user sends to the bot.
    if the message is a new number, we will add them to the list of senders and append their
    message in texts. If the message is not a new number, we will append the message to the list of texts.

    Args:
        message (_type_): A message containing the text and the number of the sender.
    """
    for sender in senders:
        # If the number is in the list of senders, we will append the message to the list of texts
        if recieved_message.phone_number == sender.get_phone_number():
            sender.append_text(recieved_message.text)
            return

    else:
        # If the number is not in the list of senders, we will add them to the list of senders and append their message in texts
        new_sender = Sender(recieved_message.phone_number, recieved_message.text)
        senders.append(new_sender)



def volunteer_prompt_response(sender, output_message):
    # If new number is not in the list of volunteers, add them to the list
    global volunteers

    # checks if volunteer has been added to the list
    for volunteer in volunteers:
        if sender.phone_number == volunteer.phone_number:
            
            if volunteer.full_name == None: # if name is not registered yet
                volunteer.full_name = sender.get_texts()[-1]
                return "Thank you for registering as a volunteer, " + volunteer.full_name + ". Please text the name of the event you would like to volunteer for." \
                    "1. YMCA \n 2. Food Bank \n 3. Habitat for Humanity \n 4. Other"
            elif volunteer.events == []: # name registered already
                    volunteer.events.append(sender.get_texts()[-1])
                    print (sender.get_texts()[-1])
                    return "How many hours will you be volunteering for"
            
            elif volunteer.hours == []:
                volunteer.hours.append(sender.get_texts()[-1])
                return "How many hours will you be volunteering for"
            elif volunteer.hours != None:
                volunteer.hours.append(sender.get_texts()[-1])
                body = ("You are attending currently attending {} for {} hours.".format("volunteer.events[-1]", "3"))
                return body
    else:
        
        # Create a new volunteer object
            volunteer = Volunteer()
            volunteer.phone_number = sender.phone_number
            volunteers.append(volunteer)
            return "Thank you for volunteering! Please enter your full name."
        
        

def host_prompt_response(sender, output_message):
    # If new number is not in the list of Hosts, add them to the list if they get approved by the admin
    global hosts

    for host in hosts:
        if sender.phone_number != host.phone_number:
            # Saves as sender object until approved by admin
            sender = Sender(sender.phone_number, sender.get_texts()[-1])
            senders.append(sender)

            return "Thank you for hosting! Please enter your organization name. After you have entered your " \
                "organization name, you will be contacted by an admin to verify your information."

    else:
        if sender.get_texts()[:-2] == "Host":

            return "Thank you for submitting your organization name. You will be " \
                "contacted by an admin to verify your information."

def add_host_promt_response(sender):
    global hosts
    pass;

def no_prompt_response(sender):
    return "Please text Volunteer or Host"

def main():
    while True:
        text_input = input("Enter a message: ")
        """Send a dynamic reply to an incoming text message"""
        global output_text
        # variables
        output_text = ""
        admin_numbers = {"19412501194"}
        current_sender = None

        # Start our TwiML response
        resp = MessagingResponse()

        # Add a message so we can use message.number and message.text
        recieved_message = Message("+19412501194", text_input)

        #  process the message (appends phone number to senders list and appends message to texts list)
        message_processing(recieved_message)

        # gets current sender
        for sender in senders:
            if sender.phone_number == recieved_message.phone_number:
                current_sender = sender

        # If the user is a volunteer they text volunteer to our number
        if "Volunteer" in current_sender.get_texts()[-4:] and "Host" not in current_sender.get_texts()[-2:]:
            output_text = volunteer_prompt_response(current_sender, output_text)
        
        # If the user is a volunteer they text volunteer to our number
        elif "Host" in current_sender.get_texts()[-2:] and "Volunteer" not in current_sender.get_texts()[-4:]:
            output_text = host_prompt_response(current_sender, output_text)
        
        elif 'Add Host' in current_sender.get_texts() and sender.phone_number in admin_numbers:
            output_text = add_host_promt_response(current_sender, output_text)
        # If the user hasnt typed either volunteer or host, they are prompted to do so
        else:
            output_text = no_prompt_response(current_sender)

        print(output_text)


@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    """Send a dynamic reply to an incoming text message"""
    global output_text
    # variables
    output_text = ""
    admin_numbers = {"19412501194"}
    current_sender = None

    # Start our TwiML response
    resp = MessagingResponse()

    # Add a message so we can use message.number and message.text
    recieved_message = Message(request.values.get('From', None), request.values.get('Body', None))

    #  process the message (appends phone number to senders list and appends message to texts list)
    message_processing(recieved_message)

    # gets current sender
    for sender in senders:
        if sender.phone_number == recieved_message.phone_number:
            current_sender = sender

    # If the user is a volunteer they text volunteer to our number
    if "Volunteer" in current_sender.get_texts()[-4:] and "Host" not in current_sender.get_texts()[-2:]:
        output_text = volunteer_prompt_response(current_sender, output_text)
    
    # If the user is a volunteer they text volunteer to our number
    elif "Host" in current_sender.get_texts()[-2:] and "Volunteer" not in current_sender.get_texts()[-4:]:
        output_text = host_prompt_response(current_sender, output_text)
    
    elif 'Add Host' in current_sender.get_texts() and sender.phone_number in admin_numbers:
        output_text = add_host_promt_response(current_sender, output_text)
    # If the user hasnt typed either volunteer or host, they are prompted to do so
    else:
        output_text = no_prompt_response(current_sender)

    resp.message(output_text)
    return str(resp)

if __name__ == "__main__":
   main()
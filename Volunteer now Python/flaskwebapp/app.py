from xmlrpc.client import DateTime
from flask import Flask, render_template, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from twilio.rest import Client
import logging
import os

account_sid = "AC9979a3d41a31d5acae3d55cf9a816529"
auth_token = "17d5401a2b667a9a8863b47d76cd66e5"
client = Client(account_sid, auth_token)
admin_numbers = ["+19412501194", "+19412671413"]

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
logging.getLogger("sqlalchemy.pool").setLevel(logging.DEBUG)


app = Flask(__name__,template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
# init database
db = SQLAlchemy(app)

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

class Message(db.Model):
    message_id = db.Column(db.Integer,primary_key=True)
    user_phone = db.Column(db.String(10),db.ForeignKey('volunteer.phone_num'))
    message = db.Column(db.String(500),nullable=False)

class Volunteer(db.Model):
    phone_num=db.Column(db.String(10),primary_key=True)
    name=db.Column(db.String(200),nullable=False)
    hours=db.Column(db.Integer,nullable=False)

class Event(db.Model):
    event_id=db.Column(db.Integer,primary_key=True)
    host_id=db.Column(db.Integer,nullable=False)
    date_created=db.Column(db.String(10), default=datetime.utcnow)
    date=db.Column(db.String(10),nullable=False)
    hours=db.Column(db.Integer,nullable=False)
    name=db.Column(db.String(200),nullable=False)
    location=db.Column(db.String(200),nullable=False)
    description=db.Column(db.String(500),nullable=False)

class Host(db.Model):
    host_id=db.Column(db.Integer,primary_key=True)
    phone_num=db.Column(db.String(10))
    organization=db.Column(db.String(200),nullable=False)
    def __repr__(self):
        return '<Name %r>' % self.organization
class Hosts(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    host_id=db.Column(db.Integer)
    event_id=db.Column(db.Integer)

class Attends(db.Model):
    attending_id=db.Column(db.Integer,primary_key=True)
    volunteer_num=db.Column(db.String(10),db.ForeignKey('volunteer.phone_num'))
    event_id=db.Column(db.Integer,db.ForeignKey('event.event_id'))

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
                return "Thank you for registering as a volunteer, " + volunteer.full_name + ". Please text the name of the" \
                    " organization you would like to volunteer for, our partnerships include\n" \
                    "1. YMCA \n2. Food Bank \n3. Habitat for Humanity \n4. Saint Jude's Hospital"
            elif volunteer.events == []: # name registered already
                    volunteer.events.append(sender.get_texts()[-1])
                    return "How many hours are you planning on attending?"
            
            elif volunteer.hours == []:
                volunteer.hours.append(sender.get_texts()[-1])
                return "See you at " + volunteer.events[0] + "!"
            elif volunteer.hours != None:
                volunteer.hours.append(sender.get_texts()[-1])
                body = ("You are attending currently attending {} for {} hours.".format("volunteer.events[-1]", "3"))
                return body
    else:
        
        # Create a new volunteer object
            volunteer = Volunteer()
            volunteer.phone_number = sender.phone_number
            volunteers.append(volunteer)
            return "Welcome to Volunteer Now! Please text your full name to register as a volunteer."
        
        

def host_prompt_response(sender, output_message):
    # If new number is not in the list of Hosts, add them to the list if they get approved by the admin
    global hosts

    for host in hosts:
        if sender.phone_number == host.phone_number:

            for phone_number in admin_numbers:
                message = client.messages \
                    .create(
                        body=sender.get_texts()[-1],
                        from_='+13329005194',
                        to=phone_number
                    )

                return "The admin has recieved your message and will soon get back with you."

    else:
    # Saves as sender object until approved by admin
        host = Host()
        host.set_phone_number(sender.phone_number)
        hosts.append(host)

        return "Thank you for hosting! Please enter your organization name. After you have entered your " \
            "organization name, you will be contacted by an admin to verify your information."


def add_host_promt_response(sender, output_text):

    # if there is a host focus on host
    for host in hosts:
        if sender.get_texts()[-4:] == host.get_phone_number(): # this would mean it is a host
            if host.organization == None:
                host.set_organization(sender.get_texts()[-1])
                return "Please enter the date of your event"
            elif host.dates == []:
                host.set_dates(sender.get_texts()[-1])
                return "Please enter the hours available at the event"
            elif host.hours_available == []:
                host.set_hours_available(sender.get_texts()[-1])
                return "Thank you for registering as a host!"


    # if the number entered isn't registed already then add it as a host
    for current in senders:
        print(current.get_phone_number())
        print(sender.get_texts())
        if str(current.get_phone_number) in sender.get_texts():
            hosts.append(current)
            return "Please text the neame of the organization"



    else:
        new_sender = Sender(sender.phone_number, sender.get_texts()[-1])
        return "Please enter the phone number of the organization you want to add. (Format: +1##########)"

def no_prompt_response(sender):
    return "Please text Volunteer or Host"

@app.route('/generate',methods=['POST','GET'])
def generate():
    msg=''

    host = [
    ['YMCA','2392759622']
    ,['Food Bank','2393347007']
    ,['Habitat for Humanity','2396520434']
    ,['Salvation Army','2392781551']
    ,['Goodwill','2399952106']
]
    try:
        elete=db.session.query(Host).delete()
        db.session.commit()
    except:
        db.session.rollback()
    for i in host:
        new_host = Host(organization=i[0],phone_num=i[1])
        try:
            db.session.add(new_host) # db.session.delete(user_to_delete)
            db.session.commit()
        except:
            print(f'error on {new_host.organization}')

    msg+= 'Generated Host '

    volunteer =[
        ['1235239837','Alex van der Meulen',2],
        ['4079872931','Kaden Carr', 25],
        ['9287441210','Ronald Chatalier',200]
    ]
    try:
        elete=db.session.query(Volunteer).delete()
        db.session.commit()
    except:
        db.session.rollback()
    for v in volunteer:
        new_volunteer=Volunteer(phone_num=v[0],name=v[1],hours=v[2])
        try:
            db.session.add(new_volunteer)
            db.session.commit()
        except:
            print(f'error on {new_volunteer.name}')
    msg+='\nVolunteer generated '
    try:
        elete=db.session.query(Event).delete()
        db.session.commit()
    except:
        db.session.rollback()

    try:
        elete=db.session.query(Attends).delete()
        db.session.commit()
        msg+='Generated Attends'
    except:
        db.session.rollback()

    try:
        elete=db.session.query(Hosts).delete()
        db.session.commit()
    except:
        db.session.rollback()



    event = [
        [1,	'2022-09-10',	'2022-09-10',	3,	'Program Volunteers',	'1360 Royal Palm Square Blvd, Fort Myers, FL 33919',	'Read to children in our Kids Zone, greet members at the membership services desk, coach one of our youth sports teams and more.'],
        [1, '2022-09-10',	'2022-09-10',	3,	'Special Event Volunteers',	'1360 Royal Palm Square Blvd, Fort Myers, FL 33919',	'In small groups or as individuals these volunteers perform tasks during a special event such as 5k races, Healthy Kids Day, or a golf tournament.']
    ]
    for e in event:
        try:
            new_event=Event(host_id=1,date=e[2],hours=e[3],name=e[4],location=e[5],description=e[6])
            db.session.add(new_event)
            db.session.commit()
            msg+='Generated Event'
        except:
            print('error generating event')
    
    
    return render_template('home.html',msg=msg)



@app.route('/add',methods=['POST','GET'])
def add():
    if request.method=="POST":
        name=request.form['name'] #form input name
        phone=request.form['phone']#
        new_host=Host(organization=name,phone_num=phone)
        print(new_host)
        try:
            db.session.add(new_host) # db.session.delete(user_to_delete)
            db.session.commit()
        except:
            print(f'error on {new_host.organization}')

        return render_template('add.html')

    else:
        return render_template('add.html')



@app.route('/addevent',methods=['POST','GET'])
def addevent():
    if request.method == "POST":
        try:
            host_id = Host.query.filter_by(organization=request.form['host']).first().host_id
            if host_id is not None:
                date=(request.form['date'])[:10] # date format issues...
                hours=request.form['hours']
                name=request.form['name']
                location=request.form['location']
                description=request.form['desc']
                new=Event(host_id=host_id,date=date,hours=hours,name=name,location=location,description=description)
                try:
                    db.session.add(new)
                    db.session.commit()
                    new_hosts_event=Hosts(host_id=new.host_id,
                    event_id=new.event_id)
                    db.session.add(new_hosts_event)
                    db.session.commit()
                except:
                    print(f'error on {new.name}')
        except:
            msg='No such organization!'
            return render_template('addevent.html',msg=msg)
    else:
        return render_template('addevent.html')

@app.route('/',methods=['POST','GET'])
def index():
    return render_template('login.html')

@app.route('/showevents',methods=['POST','GET'])
def showevents():
    hosts = Host.query.order_by(Host.host_id).all()
    names = []
    #print(hosts)
    events = db.session.query(Event,Host).filter(Event.host_id==Host.host_id)#Event.query.order_by(Event.date_created)

    return render_template("showevents.html",events=events)

@app.route('/attend/<int:id>')
def attend(id):
    volunteer_phone= '4079872931'

    #if not already attending...
    if Attends.query.filter(Attends.event_id==id,Attends.volunteer_num==volunteer_phone).count()==0:

        try:
            new_attends = Attends(volunteer_num=volunteer_phone,event_id=id)
            db.session.add(new_attends)
            db.session.commit()
        except:
            return 'error adding thing'
            
    else:
        return 'already attendintg'

    return redirect('/showevents') 

@app.route('/viewhistory/<int:id>')
def viewhistory(id):
    #return 'hi'
    if not id:
        id =1
    events = db.session.query(Event,Attends,Host).filter(Event.event_id==Attends.event_id,Host.host_id==Event.host_id,Attends.volunteer_num==id)
    for e,a,h in events:
        print(e.name,a.volunteer_num,h.organization)
    return render_template('viewhistory.html', events=events)

@app.route('/new')
def new():
    #colt steel
    events = db.session.query(Event,Attends,Host).filter(Event.event_id==Attends.event_id,Host.host_id==Event.host_id,Attends.volunteer_num=='4079872931')
    for e,a,h in events:
        print(e.name,a.volunteer_num,h.organization)
    return render_template('new.html', events=events)

@app.route('/data')
def data(): 
    events = db.session.query(Event,Host).filter(Event.host_id==Host.host_id)
    for e,h in events:
        print(f'e.name {e.name}')
    return render_template('data.html',events=events)

@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    """Send a dynamic reply to an incoming text message"""
    global output_text
    # variables
    output_text = ""
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

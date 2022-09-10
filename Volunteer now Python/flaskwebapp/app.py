from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    """Send a dynamic reply to an incoming text message"""
    # Get the message the user sent our Twilio number
    body = request.values.get('Body', None)

    # Start our TwiML response
    resp = MessagingResponse()

    # Users sees flier that says "Text 'Volunteer' to 123-456-7890 to volunteer"
    if body == 'Volunteer':
        resp.message("Question 1 (Yes/No") #Question 1
    elif body == 'Yes':
        resp.message("Which service appeals to you? \n1. YMCA") # List options for places to volunteer
    elif body == 'No':
        resp.message("Goodbye")
    elif body == '1':
        resp.message("Question 2 (Yes/No)")

    return str(resp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8080', debug=True)
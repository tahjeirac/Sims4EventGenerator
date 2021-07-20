import json
from flask import Flask, render_template, request, redirect, url_for, abort
import random
import Db
import smtplib
import ssl
import traceback
from email.message import EmailMessage
from datetime import date
import os
"""TODO:
   reszing issues, max number of emails --> keep track of messages -->packs included, try multipul times done!
"""
# first query fails
app = Flask(__name__)
is_prod = os.environ.get('IS_HEROKU', None)

if is_prod:
    app.config["DEBUG"] = os.environ.get('DEBUG')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    my_email = os.environ.get('my_email')
    password = os.environ.get('password')
else:
    import settings
    app.config["DEBUG"] = settings.DEBUG
    app.config['SECRET_KEY'] = settings.SECRET_KEY
    my_email = settings.my_email
    password = settings.password

choices = ''


@app.route('/', methods=('GET', 'POST'))
def home():
    data = request.args.to_dict()
    if data:
        if 'genFailure' in data:
            return render_template('home.html', showGenFail=True)
        elif 'displayFailure' in data:
            return render_template('home.html', showDisplayFail=True)

    return render_template('home.html')

# choose and display random event


@ app.route('/generate', methods=('GET', 'POST'))
def generate_event():
    chosen_events = Db.choose_events(choices)
    # from list of matching events, randomly choose and display one
    try:
        chosen_event = random.choice(chosen_events)
        # set events name, description, category, and whether the random number generator is needed
        event = chosen_event.get("event", "no event found")
        description = chosen_event.get(
            "description", "no description available")
        category = chosen_event.get("eventtype", "no category")
        roll_needed = chosen_event.get("rollneeded", "null")
        return render_template('home.html', event=event, description=description, category=category,
                               rollNeeded=roll_needed)
    except:
        return redirect(url_for('home', genFailure=True))


# get user filters and update 'choices' variable
@ app.route('/selection', methods=['POST'])
def get_post_javascript_data():
    jsdata = request.form['javascript_data']
    global choices
    choices = json.loads(jsdata)
    return 'Ok'


# get user suggestion and insert into database
@ app.route('/suggest', methods=['POST'])
def get_suggestion():
    try:
        jsdata = request.form['javascript_data']
        suggestion = json.loads(jsdata)
        Db.add_suggestion(suggestion)
        return 'Ok'
    except:
        return 'Bad'


@ app.route('/getEvents', methods=['GET'])
def get_events():
    try:
        events = Db.get_all()
        # change 0 to false and 1 to true
        names = ['deadly', 'rollneeded']
        for event in events:
            for name in names:
                if (event[name]):
                    event[name] = 'True'
                else:
                    event[name] = 'False'
        return render_template('displayAll.html', events=events)
    except:
        return redirect(url_for('home', displayFailure=True))


@ app.errorhandler(500)
def internal_error(err):
    email_message = 'Hi me, something went wrong, you should check it out: \n \n'
    email_message += traceback.format_exc()
    email_message += '\n \n Good luck :)'

    send_email('500', email_message)
    return render_template('500.html')


@ app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


def send_email(error, message_body):
    try:
        port = 465  # For SSL
        smtp_server = "smtp.gmail.com"

        msg = EmailMessage()
        msg['Subject'] = error
        msg['To'] = 'sims4events@gmail.com'
        msg.set_content(message_body)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(my_email, password)
            server.sendmail(my_email, my_email, msg.as_string())
        return 1
    except:
        return 0


if __name__ == '__main__':
    app.run()

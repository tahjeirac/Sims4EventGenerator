import json
import sqlite3
from flask import Flask, render_template, request
import random
import Db


"""TODO: Fix abs pos items to not overlap (setting buttons, footer,) add in error handling , fix suggestion failur/success, add error handling, done!
"""
app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SECRET_KEY'] = 'any secret string'

choices = ""



@app.route('/', methods=('GET', 'POST'))
def home():
    return render_template('home.html')

@app.route('/generate', methods=('GET', 'POST'))
def generate_event():

    chosen_event = Db.choose_event(choices)
    ##from list of matching options, randomly choose one
    try:
        print(chosen_event)
        chosen_event = random.choice(chosen_event)
        event = chosen_event.get("event", "no event found")
        description = chosen_event.get("description", "no description available")
        category = chosen_event.get("eventType", "no category")
        rollNeeded = chosen_event.get("rollNeeded", "null")
    except:
        print('nah')


    return render_template('home.html', title='random In', event = event, description = description, category = category, rollNeeded = rollNeeded)

#
# @app.route('/postmethod', methods = ['POST'])
# def get_post_javascript_data():
#     print("hello")
#     jsdata = request.form['javascript_data']
#     print(json.loads(jsdata)[0])

@app.route('/selection', methods = ['POST'])
def get_post_javascript_data():
    global choices
    jsdata = request.form['javascript_data']
    choices = json.loads(jsdata)
    return "OK"

@app.route('/suggest', methods = ['POST'])
def get_suggestion():
    jsdata = request.form['javascript_data']
    suggestion  = json.loads(jsdata)
    Db.add_suggestion(suggestion)
    print(suggestion)
    return "ok"
# @app.errorhandler(500)
# def page_not_found(e):
#     return render_template('home.html'), 500

if __name__ == '__main__':
    app.run()

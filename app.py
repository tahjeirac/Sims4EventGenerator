import json
from flask import Flask, render_template, request
import random
import Db

"""TODO: Fix abs pos items to not overlap (setting buttons, footer,) 
   add in error handling , fix suggestion failure/success, add error handling, done!
"""

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SECRET_KEY'] = 'any secret string'

choices = ''


@app.route('/', methods=('GET', 'POST'))
def home():
    return render_template('home.html')


# choose and display random event
@app.route('/generate', methods=('GET', 'POST'))
def generate_event():
    chosen_event = Db.choose_events(choices)

    # from list of matching events, randomly choose and display one
    try:
        chosen_event = random.choice(chosen_event)
        # set events name, description, category, and whether the random number generator is needed
        event = chosen_event.get("event", "no event found")
        description = chosen_event.get("description", "no description available")
        category = chosen_event.get("eventType", "no category")
        roll_needed = chosen_event.get("rollNeeded", "null")
    except:
        print('nah')

    return render_template('home.html', event=event, description=description, category=category,
                           rollNeeded=roll_needed)


# get user filters and update 'choices' variable
@app.route('/selection', methods=['POST'])
def get_post_javascript_data():
    jsdata = request.form['javascript_data']
    global choices 
    choices = json.loads(jsdata)
    return 'OK'


# get user suggestion and insert into database
@app.route('/suggest', methods=['POST'])
def get_suggestion():
    jsdata = request.form['javascript_data']
    suggestion = json.loads(jsdata)
    Db.add_suggestion(suggestion)
    return 'OK'


if __name__ == '__main__':
    app.run()

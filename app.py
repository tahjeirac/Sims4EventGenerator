import json
import sqlite3
from flask import Flask, render_template, request
import random
import Db


"""TODO: Fix apperance, add more filtering option (by pack, category), 
start off category checkboxes with all chekced by default (create all button)
change it so not having one section checked doesnt unchechk all
update methods to jquery so no resetting data
figure out .then for ajax to open generate
see if using ajax makes sense for generate ("commente out as template not working)"""

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SECRET_KEY'] = 'any secret string'

choices = ""



@app.route('/', methods=('GET', 'POST'))
def home():
    return render_template('home.html')

@app.route('/generate', methods=('GET', 'POST'))
def generate_event():
    # conn = sqlite3.connect('events.db')
    # conn.row_factory = dict_factory
    # cur = conn.cursor()
    # deathIncluded = choices['deaths']
    # print(choices)
    # ##add in error handling for if none exist
    # packs = ["Basegame"]
    # type = []
    # z = 0
    # y = 0
    # for key in choices:
    #     if (key == 'Household Events' or z == 1):
    #         z = 1
    #         if (choices[key] == True):
    #             type.append(key)
    #     if (key == 'Basegame' or y == 1):
    #         y = 1
    #         if (choices[key] == True):
    #             packs.append(key)
    # with conn:
    #     # if (not deathIncluded):
    #     #     cur.execute("""SELECT * FROM Sims4Test WHERE event IN
    #     # (SELECT event FROM Sims4Test ORDER BY RANDOM() LIMIT 1) AND deadly = "0" """)
    #     # else:
    #     #     cur.execute("""SELECT * FROM Sims4Test WHERE event IN
    #     #            (SELECT event FROM Sims4Test ORDER BY RANDOM() LIMIT 1) AND event_type = "Career" """)
    #     #cur.execute("""SELECT * FROM Sims4Test WHERE event_type = ? ; """, ("Career",))
    #     cur.execute('SELECT * FROM Sims4Test WHERE packsNeeded IN ({}) AND event_type IN ({})'
    #                 .format((', '.join(['?'] * len(packs))), ', '.join(['?'] * len(type))), [*packs, *type])
    #     chosen_event = cur.fetchall()

    chosen_event = Db.choose_event(choices)
    ##from list of matching options, randomly choose one
    chosen_event = random.choice(chosen_event)
    event = chosen_event.get("event", "no event found")
    description = chosen_event.get("description", "no description available")
    category = chosen_event.get("eventType", "no category")


    return render_template('home.html', title='random In', event = event, description = description, category = category)

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
    choices  = json.loads(jsdata)
    return "OK"

if __name__ == '__main__':
    app.run()

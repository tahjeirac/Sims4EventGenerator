import sqlite3
#TODO: Fix apperance, add more filtering option (by pack, category), make it so page does not onstantly refresh and reset chosen checks
from flask import Flask, render_template, request

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SECRET_KEY'] = 'any secret string'


def dict_factory(cursor, row):
    d = {}
    # ennumerate has built in counter
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/')
def hello_world():
   return render_template('home.html')

@app.route('/generate', methods=('GET', 'POST'))
def generate_event():
    conn = sqlite3.connect('events.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    deathIncluded = str((request.args.get('deaths')))


    with conn:
        if (not deathIncluded):
            cur.execute("""SELECT * FROM Sims4Test WHERE event IN 
        (SELECT event FROM Sims4Test ORDER BY RANDOM() LIMIT 1) AND deadly = "0" """)
        else:
            cur.execute("""SELECT * FROM Sims4Test WHERE event IN 
                   (SELECT event FROM Sims4Test ORDER BY RANDOM() LIMIT 1) """)
        chosen_event = cur.fetchone()

    event = chosen_event.get("event", "no event found")
    description = chosen_event.get("description", "no description available")
    category = chosen_event.get("event type", "no category")

    return render_template('displayEvents.html', title='random In', event = event, description = description, category = category)




if __name__ == '__main__':
    app.run()

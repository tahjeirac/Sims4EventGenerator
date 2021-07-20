import psycopg2
import psycopg2.extras
from psycopg2 import sql

import os
is_prod = os.environ.get('IS_HEROKU', None)

if is_prod:
    MY_ENV_VAR = os.environ.get('DATABASE_URL')
else:
    from dotenv import load_dotenv
    load_dotenv()
    MY_ENV_VAR = os.getenv('DATABASE_URL')

conn = psycopg2.connect(MY_ENV_VAR, sslmode='require')


def dict_factory(cur, row):
    d = {}
    for idx, col in enumerate(cur.description):
        d[col[0]] = row[idx]
    return d


# get list of events matching user filter
def choose_events(filters):
    # always include basegame
    packs = ["Basegame"]
    categories = []
    # always include non-deadly events
    death = ['0']

    z = 0
    y = 0

    for key in filters:
        # add household events and anything after to categories array
        if (key == 'Household Events' or z == 1):
            z = 1
            if filters[key]:
                categories.append(key)

        # add pets and and anything after to pack array, until household events
        elif (key == 'Pets' or y == 1):
            y = 1
            if filters[key]:
                packs.append(key)
    try:
        death_included = filters['deaths']
    except:
        death_included = False

    # if user wants deadly events, add '1' to array
    if death_included:
        death.append('1')

    try:
        deadly = array_to_tuple(death)
        packs = array_to_tuple(packs)
        eventType = array_to_tuple(categories)
        q = '''SELECT * FROM events WHERE deadly IN %s AND eventtype IN %s AND packsneeded IN %s;'''
        records = query(q, True, deadly, eventType, packs)
        return records
    except ValueError as er:
        raise ValueError('Getting Events Failed', er)

    # get matching events from database


def array_to_tuple(array):
    return tuple(array)

# send user suggestion to database


def add_suggestion(suggestion):
    death = str(suggestion['death'])
    roll = str(suggestion['roll'])
    description = str(suggestion['description'])
    event_name = str(suggestion['eventName'])
    category = str(suggestion['category'])
    email = str(suggestion['email'])

    try:
        q = sql.SQL("INSERT INTO suggestions VALUES (%s, %s, %s, %s, %s, %s)")
        query(q, False, event_name, description, category, death, roll, email)
    except ValueError as er:
        raise ValueError('Adding Suggestion Failed')


def get_all():
    try:
        select_Query = 'SELECT * FROM events'
        records = query(select_Query, True)
        return records
    except ValueError as er:
        raise ValueError('Getting all Failed')


def query(query, toReturn, *args):
    try:
        with conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                if (args):
                    if (len(args) == 3):
                        cur.execute(query, (args[0], args[1], args[2]))
                    if (len(args) == 6):
                        cur.execute(
                            query, (args[0], args[1], args[2], args[3], args[4], args[5]))
                else:
                    cur.execute(query)
                if (toReturn):
                    records = cur.fetchall()
                    return records
                else:
                    return
    except psycopg2.Error as er:
        raise ValueError('Query Failed', er)

import psycopg2
import psycopg2.extras
from psycopg2 import sql

from os import X_OK
import sqlite3

import os
from dotenv import load_dotenv
load_dotenv()
MY_ENV_VAR = os.getenv('DATABASE_URL')


# print(os.environ['DATABASE_URL'])
# DATABASE_URL = '''postgres://uocxcaticgpkmx:ec6e51c93109770140d42e5ce0a2ee45a57422ad1f232b284286690534fb5755@ec2-35-174-35-242.compute-1.amazonaws.com:5432/d4c8hl59oajso0'''

conn = psycopg2.connect(MY_ENV_VAR, sslmode='require')


# return sqlite objects as dict


def dict_factory(cur, row):
    d = {}
    for idx, col in enumerate(cur.description):
        d[col[0]] = row[idx]
    return d


# get list of events matching user filter
def choose_events(filters):
    conn = sqlite3.connect('events.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    # always include basegame
    packs = ["Basegame"]
    categories = ['Illness']
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

        records = query(q, deadly, eventType, packs)
        return records
    except psycopg2.Error as er:
        raise ValueError('Getting Events Failed')

    # get matching events from database


# format IN with array
def db_formatting(array):
    return ', '.join(['?'] * len(array))


def array_to_tuple(array):
    return tuple(array)
    # send user suggestion to database


def add_suggestion(suggestion):
    conn = sqlite3.connect('events.db')
    cur = conn.cursor()
    conn.row_factory = dict_factory

    death = suggestion['death']
    roll = suggestion['roll']
    description = suggestion['description']
    event_name = suggestion['eventName']
    category = suggestion['category']
    email = suggestion['email']
    try:
        with conn:
            cur.execute("INSERT INTO suggestions VALUES (:eventName,:description, :category, :deadly,:rollNeeded, :email)",
                        {'eventName': event_name, 'description': description, 'category': category,
                         'deadly': death, 'rollNeeded': roll, 'email': email})
    except sqlite3.Error as er:
        raise ValueError('Adding Suggestion Failed')


def check_emails():
    conn = sqlite3.connect('events.db')
    cur = conn.cursor()
    conn.row_factory = dict_factory

    try:
        with conn:
            cur.execute('''SELECT * FROM emails WHERE date IN ({})
                            AND eventType IN ({}) AND deadly IN ({}) ''')
    except sqlite3.Error as er:
        raise ValueError('Adding Suggestion Failed')


# connection
def get_all():
    try:
        select_Query = 'SELECT * FROM events'
        records = query(select_Query)
        return records
    except psycopg2.Error as er:
        raise ValueError('Getting all Failed')


def query(query, *args):
    try:
        with conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                if (args):
                    cur.execute(query, (args[0], args[1], args[2]))
                else:
                    cur.execute(query)
                records = cur.fetchall()
                return records
    except psycopg2.Error as er:
        raise ValueError('Query Failed')

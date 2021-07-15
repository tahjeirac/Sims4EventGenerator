from os import X_OK
import sqlite3


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
    print('FILTERTS', filters)
    death_included = filters['deaths']
    # if user wants deadly events, add '1' to array
    if death_included:
        death.append('1')

    # get matching events from database
    try:
        with conn:
            cur.execute('''SELECT * FROM Sims4Events WHERE packsNeeded IN ({}) 
                            AND eventType IN ({}) AND deadly IN ({}) '''
                        .format(db_formatting(packs), db_formatting(categories), db_formatting(death)),
                        [*packs, *categories, *death])
            chosen_events = cur.fetchall()
        return chosen_events
    except sqlite3.Error as er:
        print(er)
        return 0


# format IN with array
def db_formatting(array):
    return ', '.join(['?'] * len(array))


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

    try:
        with conn:
            cur.execute("INSERT INTO suggestions VALUES (:eventName,:description, :category, :deadly,:rollNeeded)",
                        {'eventName': event_name, 'description': description, 'category': category,
                         'deadly': death, 'rollNeeded': roll})
    except sqlite3.Error as er:
        print(er)
        raise ValueError('Adding Suggestion Failed')

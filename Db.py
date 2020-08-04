import sqlite3


def dict_factory(cursor, row):
    d = {}
    # ennumerate has built in counter
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def choose_event (filters):
    conn = sqlite3.connect('events.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    deathIncluded = filters['deaths']
    ##add in error handling for if none exist
    packs = ["Basegame"]
    type = []
    death = ['0']
    z = 0
    y = 0
    for key in filters:
        if (key == 'Household Events' or z == 1):
            z = 1
            if (filters[key] == True):
                type.append(key)
        elif (key == 'Pets' or y == 1):
            y = 1
            if (filters[key] == True):
                packs.append(key)

    if deathIncluded:
        death.append('1')
    print(death)

    #might not need with conn, close connection??
    with conn:
        ##make formatting cleaner
        cur.execute('''SELECT * FROM Sims4Events WHERE packsNeeded IN ({}) 
                        AND eventType IN ({}) AND deadly IN ({}) '''
                    .format((', '.join(['?'] * len(packs))),(', '.join(['?'] * len(type))), (', '.join(['?'] * len(death)))), [*packs, *type, *death])
        chosen_events = cur.fetchall()

    return chosen_events

def add_suggestion(suggestion):
    #automatically commits or rolls back (if eexception) connections
    conn = sqlite3.connect('events.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    death = suggestion['death']
    roll = suggestion['roll']
    description = suggestion['description']
    eventName = suggestion['eventName']
    category = suggestion['category']

    with conn:
        cur.execute("INSERT INTO suggestions VALUES (:eventName,:description, :category, :deadly,:rollNeeded)",
                    {'eventName': eventName,'description':description, 'category': category,
                     'deadly': death, 'rollNeeded': roll})
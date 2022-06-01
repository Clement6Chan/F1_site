import sqlite3
from datetime import datetime
import json
import random
import string

DB_FILE = "app/data/database.db"

def getNextID(type):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    arr = c.execute("SELECT MAX (id) FROM {};".format(type)).fetchall()
    print(arr)
    if arr[0][0] == None:
        return 0
    return int(arr[0][0]) + 1

#################LAPTIMES#####################
def getBestTimes(track_arr):
    best_times = []
    for track_name in track_arr:
        arr = getTrackLapTime(track_name)
        if len(arr) == 0:
            best_times.append([-1, track_name, -1, 0, 0, '---', '---', '---', '---', '---'])
        else:
            best_times.append(arr[0])
    return best_times


def getTrackLapTime(track_name):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    arr = c.execute('SELECT * FROM laptimes WHERE track_name=\"{}\" ORDER BY sec,mili ASC'.format(track_name)).fetchall()
    return arr

def addLapTime(form, userID):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    arr = c.execute('SELECT * FROM laptimes WHERE track_name = \"{}\" AND user_id ={} AND traction=\"{}\" '
                    'AND gearbox=\"{}\" AND braking=\"{}\" AND car = \"{}\"'
                    .format(form['track'], userID, form['traction'], form['gearbox'], form['braking'], form['car'])).fetchall()
    print(arr)
    entryID = 0
    if(len(arr) != 0):
        ####times not faster#####
        if int(form['seconds']) > arr[0][3]:
            return 1
        elif int(form['seconds']) == arr[0][3] and int(form['ms']) >= arr[0][4]:
            return 1
        c.execute('DELETE FROM laptimes WHERE user_id ={} AND traction=\"{}\" AND gearbox=\"{}\" '
                  'AND braking=\"{}\"'.format(userID, form['traction'], form['gearbox'], form['braking']))
        entryID = arr[0][0]
        #entryID = getNextID("laptimes")
    else:
        entryID = getNextID("laptimes")
    c.execute('INSERT INTO laptimes(id, track_name, user_id, sec, mili, traction, gearbox, braking, car, date_entered)'
              'VALUES({},\"{}\",{},{},{},\"{}\",\"{}\",\"{}\",\"{}\",\"{}\")'
              .format(entryID, form['track'], userID, form['seconds'], form['ms'], form['traction'], form['gearbox'],
                      form['braking'], form['car'], datetime.now().strftime("%m/%d/%y")))
    db.commit()
    return 0 #success


#################GET Name ID####################

def get_track_ID(track_name):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    arr = c.execute('SELECT id FROM tracks WHERE track_name=\"{}\";'.format(track_name)).fetchall()
    if len(arr) == 0:
        return -1
    return arr[0][0]

def get_track_name(id):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    arr = c.execute('SELECT track_name FROM tracks WHERE id=\"{}\";'.format(id)).fetchall()
    return arr[0][0]

def get_user_ID(username):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    arr = c.execute('SELECT id FROM users WHERE username=\"{}\";'.format(username)).fetchall()
    return arr[0][0]

def get_user_name(id):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    arr = c.execute('SELECT username FROM users WHERE id=\"{}\";'.format(id)).fetchall()
    if len(arr) == 0:
        return '---'
    return arr[0][0]



#################ACCOUNTS####################
def authUser(user,password):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    arr = c.execute('SELECT * FROM users WHERE username=\"{}\";'.format(user)).fetchall()
    if len(arr) == 0:
        return False
    elif arr[0][2] != password:
        return False
    return True

def newAccount(user,password,password1):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    arr = c.execute('SELECT * FROM users WHERE username=\"{}\"'.format(user)).fetchall()
    if len(arr) > 0:
        return 5 #Username in use
    elif password != password1:
        return 6 #Passwords do not match
    c.execute('INSERT INTO users(id, username, password) '
              'VALUES({},\"{}\",\"{}\");'.format(getNextID("users"), user, password))
    db.commit()
    return 4 #Account created - Please Log In

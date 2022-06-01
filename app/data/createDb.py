import sqlite3

DB_FILE = "database.db"
db = sqlite3.connect(DB_FILE)
c = db.cursor()
c.execute('CREATE TABLE IF NOT EXISTS users(id integer, username text, password text);')
c.execute('CREATE TABLE IF NOT EXISTS tracks(id integer, track_name text);')
c.execute('CREATE TABLE IF NOT EXISTS laptimes(id integer, track_name text, user_id integer, sec integer, '
          'mili integer, traction text, gearbox text, braking text, car text, date_entered text);')

track_names = ['Bahrain','Imola','Portugal','Spain','Monaco','Azerbaijan','Canada','France','Austria','Britain',
               'Hungary','Belgium','Netherlands','Italy','Russia','Singapore','Japan','USA','Mexico','Brazil',
               'Australia','Saudi Arabia','Abu Dhabi','China']
for i in range (24):
    c.execute('INSERT INTO tracks(id, track_name) VALUES({},\"{}\");'.format(i,track_names[i]))

db.commit()

'''
arr = c.execute("SELECT * FROM tracks;").fetchall()
for row in arr:
    print(row)
'''
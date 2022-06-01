from app.data.dbfunc import *

DB_FILE = "data/database.db"
db = sqlite3.connect(DB_FILE)
c = db.cursor()

print(get_track_ID('Brazil'))

c.execute('INSERT INTO laptimes(track_id, user_id, sec, mili,traction, gearbox, braking, car) '
          'VALUES({},{},{},{},{},{},{},\"{}\");'.format(1,0,23,320,0,1,0,'Mercedes'))

db.commit()


arr = c.execute('SELECT * FROM laptimes;').fetchall()
print(arr)
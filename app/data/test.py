from app.data.dbfunc import *

DB_FILE = "database.db"
db = sqlite3.connect(DB_FILE)
c = db.cursor()

#print(get_track_ID('Brazil'))

#c.execute('INSERT INTO laptimes(track_id, user_id, sec, mili,traction, gearbox, braking, car) '
          #'VALUES({},{},{},{},{},{},{},\"{}\");'.format(1,0,23,320,0,1,0,'Mercedes'))
#db.commit()

track_arr = ["Bahrain", "Imola", "Portugal", "Spain", "Monaco", "Azerbaijan", "Canada", "France", "Austria",
                "Britain", "Hungary", "Belgium", "Netherlands", "Italy", "Russia", "Singapore", "Japan",
                "USA", "Mexico", "Brazil", "Australia", "Saudi Arabia", "Abu Dhabi", "China"]

#arr = c.execute('SELECT * FROM laptimes;').fetchall()
best_times = []

'''
arr = c.execute('SELECT * FROM laptimes ORDER BY track_name ASC, sec ASC, mili ASC;').fetchall()

for i in range(len(track_arr) - 1):
    arr = c.execute('SELECT * FROM laptimes WHERE track_name = \"{}\" ORDER BY sec ASC, mili ASC;'.format(track_arr[i])).fetchall()
    if(len(arr) != 0):
        best_times.append(arr[0])
    else:
        best_times.append([-1, track_arr[i], -1, 0, 0, '---', '---', '---', '---', '---'])

for b in best_times:
    print(b)
    
    '''

track_arr = ["Bahrain", "Imola", "Portugal", "Spain", "Monaco", "Azerbaijan", "Canada", "France", "Austria",
                "Britain", "Hungary", "Belgium", "Netherlands", "Italy", "Russia", "Singapore", "Japan",
                "USA", "Mexico", "Brazil", "Australia", "Saudi Arabia", "Abu Dhabi", "China"]

car_arr = ["Mercedes", "Red Bull", "Ferrari", "McClaren", "Alpine", "Alpha Tauri", "Alfa Romeo",
                "Aston Martin", "GUENTHER", "Williams", "Multiplayer Car"]

traction_arr = ["High", "Med","Low","Off"]

gearbox_arr = ["Auto","Manual"]

braking_arr = ["High", "Med","Low","Off w/ ABS", "Off wo/ ABS"]

big_data = {}
big_data['track'] = track_arr
big_data['traction'] = traction_arr
big_data['gearbox'] = gearbox_arr
big_data['braking'] = braking_arr
big_data['car'] = car_arr

print(big_data)
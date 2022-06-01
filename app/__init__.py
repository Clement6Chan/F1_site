from flask import Flask, request, redirect, session, render_template, url_for, flash
import os, platform, json
from app.data.dbfunc import *

key = ""
UPLOAD_FOLDER = ""

if (platform.system() == "Windows"):
    UPLOAD_FOLDER = os.getcwd() + "\\app\\static\\images"
elif (platform.system() == "Darwin" or platform.system() == "Linux"):
        UPLOAD_FOLDER = 'static/images/'

app = Flask(__name__)
app.secret_key = os.urandom(32)
# UPLOAD_FOLDER = './static/images/'
app.config['IMAGE_UPLOADS'] = UPLOAD_FOLDER
mType = 0
app.jinja_env.globals.update(get_user_name=get_user_name)

@app.route('/')
def hello_world():
    t =  datetime.now().strftime("%m/%d/%Y")
    print([t])
    if 'username' in session:
        return redirect(url_for('home'))
    return render_template('landing.html')

@app.route('/home')
def home():
    if 'username' not in session:
        return redirect('/')
    global mType
    if mType == 0:
        return render_template('home.html')
    elif mType == 1:
        mType = 0
        return render_template('home.html', success="Logged In")
    elif mType == 2:
        mType = 0
        return render_template('landing.html', success="Logged Out")

    return render_template('home.html')

#################CORE####################
@app.route('/tracks')
def tracks():
    print(session)
    return render_template('tracklist.html')

@app.route('/tracks/<track_name>', methods=['GET', 'POST'])
def track_view(track_name):
    global mType
    print(session)
    id = get_track_ID(track_name)
    if(id == -1):
        return render_template('track_view.html', t_name="Invalid track name")

    arr = getTrackLapTime(track_name)
    for x in arr:
        print(x)
    if request.method == 'GET':
        if(mType == 7):
            mType = 0
            return render_template('track_view.html', t_name=track_name, success="Lap Time Added", arr=arr)
        return render_template('track_view.html', t_name=track_name, arr=arr)
    else:
        x = request.form
        print(x)
        user = request.form['user']
        traction = request.form['traction']
        braking = request.form['braking']
        gearbox = request.form['gearbox']
        return render_template('track_view.html', t_name=track_name, arr=arr, selections=request.form, alert="filters not implemented")

@app.route('/users')
def users():
    return render_template('users.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/addEntry', methods=['GET', 'POST'])
def addEntry():
    '''
    if 'username' not in session:
        return redirect('/')
        '''
    if request.method == 'GET':
        return render_template('entry.html')
    else:
        global mType
        x = request.form
        print(x)
        print(session)
        track_name = request.form['track']

        x = addLapTime(request.form, get_user_ID(session['username']))
        #print("add result: " + str(x))
        if(x == 1):
            return render_template('entry.html', alert="Faster laptime in this configuration exists", arr=request.form)
        mType = 7
        session['entry'] = request.form
        return redirect('tracks/' + track_name)


#################ACCOUNTS####################
@app.route('/login', methods=['GET', 'POST'])
def login():
    global mType
    if request.method == 'GET':
        if mType == 0:
            return render_template('login.html')
        elif mType == 3:
            mType = 0
            return render_template('login.html', alert="Username or Password incorrect")
        elif mType == 4:
            mType = 0
            return render_template('login.html', success="Account Created - Please Log In")
        else:
            mType = 0
            return render_template('login.html', alert="?")
    else:
        eUser = request.form['username']
        ePass = request.form['password']
        if not authUser(eUser, ePass):
            mType = 3
            return redirect(url_for('login'))
        session['username'] = eUser
        mType = 1 #Logged In
        return redirect(url_for('home'))


@app.route('/logOut')
def logOut():
    global mType
    session.pop('username')
    mType = 2 #logged out
    return redirect(url_for('home'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    global mType
    if request.method == 'GET':
        if mType == 0:
            return render_template('register.html')
        elif mType == 5:
            mType = 0
            return render_template('register.html', alert="Username in use")
        elif mType == 6:
            mType = 0
            return render_template('register.html', alert="Passwords do not match")
        else:
            mType = 0
            return render_template('register.html', alert="?")
    else:
        print(request.form)
        user = request.form['username']
        pass0 = request.form['password']
        pass1 = request.form['password-repeat']
        mType = newAccount(user, pass0, pass1)
        if (mType != 4):
            return redirect(url_for('register'))
        return redirect(url_for('login'))



if __name__ == "__main__":
    app.debug = True
    app.run()

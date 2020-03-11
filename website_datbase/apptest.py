from forms import Registration, log_in_form
from flask import Flask, render_template, url_for, flash, redirect
import pyrebase
from getpass import getpass


firebaseConfig = {
    "apiKey" : "AIzaSyA_FK4WL3wS1Cy7WOiDA71IP-m2SYwXJv8",
    "authDomain" : "big-brother-b8f63.firebaseapp.com",
    "databaseURL" : "https://big-brother-b8f63.firebaseio.com",
    "projectId" : "big-brother-b8f63",
    "storageBucket" : "big-brother-b8f63.appspot.com",
    "messagingSenderId" : "445901799408",
    "appId" : "1:445901799408:web:696967fb3a0871e9f16735",
    "measurementId" : "G-22J582W7SC"
  }

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()
app = Flask(__name__)

app.config['SECRET_KEY'] = 'bT4YXj2gdI7jAzEJQVuuYO4KsgEU14H5'

# message="/Classroom%201"
# def stream_handler(message):
#    print(message)
# my_stream = db.child("/Classroom%201").stream(stream_handler)


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html',)


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = Registration()
    if form.validate_on_submit():
        flash(f'Account Created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('user_reg.html', title='Register', form=form)


@app.route("/log_in")
def log_in():
    form = log_in_form()
    return render_template('user_login.html', title='Login', form=form)


@app.route("/roster", methods=['GET', 'POST'])
def roster():
    # print(message["event"])
    # print(message["/Classroom%201"])
    # print(message["data"])
    # my_stream = db.child("posts").stream(stream_handler)
    # return render_template('roster.html', events=my_stream)
    # db_temp = db.child("/Classroom%201/1st%20Period").get().val()
    db_temp = db.child("/Classroom%201/1st%20Period").get().val().items()
    return render_template('roster.html', events=db_temp)

if __name__ == '__main__':
    app.run(debug=True)
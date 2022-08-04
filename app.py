from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase



config = {
  "apiKey": "AIzaSyA_cycsH9cx7SonxowXgfzUa9mfr0rSzuA",
  "authDomain": "project-firebase-66130.firebaseapp.com",
  "projectId": "project-firebase-66130",
  "storageBucket": "project-firebase-66130.appspot.com",
  "messagingSenderId": "1090676868452",
  "appId": "1:1090676868452:web:9f3af260c9a25616d6e671",
  "measurementId": "G-XKQ6HTJW4V",
  "databaseURL": "https://project-firebase-66130-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email,password)
            return redirect(url_for('home'))
        except:
            error = "Error with signing up"
    return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = {"email": request.form['email'],"password": request.form['password'],"full_name": request.form['full_name'],"username": request.form['username']}
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email,password)
            db.child("Users").child(login_session['user']['localId']).set(user)
            login_session['inside'] = True
            return redirect(url_for('home'))
        except:
            error = "Error with signing up"
    return render_template("signup.html", error = error)



@app.route('/', methods = ['GET', 'POST'])
def home():
    error = ""
    logged_out = login_session['user'] is None
    if request.method == 'POST':
        name = request.form['Name']
        email = request.form['Email']
        subject = request.form['Subject']
        message = request.form['Message']
        feedback = {"name": name, "email_feedback": email, "subject": subject, "message": message}
        try:
            db.child("Users").child(login_session['user']['localId']).child("feedbacks").push(product)
            return render_template("testProject.html")
        except:
            error = "There was an error"
    return render_template("testProject.html", logged_out = logged_out)


counter = 0
@app.route('/store', methods = ['GET', 'POST'])
def store():
    error = ""
    if request.method == 'POST':
        product = {"quantity": 1, "price": 150}
        img = request.form['img']
        title = request.form['title']
        price = request.form['price']
        description = request.form['description']
        suit = {"img": img, "title": title, "price": price, "description": description, "amount": counter}
        try:
            #all_suits = {"suit1": {"img": "buy1.jpg", "title": "Slim-Fit Suit", "price": "150$", "description": "98% Virgin Wool 2% Lastane"}, "suit2": {"img": "buy2.jpg", "title": "Regular Classic Pocket", "price": "50$", "description": "Light Blue Black Wine Khaki Navy Blue Business Daily"}, "suit3": {"img": "buy3.jpg", "title": "Slim-Fit Suit Jacket", "price": "315$", "description": "True to size, choose your normal size"} }
            #for item in db.child("Users").child(login_session['user']['localId']).child("cart").get().val():
                #if item['title'] == suit['title']:
            suit['amount'] = suit['amount'] + 1
            #db.child("Users").child(login_session['user']['localId']).child("cart").update(suit)
                #else:
            db.child("Users").child(login_session['user']['localId']).child("cart").push(suit)
            return redirect(url_for('cart'))
        except:
            error = "adding failed"
    return render_template("store.html", user = db.child("Users").child(login_session['user']['localId']).get().val(), all_suits = {"suit1": {"img": "static/buy1.jpg", "title": "Slim-Fit Suit", "price": 150, "description": "98% Virgin Wool 2% Lastane"}, "suit2": {"img": "static/buy2.jpg", "title": "Regular Classic Pocket", "price": 50, "description": "Light Blue Black Wine Khaki Navy Blue Business Daily"}, "suit3": {"img": "static/buy3.jpg", "title": "Slim-Fit Suit Jacket", "price": 315, "description": "True to size, choose your normal size"} })



@app.route('/cart', methods = ['GET', 'POST'])
def cart():
    all_suits = {"suit1": {"img": "buy1.jpg", "title": "Slim-Fit Suit", "price": 150, "description": "98% Virgin Wool 2% Lastane", "amount": 1},
    "suit2": {"img": "buy2.jpg", "title": "Regular Classic Pocket", "price": 50, "description": "Light Blue Black Wine Khaki Navy Blue Business Daily", "amount": 0},
    "suit3": {"img": "buy3.jpg", "title": "Slim-Fit Suit Jacket", "price": 315, "description": "True to size, choose your normal size", "amount": 0}}
    print(db.child("Users").child(login_session['user']['localId']).child("cart").get().val())
    return render_template("cart.html", all_suits = all_suits, suits = db.child("Suits").get().val(), cart = db.child("Users").child(login_session['user']['localId']).child("cart").get().val())


@app.route('/signout')
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
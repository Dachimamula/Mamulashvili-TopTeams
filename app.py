#https://dachimamula.pythonanywhere.com/login

from flask import Flask, redirect, url_for, render_template, request, session, flash, get_flashed_messages
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'asbai3q4qova234rdf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///games.sqlite'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

class games(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    team = db.Column(db.String(30), nullable=False)
    goals = db.Column(db.Float, nullable=False)
    rating = db.Column(db.Float, nullable=False)


# with app.app_context():
    # db.create_all()

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/user')
def user():
    footballers = ['Mamardashvili', 'Kvaratskhelia', 'Zivzivadze', 'Miqautadze', 'Kochorashvili']
    return render_template('user.html', footballers=footballers)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        p = request.form['password']
        session['username'] = user
        return redirect('/user')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return render_template('logout.html')

@app.route('/games')
def game():
    if 'Team' in request.args:
        t = request.args['team']
        g = request.args['goals']
        r = request.args['rating']
        if t == ' ' or g == '' or r == '':
            flash('Please enter team, goal and rating values', 'error')
        elif not g.isdecimal() or not r.isdecimal():
            flash('goals and rating must be float.', 'error')
        else:
            t1 = games(team=t, goals=float(g), rating=float(r))
            db.session.add(t1)
            db.session.commit()
            flash('team added!', 'info')
    return render_template('games.html')


@app.route('/allgames')
def allgames():
    all_games = games.query.all()
    return render_template('allgames.html', all_games=all_games)

if __name__ == '__main__':
    app.run(debug=True)

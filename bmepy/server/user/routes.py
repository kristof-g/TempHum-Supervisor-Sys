import sys

from flask import Blueprint, render_template, session, redirect, request, url_for

from server import db
from server.user.model import User
from server.helpers import pwIsValid, LoginRequired

app = sys.modules['__main__']

user = Blueprint('user', __name__, template_folder='templates')

@user.route('/reg', methods=['GET', 'POST'])
def reg():
    new_user = User()
    new_user.usrname = "hello"
    new_user.pw = "supersecret"
    db.session.add(new_user)
    db.session.commit()
    return "SIKERES REG"



@user.route('/login', methods=['GET','POST'])
def login():
    if 'logged_in' in session:
        print('in sess')
        return redirect(url_for('allomasok'))
    if request.method == 'POST':
        password_candidate = request.form['password']
        if pwIsValid(password_candidate, app.config['HozzaferesiKulcs']):
            session['logged_in'] = True
            return redirect(url_for('allomasok'))
        else:
            return render_template('login.html', msg = "Nem megfelelő kulcs! Hozzáférés megtagadva, Próbáld újra!")
    return render_template('login.html')


@user.route('/logout')
@LoginRequired
def logout():
    session.clear()
    return redirect(url_for('login'))
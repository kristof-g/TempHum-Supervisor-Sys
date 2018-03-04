import sys

from flask import Blueprint, render_template, session, redirect, request, url_for

from helpers import pwIsValid, LoginRequired

app = sys.modules['__main__']

login_page = Blueprint('login_page', __name__, template_folder='templates')
logout_page = Blueprint('logout_page', __name__, template_folder='templates')

@login_page.route('/login', methods=['GET','POST'])
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


@logout_page.route('/logout')
@LoginRequired
def logout():
    session.clear()
    return redirect(url_for('login'))
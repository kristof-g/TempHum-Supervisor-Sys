# -*- coding: utf-8 -*-

from flask import redirect
#Időegység léptető module
from datetime import timedelta, date, datetime
def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

from flask import session, redirect, url_for
from functools import wraps
#Belépés védelem dekorátor
def LoginRequired(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrap

from passlib.hash import sha256_crypt
def pwIsValid(pw_can,pw):
    pw = sha256_crypt.hash(pw)
    print(pw)
    if sha256_crypt.verify(pw_can,pw):
        print("A megadott jelszó helyes")
        return True
    return False


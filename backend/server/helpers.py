# -*- coding: utf-8 -*-
import os
import sys
from termcolor import colored

from flask import session, redirect, url_for
from functools import wraps
from datetime import timedelta, date, datetime

#Időegység léptető module
def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)


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
    if sha256_crypt.verify(pw_can,pw):
        logger("pwIsValid", "Yes, user can get access.")
        return True
    return False


def logger(src, msg):
    datenow=datetime.now()
    print("{} - [{}]: {}".format(colored(datenow, 'blue'), colored(src, 'cyan'), colored(msg, 'white')))


def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

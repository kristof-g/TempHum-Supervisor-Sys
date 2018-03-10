import sys
import os
import json
import csv
from time import strftime
from datetime import timedelta, date, datetime

from flask import Blueprint, render_template, redirect, request, url_for, flash

import server.configuration as cfg
from server.postalservice import checkTemp
from server.helpers import LoginRequired, pwIsValid, resource_path
from server.models import SzenzorAdatok

app = sys.modules['__main__']

allomas_page = Blueprint('allomas_page', __name__, template_folder='templates')
log_page = Blueprint('log_page', __name__, template_folder='templates')
deletestation_page = Blueprint('deletestation_page', __name__, template_folder='templates')
addnewstation_page = Blueprint('addnewstation_page', __name__, template_folder='templates')


@allomas_page.route('/allomas/<id>', methods=['GET'])
@LoginRequired
def allomas(id):
    print(id)
    if os.listdir(resource_path("logs/{}/".format(id))):
        if request.method == 'GET' and request.args.get('sdate') and request.args.get('edate'):
            start_date = datetime.strptime(request.args.get('sdate'), '%Y-%m-%d')
            end_date = datetime.strptime(request.args.get('edate'), '%Y-%m-%d')
            if start_date > datetime.now():
                flash("Hiba a bevitt adatokban!", category='danger')
                start_date = date.today() - timedelta(days=0)
                end_date = date.today() + timedelta(days=1)
            elif start_date == end_date:
                start_date = start_date
                end_date = start_date + timedelta(days=1)
            elif start_date > end_date:
                flash("Hiba a bevitt adatokban! a záró dátum korábbi, mint a kezdő dátum.", category='danger')
                start_date = date.today() - timedelta(days=0)
                end_date = date.today() + timedelta(days=1)
        else:
            # Past 24h as deafault
            start_date = date.today() - timedelta(days=0)
            end_date = date.today() + timedelta(days=1)
        path = os.path.join(app.GLOBAL_CONFIG['SERVER']['WORKDIR'], "allomasok.json")
        allomasok = json.load(open(path, encoding="utf-8"))
        jelenlegiAllomas = allomasok[id]
        print('DATES: [{}]-[{}]'.format(start_date, end_date))
        adatok = SzenzorAdatok(start_date, end_date, id)
        try:
            fajlnev = adatok.generateCsv()
        except Exception as error:
            flash(error)
        print(adatok.nev)
        try:
            latest = SzenzorAdatok(date.today() - timedelta(days=0), date.today() + timedelta(days=1), id)
            latest.adatok = latest.adatok[::-1]
            latest = latest.adatok[0]
            # Legfrissebb adatok
            latest['homerseklet'] = round(Decimal(str(latest['homerseklet']).replace(",", ".")), 1)
            latest['paratartalom'] = round(Decimal(str(latest['paratartalom']).replace(",", ".")), 1)
        except Exception as error:
            pass

        ctx = {
            "jallomas": app.GLOBAL_STATION_CONFIG[id],
            "id": id,
            "mero_nev": jelenlegiAllomas['allomasnev'],
            "datumok": {"ma": date.today() - timedelta(days=0), "holnap": date.today() + timedelta(days=1),
                        "hetmulva": date.today() - timedelta(days=7), "honapmulva": date.today() - timedelta(days=30)},
            "stat": adatok.stat,
            "latest": latest,
            "adatok": adatok,
            "fajlnev": fajlnev,
            "sdate": start_date.strftime("%Y-%m-%d"),
            "edate": end_date.strftime("%Y-%m-%d")
        }
        return render_template("layout.html", ctx=ctx)
    else:
        flash("Ezen az állomáson még nincs felvett adat", category="warning")
        return redirect(url_for('allomasok'))


@log_page.route('/log/<id>', methods=['GET'])
def log(id):
    if request.method == 'GET':
        print("[SERVER] GET REQUEST FROM: {}".format(request.remote_addr))
        app.GLOBAL_STATION_CONFIG[id]['ip'] = str(request.remote_addr)
        cfg.save_allomas()
        homerseklet = request.args.get('homerseklet')
        # Hőmérséklet határérték ellenörzése:
        checkTemp(homerseklet, id)
        paratartalom = request.args.get('paratartalom')
        currDate = strftime("%Y/%m/%d")
        currTime = strftime("%H:%M:%S")
        try:
            dir = os.path.dirname(__file__)
            filename = os.path.join(dir, strftime("logs/{}/%Y/%m/%d.csv".format(id)))
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            ofile = open(filename, "a")
            writer = csv.writer(ofile, delimiter=';', lineterminator='\n')
            writer.writerow([currDate] + [currTime] + [homerseklet] + [paratartalom])
            ofile.close()
            return "Siker!"
        except Exception as error:
            return str(error)
    else:
        return "Not Get"


@deletestation_page.route('/deletestation', methods=['POST'])
@LoginRequired
def deletestation():
    password_candidate = request.form['password']
    if request.method == 'POST' and pwIsValid(password_candidate, app.GLOBAL_CONFIG['HozzaferesiKulcs']):
        app.GLOBAL_STATION_CONFIG.pop(request.form['id'], None)
        flash("Sikeresen törölve a " + str(request.form['id']) + " állomás!", category='success')
        cfg.save_allomas()
        return redirect(url_for('allomasok'))
    else:
        flash("Helytelen kulcs! Hozzáférés megtagadva!", category='danger')
        return redirect(url_for('allomasok'))


@addnewstation_page.route('/addnewstation')
@LoginRequired
def newstation():
    if request.method == 'GET':
        dict = {
            request.args.get('id'): {"allomasnev": request.args.get('megnev'), "allomashely": request.args.get('hely')}}
        print("bevitt adatok:")
        print(dict)
        app.GLOBAL_STATION_CONFIG[request.args.get('id')] = {"allomasnev": request.args.get('megnev'),
                                                             "allomashely": request.args.get('hely'), "ip": "0.0.0.0",
                                                             "minT": float(request.args.get('mint')),
                                                             "maxT": float(request.args.get('maxt'))}
        dir = os.path.dirname(__file__)
        path = os.path.join(dir, strftime("logs/{}/".format(request.args.get('id'))))
        os.makedirs(os.path.dirname(path), exist_ok=True)
        flash("Sikeresen hozzáadva!", category='success')
    cfg.save_allomas()
    return redirect(url_for('allomasok'))

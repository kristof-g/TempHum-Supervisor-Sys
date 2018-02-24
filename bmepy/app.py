# -*- coding: utf-8 -*-
#Event handler
import gevent
import gevent.monkey
gevent.monkey.patch_all()


import os, json, csv
from configuration import loadConfigs, saveAllomas, config, allomasokconfig
from postalservice import checkTemp, backup
from helpers import LoginRequired, daterange, pwIsValid
from models import Allomas, SzenzorAdatok
from time import strftime,time
from datetime import timedelta, date, datetime


from decimal import Decimal
import socket
import sys
from zeroconf import ServiceInfo, Zeroconf


#Webserver
#from gevent.pywsgi import WSGIServer
from waitress import serve


#Web MicroFramework
from flask import Flask,request,render_template,redirect,url_for,session,Response,flash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'VBXXXVK7VzbBvWdx8lHqNy90FWb1a643'

desc = {'path': '/'}

info = ServiceInfo("_http._tcp.local.",
                    "szenzor._http._tcp.local.",
                    socket.inet_aton("127.0.0.1"), 80, 0, 0,
                    desc, "szenzor.local.")

@app.before_first_request
def startup():
    zeroconf = Zeroconf()
    print("Registration of a service, press Ctrl-C to exit...")
    zeroconf.register_service(info)
    loadConfigs()

@app.route('/login', methods=['GET','POST'])
def login():
    if 'logged_in' in session:
        print('in sess')
        return redirect(url_for('allomasok'))
    if request.method == 'POST':
        password_candidate = request.form['password']
        if pwIsValid(password_candidate,config['login']['HozzaferesiKulcs']):
            session['logged_in'] = True
            return redirect(url_for('allomasok'))

        else:
            return render_template('login.html', msg = "Nem megfelelő kulcs! Hozzáférés megtagadva, Próbáld újra!")
    return render_template('login.html')


@app.route('/logout')
@LoginRequired
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/')
@LoginRequired
def allomasok():
    ipcim = socket.gethostbyname(socket.gethostname())
    dir = os.path.dirname(__file__)
    return render_template('start.html', ipcim=ipcim, data = allomasokconfig)


@app.route("/getcsv", methods=['GET'])
@LoginRequired
def getPlotCSV():
    if request.method == 'GET':
        filenev = request.args.get('f')
        dir = os.path.dirname(__file__)
        fajlPath = os.path.join(dir,"downloads/{}".format(filenev) )
        with open(fajlPath) as fp:
            fajl = fp.read()
        return Response(
            fajl,
            mimetype="text/csv",
            headers={"Content-disposition":
                    "attachment; filename="+filenev})


@app.route('/allomas/<id>',methods = ['GET'])
@LoginRequired
def allomas(id):
    print(id)
    dir = os.path.dirname(__file__)
    path = os.path.join(dir,strftime("logs/{}/".format(id)))
    print(os.listdir(path))
    if os.listdir(path):
        if request.method == 'GET' and request.args.get('sdate') and request.args.get('edate'):
            start_date = datetime.strptime(request.args.get('sdate'), '%Y-%m-%d')
            end_date = datetime.strptime(request.args.get('edate'), '%Y-%m-%d')
            if start_date > datetime.now():
                flash("Hiba a bevitt adatokban! Az időgép sajnos még nincs kész.", category='danger')
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
            #Past 24h as deafault
            start_date = date.today() - timedelta(days=0)
            end_date = date.today() + timedelta(days=1)

        dir = os.path.dirname(__file__)
        path = os.path.join(dir,"allomasok.json")
        allomasok = json.load(open(path, encoding="utf-8"))
        jelenlegiAllomas = allomasok[id]
        print('DATES: [{}]-[{}]'.format(start_date,end_date))
        adatok = SzenzorAdatok(start_date,end_date,id)
        fajlnev = adatok.generateCsv()
        print(adatok.nev)
        try:
            latest = SzenzorAdatok(date.today() - timedelta(days=0),date.today() + timedelta(days=1),id)
            latest.adatok = latest.adatok[::-1]
            latest = latest.adatok[0]
            #Legfrissebb adatok
            latest['homerseklet'] = round(Decimal(str(latest['homerseklet']).replace(",", ".")),1)
            latest['paratartalom'] = round(Decimal(str(latest['paratartalom']).replace(",", ".")),1)
        except Exception as error:
            flash(error)

        ctx = {
            "jallomas":allomasokconfig[id],
            "id":id,
            "mero_nev" : jelenlegiAllomas['allomasnev'],
            "datumok" : {"ma":date.today() - timedelta(days=0), "holnap":date.today() + timedelta(days=1), "hetmulva":date.today() - timedelta(days=7), "honapmulva":date.today() - timedelta(days=30)},
            "stat" : adatok.stat,
            "latest" : latest,
            "adatok" : adatok,
            "fajlnev" : fajlnev,
            "sdate" : start_date.strftime("%Y-%m-%d"),
            "edate" : end_date.strftime("%Y-%m-%d")
        }
       
        return render_template("layout.html",ctx = ctx)
    else:
        flash("Ezen az állomáson még nincs felvett adat",category="warning")
        return redirect(url_for('allomasok'))

@app.route('/log/<id>', methods=['GET'])
def log(id):
    if request.method == 'GET':
        print("GET REQUEST FROM{}".format(request.remote_addr))
        allomasokconfig[id]['ip'] = str(request.remote_addr)
        saveAllomas()
        homerseklet = request.args.get('homerseklet')
        checkTemp(homerseklet)
        paratartalom = request.args.get('paratartalom')
        currDate = strftime("%Y/%m/%d")
        currTime = strftime("%H:%M:%S")
        try:
            dir = os.path.dirname(__file__)
            filename = os.path.join(dir,strftime("logs/{}/%Y/%m/%d.csv".format(id)))
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            ofile  = open(filename, "a")                
            writer = csv.writer(ofile,delimiter=';',lineterminator='\n') 
            writer.writerow([currDate]+[currTime]+[homerseklet]+[paratartalom])
            ofile.close()
            return "Siker!"
        except Exception as error:
            return str(error)
    else:
        return "Not Get"

@app.route('/deletestation', methods=['POST'])
@LoginRequired
def deltation():
    password_candidate = request.form['password']
    if request.method == 'POST' and pwIsValid(password_candidate,config['login']['HozzaferesiKulcs']):
        allomasokconfig.pop(request.form['id'],None)
        flash("Sikeresen törölve a "+str(request.form['id'])+" állomás!", category='success')
        saveAllomas()
        return redirect(url_for('allomasok'))
    else:
        flash("Helytelen kulcs! Hozzáférés megtagadva!", category='danger')
        return redirect(url_for('allomasok'))

@app.route('/addnewstation')
@LoginRequired
def newstation():
    if request.method == 'GET' and request.args.get('id') and request.args.get('del'):
        allomasokconfig.pop(request.args.get('id'),None)
        flash("Sikeresen törölve a "+request.args.get('id')+" állomás!", category='success')
    elif request.method == 'GET':
        dict = { request.args.get('id'):{ "allomasnev":request.args.get('megnev'),"allomashely":request.args.get('hely')} }
        print("bevitt adatok:")
        print(dict)
        allomasokconfig[request.args.get('id')] = { "allomasnev":request.args.get('megnev'),"allomashely":request.args.get('hely'), "ip":"0.0.0.0", "minT":request.args.get('mint'), "maxT":request.args.get('maxt') }
        flash("Sikeresen hozzáadva!", category='success')
    saveAllomas()
    return redirect(url_for('allomasok'))

if __name__ == '__main__':
    http_server = serve(app, host='0.0.0.0', port=80)
    srv_greenlet = gevent.spawn(http_server.start)
    background_task = gevent.spawn(backup)
    try:
        gevent.joinall([srv_greenlet, background_task])
    except KeyboardInterrupt:
        print("Unregistering...")
        zeroconf.unregister_service(info)
        zeroconf.close()
        print("Exiting")
 
    


        
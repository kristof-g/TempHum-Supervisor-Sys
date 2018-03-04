# -*- coding: utf-8 -*-
# Event handler
import gevent.monkey
gevent.monkey.patch_all()
import os
import socket

# Web server
from waitress import serve
# Web MicroFramework parts
from flask import Flask, request, render_template, Response

import configuration as cfg
from postalservice import backup
from helpers import LoginRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'VBXXXVK7VzbBvWdx8lHqNy90FWb1a643'
app.config['debug'] = True
# GLOBAL CONFIGURATIONS
GLOBAL_STATION_CONFIG = {}
GLOBAL_CONFIG = {}

#-------------------------------------------
#   loading Blueprints for routes
#-------------------------------------------
from routes.user import login_page, logout_page
from routes.device import log_page, deletestation_page, allomas_page, addnewstation_page
app.register_blueprint(login_page)
app.register_blueprint(logout_page)
app.register_blueprint(deletestation_page)
app.register_blueprint(allomas_page)
app.register_blueprint(addnewstation_page)
app.register_blueprint(log_page)


@app.before_first_request
def startup():
    #cfg.load_configs()
    pass


@app.route('/')
@LoginRequired
def allomasok():
    ctx = {
        "ipcim": GLOBAL_CONFIG['SERVER']['IP']+str(GLOBAL_CONFIG['SERVER']['PORT']),
        "data": GLOBAL_STATION_CONFIG
    }
    return render_template('start.html', ctx=ctx)


@app.route("/getcsv", methods=['GET'])
@LoginRequired
def get_plot_csv():
    if request.method == 'GET':
        file_nev = request.args.get('f')
        fajlPath = os.path.join(GLOBAL_CONFIG['SERVER']['WORKDIR'], "downloads/{}".format(file_nev))
        with open(fajlPath) as fp:
            fajl = fp.read()
        return Response(
            fajl,
            mimetype="text/csv",
            headers={"Content-disposition":
                     "attachment; filename="+file_nev})


if __name__ == '__main__':
    cfg.load_configs()
    GLOBAL_CONFIG['SERVER']['IP'] = socket.gethostbyname(socket.gethostname())
    GLOBAL_CONFIG['SERVER']['WORKDIR'] = str(os.path.dirname(__file__))
    cfg.save_cfg()
    background_task = gevent.spawn(backup)
    http_server = serve(app, host='0.0.0.0', port=GLOBAL_CONFIG['SERVER']['PORT'])
    srv_greenlet = gevent.spawn(http_server.start())
    try:
        gevent.joinall([srv_greenlet, background_task])
    except KeyboardInterrupt:
        print("Exiting")

# -*- coding: utf-8 -*-
# Event handler
import gevent.monkey
gevent.monkey.patch_all()
import os
import socket

# Web server
from waitress import serve


#from server.postalservice import backup
from server import app, GLOBAL_CONFIG
from server.device.connectors.modbus_rtu_temp_hum.read import read_instrument

#background_task = gevent.spawn(backup)
#modb_task = gevent.spawn(read_instrument)
http_server = serve(app, host='0.0.0.0', port=3125)
srv_greenlet = gevent.spawn(http_server.start())
try:
    gevent.joinall([srv_greenlet])
except KeyboardInterrupt:
    print("Exiting")

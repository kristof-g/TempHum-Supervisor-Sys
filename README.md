# Sensor Supervisor System

This system is designed to log, and analyze primarily Tempreture and hummidity data primarily for the food industry. However it is planned to make it more universal, for several use case secanarios. Was not using Git, in the begining sicne this started from a fairly simple design, but i feel like now it makes more sense.

## Get started
### Linux -  Python 3.6 and Virtualenv 

    $ cd bmepy
    $ mkdir venv
    $ virtualenv venv
    $ pip install requirements.txt
    $ python run.py - or service file available for deployment ( Dockerfile in progress)
## Used technology:
### Software side:
- Backend (--> API ) written in Flask using Blueprints for better readability
- Frontend rendered by Jinja2 templating engine  <br />[ currently switching to Vue.JS2, so backend only provides API  ]
- Bootstrap 4 Material used as a responsive CSS Framework
- Chart.JS for charting the data
### Sensor Side
- Developing universal connector <br />
[ in progress ]
- ESP8266 / ESP32 with BME280 temp and hum sensors<br />
sensor node only announce IP addr, then server fetches data from nodes via HTTP request. ESP returns JSON data.
- RS485 based wired solution for places where wireless network woud not be feasible


----------
## Plans ahead
-  [ done ] Experiment with replacing Flask with Sanic for async web  <br />
	Although sanic has way higher throughput, for now speed is not an issue with the Flask backend, 
	also using Client side Javascript to render makes everything smoother overall.
 - [ done ] manage multiple sensor nodes at the same time
 - [ - ] Universal connector 
 - [ - ] Add the ability to manage different types of sensors
 - [ semi-ready ] Dockerfile for easier deployment and OTA updates

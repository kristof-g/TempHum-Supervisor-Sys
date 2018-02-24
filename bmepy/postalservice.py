# -*- coding: utf-8 -*-
#from app import config
import gevent, smtplib,config
from time import strftime,time
from configuration import config, allomasokconfig
msg_sent_time = 0

"""
Ez a fv. felel a homerseklet ellenorzeserol, megnézi hogy benne van-e a tartományba.
Ha nincs akkor még megnézi hogy mikor küldött utoljára üzenetet és ha eltelt a konfigurált időtartam akkor
értesíti a megadott email cimet.
"""
def checkTemp(homerseklet,id):
    global msg_sent_time
    elapsed_time = time() - msg_sent_time
    if not allomasokconfig[id]['minT'] <= float(homerseklet) <= allomasokconfig[id]['maxT'] and elapsed_time/60 > 70:
        print("Homerseklet definialt tartomanyon kivul esik!")
        try:
            subject = "Homerseklet figyelmeztetes a {} allomasnal.".format(allomasokconfig[id]['allomasnev'])
            msg = "Homerseklet a definialt tartomanyon kivul: {} ".format(homerseklet)
            message = "Subject: {}\n\n{}".format(subject,msg)
            # TFH Google Mailt hasznalunk
            mail = smtplib.SMTP('smtp.gmail.com',587)
            mail.ehlo()
            mail.starttls()
            mail.login(config['MailerFelhasznalo'],config['MailerJelszo'])
            mail.sendmail(config['MailerFelhasznalo'],config['ErtesitesiEmail'],message)
            mail.close() 
            msg_sent_time = time()
            print("SENDMAIL: EMAIL sikeresen elkuldve...")
        except:
            print("SENDMAIL: FAILURE :[ ")

def backup():
    count = 0
    while True:
        #print(count)
        count += 1
        gevent.sleep(3)

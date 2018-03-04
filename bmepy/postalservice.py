# -*- coding: utf-8 -*-
import gevent
import sys
import smtplib
import os.path as op
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders
from time import strftime, time

from helpers import logger

app = sys.modules['__main__']



"""
This function checks whether the temps are in the predefined range, if they are not then alerts.
"""
def checkTemp(homerseklet,id):
    app.GLOBAL_STATION_CONFIG[id]['']
    elapsed_time = time() - msg_sent_time
    if not app.GLOBAL_STATION_CONFIG[id]['minT'] <= float(homerseklet) <= app.GLOBAL_STATION_CONFIG[id]['maxT'] and elapsed_time/60 > 70:
        logger("TEMP-CHECK", "Temps are outside configured values.")
        try:
            subject = "Homerseklet figyelmeztetes a {} allomasnal.".format(id)
            msg = "Homerseklet a definialt tartomanyon kivul: {} ".format(homerseklet)
            message = "Subject: {}\n\n{}".format(subject, msg)
            send_mail(subject=subject, message=message, files=[],)
            msg_sent_time = time()
            logger("CHECK-TEMP", "Mail sent!")
        except Exception as error:
            logger("CHECK-TEMP", "Unsuccessful")
            logger("CHECK-TEMP", error)


"""
Making a backup of the past month, zip it. And send backup.zip every 2 week.
"""
def backup():
    import os
    import zipfile
    import configuration as cfg
    cfg.load_configs()
    while True:
        logger("BACKUP", "Starting backup proc...")
        try:
            dir = os.path.dirname(__file__)
            zf = zipfile.ZipFile(os.path.join(dir,"downloads/backup.zip"), "w")
            for key in app.allomasokconfig:
                for dirname, subdirs, files in os.walk(os.path.join(dir,strftime("logs/{}/%Y/%m".format(key)))):
                    zf.write(dirname, dirname.replace(dir,""))
                    for filename in files:
                        f = os.path.join(dirname, filename)
                        zf.write(f,f.replace(dir,""))
            zf.close()
            send_mail(subject=strftime("Meroallomas backup: %Y %m"),message="Ez egy automatikus uzenet, mellekletben a ehavi mentes talalhato.", files=[os.path.join(dir,"downloads/backup.zip")] )
            logger("BACKUP", "Done... waiting 2 weeks")
        except Exception as error:
            logger("BACKUP", "Unsuccessful")
            logger("BACKUP", error)
        gevent.sleep(1209600)

"""
Sending EMAIL using parameters
"""
def send_mail(subject, message, files=[], use_tls=True):
    msg = MIMEMultipart()
    msg['From'] = app.config['MailerFelhasznalo']
    msg['To'] = app.config['ErtesitesiEmail']
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(message))

    for path in files:
        part = MIMEBase('application', "octet-stream")
        with open(path, 'rb') as file:
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        'attachment; filename="{}"'.format(op.basename(path)))
        msg.attach(part)

    smtp = smtplib.SMTP('smtp.gmail.com',587)
    if use_tls:
        smtp.starttls()
    smtp.login(app.config['MailerFelhasznalo'], app.config['MailerJelszo'])
    smtp.sendmail(app.config['MailerFelhasznalo'], app.config['ErtesitesiEmail'], msg.as_string())
    smtp.quit()
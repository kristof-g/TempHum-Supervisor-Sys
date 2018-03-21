#generate fake data
from time import strftime
from datetime import timedelta, date
import os
import csv
import random
from math import sin,cos

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)


start_date = date(2017, 12, 5)
end_date = date(2018, 2, 24)
try:
    lepteto = 0
    for single_date in daterange(start_date, end_date):
        dir = os.path.dirname(__file__)
        filename = os.path.join(dir,single_date.strftime("logs/szfoliasator/%Y/%m/%d.csv"))
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        ofile  = open(filename, "a")                
        writer = csv.writer(ofile,dialect='excel') 
        for i in range(48):
            writer.writerow([single_date.strftime("%Y/%m/%d")]+[single_date.strftime("%H:%M:%S")]+[sin(lepteto)]+[cos(lepteto)])
            lepteto += 0.005
        ofile.close()
except Exception as error:
    print(str(error))
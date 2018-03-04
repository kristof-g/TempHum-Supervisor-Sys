# -*- coding: utf-8 -*-
import os
import csv
import json

from flask import flash

from helpers import daterange


class Allomas:
    def __init__(self,id):
        dir = os.path.dirname(__file__)
        path = os.path.join(dir,"allomasok.json")
        allomasok = json.load( open(path, encoding="UTF-8") )
        allomasok = allomasok[id]
        self.id = id
        self.nev = allomasok['allomasnev']
        self.hely = allomasok['allomashely']


class SzenzorAdatok(Allomas):
    def __init__(self,sDate,eDate,id):
        super(SzenzorAdatok, self).__init__(id)
        self.StartDate = sDate 
        self.EndDate = eDate
        self.adatok = self.getDataFromCsv(sDate,eDate,id)
        self.stat = self.getStat()



    def getDataFromCsv(self, start_date, end_date, id):
        data = []
        hianyos = False
        for single_date in daterange(start_date, end_date):
            try:
                dir = os.path.dirname(__file__)
                filename = os.path.join(dir,single_date.strftime("logs/{}/%Y/%m/%d.csv".format(id)))
                print(filename)
                with open(filename, encoding="utf-8") as f:
                    reader = csv.reader(f,delimiter=';',lineterminator='\n')
                    for row in reader:
                        #print(row)
                        row = { "datum" : row[0], "idopont" : row[1], "homerseklet" : row[2], "paratartalom" : row[3] }
                        data.append(row)
            except Exception as error:
                print(error)
                row = { "datum" : single_date.strftime("%Y/%m/%d"), "idopont" : single_date.strftime("%H:%M:%S") }
                data.append(row)
                hianyos = True

        if hianyos: 
            flash("A megadott ídősáv hiányos!", category='warning')
        return data

    def getStat(self):
        try:
            print("getstatcalled")
            dat = self.adatok
            i = 0
            while 'homerseklet' and 'paratartalom' not in dat[i]:
                i += 1
            minTemp = dat[i]
            maxHum = dat[i]
            minHum = dat[i]
            maxTemp = dat[i]
            

            for row in dat:
                try:
                    #MAXTEMP
                    if float(row['homerseklet']) > float(maxTemp['homerseklet']):
                        maxTemp = row
                    #MINTEMP
                    if float(row['homerseklet']) < float(minTemp['homerseklet']):
                        minTemp = row
                    #MAXHUM
                    if float(row['paratartalom']) > float(maxHum['paratartalom']):
                        maxHum = row
                    #MINHUM
                    if float(row['paratartalom']) < float(minHum['paratartalom']):
                        minHum = row
                except Exception:
                    pass
            dict = { "maxTemp":maxTemp, "minTemp":minTemp, "maxHum":maxHum, "minHum":minHum }
            return dict
        except Exception:
            pass

    def generateCsv(self):
        dir = os.path.dirname(__file__)
        fajl = "{}_{}-{}.csv".format(self.id,self.StartDate.strftime("%Y_%m_%d"),self.EndDate.strftime("%Y_%m_%d"))
        filename = os.path.join( dir,"downloads/{}".format(fajl))
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        ofile  = open(filename, "w")                
        writer = csv.writer(ofile,delimiter=';',lineterminator='\n')
        for row in self.adatok:
            try:
                writer.writerow([row['datum']]+[row['idopont']]+[row['homerseklet'].replace('.', ',')]+[row['paratartalom'].replace('.', ',')])
            except KeyError:
                pass
        ofile.close()
        return fajl

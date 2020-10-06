# -*- coding: utf-8 -*-
"""
Created on Sun Oct  4 15:47:52 2020

@author: drale
"""
import uuid
import datetime
import random
import json
import time
import multiprocessing
#class Sensor():
LOG_FILE_A="tempSensorLogA.json"
LOG_FILE_B="tempSensorLogB.json"
LOG_MAX=200

#number of seconds in between logging temperature readings
SLEEP_TIME=1

def getTemp():
    minVal=-50
    maxVal=150
    scaledVal = minVal + (random.random() * (maxVal - minVal))
    return scaledVal

def getTempData():
    #technically there is a chance of an id collision here, but it is very small
    guid = str(uuid.uuid4())
    isoTime = datetime.datetime.now().isoformat()
    fTemp=getTemp()

    return {"id" : guid, 
            "type" : "sensor", 
            "content" : {"temperature_f" : fTemp,
                         "time_of_measurement" : isoTime}}

def writeLogEntry(logFile, data):
    with open(logFile, "a") as file:
        file.write(str(data).replace("\'", "\""))
        file.write("\n")

def clearLogFile(logFile):
    with open(logFile, "w+") as file:
        file.write("")

def generateSensorLog(numEntries, debug=False):
    currentLogFile = LOG_FILE_A
    entriesWritten = 0
    clearLogFile(LOG_FILE_A)
    clearLogFile(LOG_FILE_B)

    for _ in range(numEntries):
        data = getTempData()
        writeLogEntry(currentLogFile, data)
        entriesWritten += 1

        if entriesWritten % LOG_MAX == 0:
            newLogFile = LOG_FILE_B
            if currentLogFile == LOG_FILE_B:
                newLogFile = LOG_FILE_A

            clearLogFile(newLogFile)
            currentLogFile = newLogFile

        if not debug:
            time.sleep(SLEEP_TIME)
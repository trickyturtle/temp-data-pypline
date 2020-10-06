# -*- coding: utf-8 -*-
"""
Created on Sun Oct  4 15:47:52 2020

@author: drale
"""
import uuid
import datetime
import random
#class Sensor():

def getTemp():
    minVal=-50
    maxVal=150
    scaledVal = minVal + (random.random() * (maxVal - minVal))
    return scaledVal

def getTempData():
    #technically there is a chance of an id collision here, but it is very small
    guid = uuid.uuid4()
    isoTime = datetime.datetime.now().isoformat()
    fTemp=getTemp()

    return {"id" : guid, 
            "type" : "sensor", 
            "content" : {"temperature_f" : fTemp,
                         "time_of_measurement" : isoTime}}

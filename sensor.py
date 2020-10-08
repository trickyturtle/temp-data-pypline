# -*- coding: utf-8 -*-
"""
Created on Sun Oct  4 15:47:52 2020

@author: drale
"""
import uuid
import datetime
import random

def getTempData():
    #technically there is a chance of an id collision using uuid4, but it is very small
    guid = str(uuid.uuid4())
    fTemp=random.randint(-100,500)
    isoTime = datetime.datetime.now().replace(microsecond=0).isoformat()

    return {"id" : guid, 
            "type" : "sensor", 
            "content" : {"temperature_f" : fTemp,
                         "time_of_measurement" : isoTime}}


# -*- coding: utf-8 -*-
"""
Created on Sun Oct  4 15:50:29 2020
@author: drale
A data enricher that takes data from a sensor
"""
import sys
import logging

def enrichAndEnqueDataMessage(data, queue):
    temperature_c = (data["content"]["temperature_f"] - 32) * (5.0/9.0)
    try:
        msg = [data["id"], data["type"], data["content"]["temperature_f"], 
            temperature_c, data["content"]["time_of_measurement"]]
        queue.put(msg)
    except:
        #This is probably due to a malformed data message. A single data
        #point is probably less valuable than keeping the pipeline moving, so
        #we note it and move on.
        logging.error("Unexpected error:", sys.exc_info()[0])
    return msg

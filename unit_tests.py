# -*- coding: utf-8 -*-
"""
Created on Sun Oct  4 15:44:17 2020

@author: drale
"""


import unittest
import sensor
import data_processor
import data_enricher
import data_pipeline
import uuid
import json

LOG_FILE_A="tempSensorLogA.json"
LOG_FILE_B="tempSensorLogB.json"

class TestTempDataPipeline(unittest.TestCase):
    # =============================================================================
    # Sensor Tests
    # =============================================================================

    #Test that sensor returns a float temp
    def test_getTemp(self):
        self.assertTrue(isinstance(sensor.getTemp(), int))

    #Test that sensor.getTempData returns a dict with the correct fields
    def test_getTempData(self):
        tempData=sensor.getTempData()
        self.assertTrue(isinstance(tempData, dict))
        self.assertTrue("id" in tempData)
        self.assertTrue("type" in tempData)
        self.assertTrue("content" in tempData)
        try:
            self.assertTrue(isinstance(uuid.UUID(tempData["id"]), uuid.UUID))
        except ValueError:
            self.fail("Data did not have a valid UUID")
        self.assertTrue(tempData["type"]=="sensor")
        self.assertTrue("temperature_f" in tempData["content"])
        self.assertTrue("time_of_measurement" in tempData["content"])
        self.assertTrue(isinstance(tempData["content"]["temperature_f"], int))
        self.assertTrue(isinstance(tempData["content"]["time_of_measurement"], str))
        self.assertRegex( tempData["content"]["time_of_measurement"],
                         '\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\d')
        
    #Test that runSensor generates logs correctly
    def test_generateSensorLog(self):
        sensor.clearLogFile(LOG_FILE_A)
        sensor.clearLogFile(LOG_FILE_B)
        sensor.generateSensorLog(2*sensor.LOG_MAX+2, True)
        with open(LOG_FILE_A, "r") as readFile:
            logs = readFile.read().splitlines()
 
        #Verify old log is deleted on reaching max number of entries
        self.assertTrue(len(logs)==2)
    
        for log in logs:
            log = json.loads(log)
            self.assertTrue(isinstance(log, dict))
            self.assertTrue("id" in log)
            self.assertTrue("type" in log)
            self.assertTrue("content" in log)
            try:
                self.assertTrue(isinstance(uuid.UUID(log["id"]), uuid.UUID))
            except ValueError:
                self.fail("Data did not have a valid UUID")
            self.assertTrue(log["type"]=="sensor")
            self.assertTrue("temperature_f" in log["content"])
            self.assertTrue("time_of_measurement" in log["content"])
            self.assertTrue(isinstance(log["content"]["temperature_f"], int))
            self.assertTrue(isinstance(log["content"]["time_of_measurement"], str))
            self.assertRegex( log["content"]["time_of_measurement"],
                             '\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\d')
        

if __name__ == '__main__':
    unittest.main()
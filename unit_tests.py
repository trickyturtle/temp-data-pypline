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

class TestTempDataPipeline(unittest.TestCase):
    # =============================================================================
    # Sensor Tests
    # =============================================================================

    #Test that sensor returns a float temp
    def test_getTemp(self):
        self.assertTrue(isinstance(sensor.getTemp(), float))

    #Test that sensor.getTempData returns a dict with the correct fields
    def test_getTempData(self):
        tempData=sensor.getTempData()
        self.assertTrue(isinstance(tempData, dict))
        self.assertTrue("id" in tempData)
        self.assertTrue("type" in tempData)
        self.assertTrue("content" in tempData)
        self.assertTrue(isinstance(tempData["id"], uuid.UUID))
        self.assertTrue(tempData["type"]=="sensor")
        self.assertTrue("temperature_f" in tempData["content"])
        self.assertTrue("time_of_measurement" in tempData["content"])
        self.assertTrue(isinstance(tempData["content"]["temperature_f"], float))
        self.assertTrue(isinstance(tempData["content"]["time_of_measurement"], str))
        self.assertRegex( tempData["content"]["time_of_measurement"],
                         '\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\d')

if __name__ == '__main__':
    unittest.main()
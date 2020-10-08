# -*- coding: utf-8 -*-
"""
Created on Sun Oct  4 15:44:17 2020

@author: drale
"""


import unittest
import sensor
import data_processor
import data_enricher
import psycopg2
import multiprocessing as mp
import uuid

PG_HOST_NAME="localhost"
PG_DATA_BASE="postgres"
PG_USER_NAME="postgres"
PG_PASSWORD="postgres"


class TestTempDataPipeline(unittest.TestCase):
    # =============================================================================
    # Sensor Tests
    # =============================================================================

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
        
    # =============================================================================
    # Data Enricher Tests
    # =============================================================================
    #Test that the data_enricher produces a properly formatted message
    def test_enrichAndEnqueDataMessage(self):
        queue = mp.JoinableQueue()
        data_enricher.enrichAndEnqueDataMessage(sensor.getTempData(), queue)
        msg = queue.get()
        try:
            self.assertTrue(isinstance(uuid.UUID(msg[0]), uuid.UUID))
        except ValueError:
            self.fail("Data did not have a valid UUID")
        self.assertTrue(msg[1]=="sensor")
        self.assertTrue(isinstance(msg[2], int))
        self.assertTrue(isinstance(msg[3], float) or isinstance(msg[3], int))
        self.assertRegex(msg[4],
                         '\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\d')
 
    # =============================================================================
    # Data Processor Tests
    # =============================================================================
    #Test that the data_processor correctly inputs data into the db
    def test_insertDataFromQueue(self):
        data_processor.clearTable()
        data_processor.createTable()
        queue = mp.JoinableQueue()
        for i in range(3):
            data_enricher.enrichAndEnqueDataMessage(sensor.getTempData(), queue)
        worker_process = mp.Process(target=data_processor.insertDataFromQueue, args=(queue, ), daemon=True, name='worker_process_{}'.format(i))
        worker_process.start()
        queue.join()
        conn = psycopg2.connect(host=PG_HOST_NAME,
                                    database=PG_DATA_BASE,
                                    user=PG_USER_NAME,
                                    password=PG_PASSWORD)
        cur = conn.cursor()
        cur.execute("select * from temperatures")
        contents = cur.fetchall()
        i=0
        for msg in contents:
            i+=1
            try:
                self.assertTrue(isinstance(uuid.UUID(msg[0]), uuid.UUID))
            except ValueError:
                self.fail("Data did not have a valid UUID")
            self.assertTrue(msg[1]=="sensor")
            self.assertTrue(isinstance(msg[2], int))
            self.assertTrue(isinstance(msg[3], float) or isinstance(msg[3], int))
            self.assertRegex(msg[4],
                             '\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\d')
        self.assertTrue(i==3)
        cur.close()
        conn.close()
        
if __name__ == '__main__':
    unittest.main()
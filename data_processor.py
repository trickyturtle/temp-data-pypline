# -*- coding: utf-8 -*-
"""
Created on Sun Oct  4 15:50:04 2020

@author: drale
"""
import sys
import psycopg2
import logging
PG_HOST_NAME="localhost"
PG_DATA_BASE="postgres"
PG_USER_NAME="postgres"
PG_PASSWORD="postgres"
def createTable():
    try:
        conn = psycopg2.connect(host=PG_HOST_NAME,
                                    database=PG_DATA_BASE,
                                    user=PG_USER_NAME,
                                    password=PG_PASSWORD)
        cur = conn.cursor()
        cur.execute("""
                 CREATE TABLE IF NOT EXISTS temperatures (
                 id TEXT NOT NULL UNIQUE,
                 type TEXT,
                 temperature_f INT,
                 temperature_c INT,
                 time_of_measurement TEXT
                 )
                 """)
        conn.commit()
    except:
        logging.error("Table creation failed")
    cur.close()
    conn.close()

def clearTable():
    try:
        conn = psycopg2.connect(host=PG_HOST_NAME,
                                    database=PG_DATA_BASE,
                                    user=PG_USER_NAME,
                                    password=PG_PASSWORD)
        cur = conn.cursor()
        cur.execute("""
                 DROP table IF EXISTS temperatures
                 """)
        conn.commit()
    except:
        logging.error("Table deletion failed")
    cur.close()
    conn.close()
        
def insertDataFromQueue(queue):
    while True:
        try:
            conn = psycopg2.connect(host=PG_HOST_NAME,
                                    database=PG_DATA_BASE,
                                    user=PG_USER_NAME,
                                    password=PG_PASSWORD)
            cur = conn.cursor()
            msg = queue.get()
            cur.execute("insert into temperatures (id, type, temperature_f, temperature_c, time_of_measurement) values (%s, %s, %s, %s, %s)", msg )
            conn.commit()
            
            queue.task_done()
            cur.close()
            conn.close()
        except:
            logging.error("Unexpected error:", sys.exc_info()[0])
            raise

#Final Sports Project SI 206 - Alex Choi, Zachary Fewkes, Abhay Shakhapur

from bs4 import BeautifulSoup
import requests
import json
import unittest
import re
import os
import csv
import sqlite3

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def setUpSportsTable(name, cur, conn):
    cur.execute('''CREATE TABLE IF NOT EXISTS ''' + name + '''(id INTEGER PRIMARY KEY, agg_score INTEGER,
     game_length FLOAT, location_id INTEGER)''')
    conn.commit()
    print('here')

#For use in case of mistake
def delSportsTable(name, cur, conn):
    cur.execute("DROP TABLE IF EXISTS " + name)
    conn.commit()




def main():
    # SETUP DATABASE AND TABLE
    cur, conn = setUpDatabase('Sports.db')

    
    #delSportsTable('Basketball', cur, conn)
    setUpSportsTable('Basketball', cur, conn)
    
main()
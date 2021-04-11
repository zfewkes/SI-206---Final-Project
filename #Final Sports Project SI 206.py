#Final Sports Project SI 206 - Alex Choi, Zachary Fewkes, Abhay Shakhapur


#Remember, Use 2019 - 2020 data! 
#(we can change this if its too difficult for some API ...)


from bs4 import BeautifulSoup
import requests
import json
import unittest
import re
import os
import csv
import sqlite3


#USEFUL CODE FOR ALL ----------------------------------------------------------
def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def setUpSportsTable(name, cur, conn):
    cur.execute('''CREATE TABLE IF NOT EXISTS ''' + name + '''(id INTEGER PRIMARY KEY, game_id INTEGER UNIQUE,
     home_team_score INTEGER, away_team_score INTEGER, agg_score INTEGER,
     game_length FLOAT, location_hometeam_id INTEGER)''')
    conn.commit()
    print('here')

def setUpLocation_TeamTable(name, cur, conn):
    cur.execute('''CREATE TABLE IF NOT EXISTS ''' + name + ''' (id INTEGER PRIMARY KEY,
     home_team TEXT, stadium TEXT)''')
    conn.commit()
    print('here')

#For use in case of mistakes
def delTable(name, cur, conn):
    cur.execute("DROP TABLE IF EXISTS " + name)
    conn.commit()

#USEFUL CODE FOR ALL ----------------------------------------------------------



#Zach/BBall Specific Code -----------------------------------------------------
def read_25_ball_dont_lie_api(page, cur, conn):
    print("Fetching data for <bball>")

    try:
        r = requests.get('https://www.balldontlie.io/api/v1/games?seasons[]=2019&page=' + page)
        data_0 = r.text
        data = json.loads(data_0)
        print('Success')
        return data
    except:
        print('something\'s wrong')
        return None

def write_to_bball_db(data, cur, conn):

    for item in data['']:
        cur.execute('SELECT id FROM Categories WHERE title = ? LIMIT 1', (item['categories'][0]['title'], )) 
        cat_id = cur.fetchone()[0]

        cur.execute('INSERT INTO Restaurants (restaurant_id, name, address, zip, category_id, rating, price) VALUES (?,?,?,?,?,?,?)',
         (item['id'], item['name'], item['location']['address1'], item['location']['zip_code'], 
         cat_id, float(item['rating']), item.get('price', '$$$$')))
    conn.commit()


#Zach/BBall Specific Code -----------------------------------------------------



def main():
    # SETUP DATABASE AND TABLE
    cur, conn = setUpDatabase('Sports.db')

    delTable('Basketball', cur, conn)
    setUpSportsTable('Basketball', cur, conn)
    setUpLocation_TeamTable('Basketball_teams_stadiums', cur, conn)


    game_json = read_25_ball_dont_lie_api(str(1), cur, conn)



    
    
main()
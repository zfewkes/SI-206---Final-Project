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
     stadium_hometeam_id INTEGER)''')
    conn.commit()
    print('here')

def setUpLocation_TeamTable(name, cur, conn):
    cur.execute('''CREATE TABLE IF NOT EXISTS ''' + name + ''' (id INTEGER PRIMARY KEY UNIQUE,
    team TEXT, stadium TEXT)''')
    conn.commit()
    print('here')

#For use in case of mistakes
def delTable(name, cur, conn):
    cur.execute("DROP TABLE IF EXISTS " + name)
    conn.commit()

#USEFUL CODE FOR ALL ----------------------------------------------------------



#Zach/BBall Specific Code -----------------------------------------------------
def read_all_team_ids():
    print("Reading team ids")

    try:
        r = requests.get('https://www.balldontlie.io/api/v1/teams')
        data_0 = r.text
        data = json.loads(data_0)
        print('Success')
        return data
    except:
        print('something\'s wrong')
        return None


#unfinished - !!!!
def read_all_stadium_ids():
    print("Reading stadium ids")
    tup_list = []
    soup = BeautifulSoup(requests.get('https://en.wikipedia.org/wiki/List_of_National_Basketball_Association_arenas').text, 'html.parser')
    tag = soup.find('tbody')
    print(tag)
    for item in tag.find_all('b'):
        print()
        print(item)
        print(item.find('a'))
        print(item.find('a').get('title'))
        tup_list.append(item.find('a').get('title'))


def read_25_ball_dont_lie_api(page):
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


#data is a list of JSON 
def write_to_bball_db(data, cur, conn):

    for item in data['data']:
        cur.execute('''INSERT OR IGNORE INTO Basketball (game_id, home_team_score, away_team_score,
        agg_score, stadium_hometeam_id) VALUES (?,?,?,?,?)''',
         (int(item.get('id')), int(item.get('home_team_score')), int(item.get('visitor_team_score')),
          int(item.get('home_team_score')) +  int(item.get('visitor_team_score')), 
          int(item.get('home_team').get('id')) ))
    conn.commit()

def write_to_basketball_teams_stadiums(data, cur, conn):
    for item in data['data']:
        #print(item.get('id'))
        #print(item.get('full_name'))
        cur.execute('INSERT OR IGNORE INTO Basketball_teams_stadiums (id,team) VALUES (?,?)',
         (item.get('id', None), item.get('full_name', None)))
    conn.commit()


#Zach/BBall Specific Code -----------------------------------------------------


def main():
    # SETUP DATABASE AND TABLE

    cur, conn = setUpDatabase('Sports.db')


#------------------------------------------------------------------------- Zach's part
    #delTable('Basketball', cur, conn)
    #delTable('Basketball_teams_stadiums', cur, conn)

    setUpLocation_TeamTable('Basketball_teams_stadiums', cur, conn)
    team_table_json = read_all_team_ids()
    #read_all_stadium_ids()
    write_to_basketball_teams_stadiums(team_table_json, cur, conn)
    #print (team_table_json)


    setUpSportsTable('Basketball', cur, conn)
    game_json = read_25_ball_dont_lie_api(str(1))
    write_to_bball_db(game_json, cur, conn)

    #cur.execute('''SELECT Basketball.agg_score FROM Basketball JOIN Basketball_teams_stadiums 
    #ON Basketball.stadium_hometeam_id = Basketball_teams_stadiums.id 
    #WHERE Basketball_teams_stadiums.team = ? ''', ("Denver Nuggets",))

    #for row in cur: 
    #    print(row)


#------------------------------------------------------------------------- Zach's part

main()
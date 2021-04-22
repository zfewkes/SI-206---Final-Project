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
    cur.execute('''CREATE TABLE IF NOT EXISTS ''' + name + '''(id INTEGER PRIMARY KEY, game_id INTEGER UNIQUE,
     home_team_score INTEGER, away_team_score INTEGER, agg_score INTEGER,
     stadium_hometeam_id INTEGER, home_team_names TEXT, away_team_names TEXT)''')
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

#setUpDatabase('hockey.db')


def getScores():
    #Function returns game data for each game played in the NHL in the season
    url = "https://v1.hockey.api-sports.io/games/"
    payload={}
    headers = {'x-rapidapi-key': 'e183f3258ead601b2e1d06804f59d49e', 'x-rapidapi-host': 'v1.hockey.api-sports.io'}
    param_league = {'id':'57','season':'2019'}
    param_games = {'league':'57','season':'2019'}
    response = requests.get(url, headers=headers, params=param_games)
    data = json.loads(response.text)
    return data

def getArenas():
    #Function returns team data for each team in the NHL
    url = "https://v1.hockey.api-sports.io/teams/"
    payload={}
    headers = {'x-rapidapi-key': 'e183f3258ead601b2e1d06804f59d49e', 'x-rapidapi-host': 'v1.hockey.api-sports.io'}
    param_league = {'id':'57','season':'2019'}
    param_teams = {'league':'57','season':'2019'}
    response = requests.get(url, headers=headers, params=param_teams)
    data = json.loads(response.text)
    #print(data)
    return data
getArenas()

arena_data = getArenas()
game_data = getScores()

def parseScores(data):
    #Function returns parsed data from each game ordered by index
    #Function then concatenates it all into a list of dictionaries
    #Stadium id is also the home team id
    scores = []
    home_team_scores = []
    away_team_scores = []
    total_scores = []
    game_ids = []
    id_num = 0
    home_teams = []
    list_dict = []
    home_team_names = []
    away_team_names = []
    for game in data['response']:
        scores.append(game['scores'])
        home_teams.append((game['teams'].get('home')).get('id'))
        home_team_names.append(game['teams']['home']['name'])
        away_team_names.append(game['teams']['away']['name'])
    for game in scores:
        home_team_scores.append(game.get('home'))
        away_team_scores.append(game.get('away'))
        total_scores.append(game.get('home')+game.get('away'))
        game_ids.append(id_num)
        id_num=id_num+1
    for index in range(len(home_team_scores)):
        total_scores.append(
           int(home_team_scores[index])+int(away_team_scores[index]) 
        )
    #print(game_ids)
    for x in range(len(scores)):
        game_dict = {}
        game_dict['id']=game_ids[x]
        game_dict['home_team_score']=home_team_scores[x]
        game_dict['away_team_score']=away_team_scores[x]
        game_dict['total_score']=total_scores[x]
        game_dict['stadium_id']=home_teams[x]
        game_dict['home_team_name']=home_team_names[x]
        game_dict['away_team_name']=away_team_names[x]
        list_dict.append(game_dict)
    return list_dict
parseScores(game_data)

def parseArenas(data):
    #Function return dict of home team id and arena name
    home_team_id = []
    arena_names = []
    team_names = []
    list_dict = []
    for x in data['response']:
        home_team_id.append(x['id'])
        arena_names.append((x['arena']['name']))
        team_names.append(x['name'])
    #print(len(arena_names))
    #print(len(home_team_id))

    for x in range(len(home_team_id)):
        dic = {}
        dic['stadium_id']=home_team_id[x]
        dic['stadium_name']=arena_names[x]
        dic['team_name']=team_names[x]
        list_dict.append(dic)
    #print(list_dict)
    return list_dict
#parseArenas(arena_data)

def writing_arenadata(cur, conn):
    arena_dict = parseArenas(arena_data)
    for arena in arena_dict:
        print(arena)
    for stadium in arena_dict:
        cur.execute('INSERT OR IGNORE INTO Hockey_Stadiums (id, team, stadium) VALUES (?,?,?)',
        (int(stadium.get('stadium_id')), stadium.get('team_name'), stadium.get('stadium_name')))
    conn.commit()

def writing_gamedata(cur, conn):
    game_dict = parseScores(game_data)
    #for game in game_dict:
    #    print(game)
    for game in game_dict:
        cur.execute('''INSERT OR IGNORE INTO Hockey_games 
        (game_id, home_team_score, away_team_score,agg_score, stadium_hometeam_id, home_team_names, away_team_names) VALUES (?,?,?,?,?,?,?)''',
        (int(game.get('id')), int(game.get('home_team_score')), 
        int(game.get('away_team_score')), int(game.get('total_score')), 
        int(game.get('stadium_id')), game.get('home_team_name'), game.get('away_team_name')))
    conn.commit()

setUpDatabase('Sports.db')
cur, conn = setUpDatabase('Sports.db')   
delTable('hockey_games', cur, conn) 
setUpLocation_TeamTable("hockey_stadiums", cur, conn)
writing_arenadata(cur, conn)
setUpSportsTable('hockey_games', cur, conn)
writing_gamedata(cur, conn)


#parseScores(game_data)
#parseArenas(arena_data)

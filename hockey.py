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

#arena_data = getArenas()
#game_data = getScores()

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
    game_dict = {}
    list_dict = []
    for game in data['response']:
        scores.append(game['scores'])
        home_teams.append((game['teams'].get('home')).get('id'))
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
    for x in range(len(scores)):
        game_dict['id']=game_ids[x]
        game_dict['home_team_score']=home_team_scores[x]
        game_dict['away_team_score']=away_team_scores[x]
        game_dict['total_score']=total_scores[x]
        game_dict['stadium_id']=home_teams[x]
        list_dict.append(game_dict)
    print(list_dict)
    return list_dict


def parseArenas(data):
    #Function return dict of home team id and arena name
    dic = {}
    home_team_id = []
    arena_name = []
    list_dict = []
    for x in data['response']:
        home_team_id.append(x['id'])
        arena_name.append((x['arena']['name']))
    for x in range(len(home_team_id)):
        dic['stadium_id']=home_team_id[x]
        dic['full_name']=arena_name[x]
    return list_dict

def writing_arenadata(cur, conn):
    arena_dict = parseArenas(arena_data)
    for team in arena_dict:
        cur.execute('INSERT OR IGNORE INTO Basketball_teams_stadiums (id,team) VALUES (?,?)',
        (int(team.get('id')), team.get('full_name')))
    conn.commit()


def writing_gamedata(cur, conn):
    game_dict = parseScores(game_data)
    for game in game_dict:
        cur.execute('''INSERT OR IGNORE INTO Basketball (game_id, home_team_score, away_team_score,
        agg_score, stadium_hometeam_id) VALUES (?,?,?,?,?)''',
        (int(game.get('id')), int(game.get('home_team_score')), 
        int(game.get('away_team_score')), int(game.get('total_score')), 
        int(game.get('stadium_id')))
    conn.commit()

#__________________________________________________________________________
#Setting up and using functions
def main():
    cur, conn = setUpDatabase('hockey.db')
    
    setUpLocation_TeamTable("hockey_stadiums", cur, conn)
    writing_arenadata(cur, conn)

    setUpSportsTable('hockey_games', cur, conn)
    writing_gamedata(cur, conn)


#parseScores(game_data)
#parseArenas(arena_data)
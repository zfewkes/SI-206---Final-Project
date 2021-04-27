from bs4 import BeautifulSoup
import requests
import json
import os
import sqlite3

def setUpDatabase(db_name):
    #Reads from the database file and returns the database cursor and connection
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def createSportsTable(name, cur, conn):
    #Creates datatable for information of every match in 2019-2020 Premier League season.
    cur.execute('''CREATE TABLE IF NOT EXISTS ''' + name + '''(id INTEGER PRIMARY KEY, game_id INTEGER UNIQUE,
     home_team_score INTEGER, away_team_score INTEGER, agg_score INTEGER,
     stadium_hometeam_id INTEGER, away_team_id INTEGER)''')
    conn.commit()
    print('here')

def createLocation_TeamTable(name, cur, conn):
    #Creates datatable for every team and its stadium. This table uses 
    cur.execute('''CREATE TABLE IF NOT EXISTS ''' + name + ''' (id INTEGER PRIMARY KEY UNIQUE,
    team TEXT, stadium TEXT)''')
    conn.commit()
    print('here')


def get_team_ids():
    try: 
        url = "https://api-football-v1.p.rapidapi.com/v2/teams/league/524"

        headers = {
        'x-rapidapi-key': "611077d929msh0d5d946c11e8245p1cfdbajsn0c38ff1bf50a",
        'x-rapidapi-host': "api-football-v1.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers)
        t = response.text
        data = json.loads(t)
        return data
    
    except:
        print("Exception")
        return None 


#def get_stadiums():
    #tup_list = []
    #r = requests.get('https://www.stadiumguide.com/premier-league-stadiums/')
    #soup = BeautifulSoup(r.content, 'html.parser')
    #tag = soup.find('tbody')
    #for row in tag.find_all('tr'):
        #for i in row.find_all('td', class_='column-3'):
            #stadium = i.find('a').text.strip()
            #tup_list.append(stadium)
    #return tup_list


def get_game_results():
    tup_list = []
    team_list = []
    row_count = 0
    r = requests.get('https://en.wikipedia.org/wiki/2019–20_Premier_League')
    soup = BeautifulSoup(r.content, 'html.parser')
    table_tag = soup.find('table', class_='wikitable plainrowheaders')
    row_tags = table_tag.find_all('tr')
    for row in row_tags[1:]:
        column_count = 0 
        column_tags = row.find_all('td')
        team_name = row.find("th").text.strip()
        
        if team_name=='Brighton & Hove Albion':
            team_name='Brighton'
        if team_name=='Sheffield United':
            team_name='Sheffield Utd'
        if team_name=='Norwich City':
            team_name='Norwich'
        if team_name=='Tottenham Hotspur':
            team_name='Tottenham'
        if team_name=='Wolverhampton Wanderers':
            team_name='Wolves'
        if team_name=='Leicester City':
            team_name='Leicester'
        if team_name=='West Ham United':
            team_name='West Ham'
        if team_name=='Newcastle United':
            team_name='Newcastle'

        team_list.append((row_count, team_name))
        for column in column_tags:
            score = column.text.strip()
            if score != "—":
                tup_list.append((row_count, column_count, score[0], score[2]))
            column_count += 1
        row_count += 1
    return tup_list, team_list



def write_to_soccer_db(data, team_list, team_stadium_dict, cur, conn):
    game_id=1
    count = 1
    for item in data:
        if item[0] in team_stadium_dict and count < 26:
            affectedRow = cur.execute('''INSERT OR IGNORE INTO Soccer (game_id, home_team_score, away_team_score,
            agg_score, stadium_hometeam_id, away_team_id) VALUES (?,?,?,?,?,?)''',
            (game_id, int(item[2]), int(item[3]),
            int(item[2]) + int(item[3]), 
            int(team_stadium_dict[item[0]]),
            int(team_stadium_dict[item[1]])))
            game_id += 1
            if affectedRow.rowcount == 1:
                count += affectedRow.rowcount
    conn.commit()


def write_to_soccer_teams_stadiums(data, cur, conn):
    for item in data:
        cur.execute('INSERT OR IGNORE INTO Soccer_teams_stadiums (id, team, stadium) VALUES (?,?,?)',
         (item[0], item[1], item[2]))
    conn.commit()





def main():

    cur, conn = setUpDatabase('Sports.db')
    

    createLocation_TeamTable('Soccer_teams_stadiums', cur, conn)
    team_table_json = get_team_ids()
    #tup_list = get_stadiums()

    stadium_list=[]
    stadium_id=1
    for item in team_table_json['api']['teams']:
        stadium_list.append((stadium_id, item.get('name', None), item.get('venue_name', None)))
        stadium_id+=1

    write_to_soccer_teams_stadiums(stadium_list, cur, conn)
    #print (team_table_json)
    #print(tup_list)

    createSportsTable('Soccer', cur, conn)
    game_list, team_list = get_game_results()
    #print(game_list, team_list)

    #print(stadium_list)
    team_stadium_dict={}
    for team in team_table_json['api']['teams']:
        for x in team_list:
            if x[1] == team.get('name',None):
                for y in stadium_list:
                    if y[2]==team.get('venue_name', None):
                        team_stadium_dict[x[0]]=y[0]  
      
    #print(team_stadium_dict)

    write_to_soccer_db(game_list, team_list, team_stadium_dict, cur, conn)

main()
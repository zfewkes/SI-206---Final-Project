import sqlite3
import matplotlib
import matplotlib.pyplot as plt
import csv
import json
import numpy as np
import statistics
import os
import sklearn
from sklearn import preprocessing
import plotly.graph_objects as go
import plotly.express as px
 
def setUpDatabase(db_name):
   #Sets up db and creates connection
   path = os.path.dirname(os.path.abspath(__file__))
   conn = sqlite3.connect(path+'/'+db_name)
   cur = conn.cursor()
   return cur, conn
 
 
def pullBasketball(cur, con):
   #pulls out data from db about the total scores for each team
   cur.execute('SELECT Basketball.home_team_id FROM Basketball'
   )
   score_dict = {}
   team_dict = {}
   cur.execute('''SELECT Basketball.home_team_score, Basketball_teams_stadiums.team
           FROM Basketball JOIN Basketball_teams_stadiums
           ON Basketball.home_team_id = Basketball_teams_stadiums.id''')
   for game in cur:
       if game[1] not in score_dict:
           score_dict[game[1]]=game[0]
       else:
           score_dict[game[1]]=score_dict[game[1]]+game[0]
       if game[1] not in team_dict:
           team_dict[game[1]]=[game[0]]
       else:
           team_dict[game[1]]=team_dict[game[1]]+[game[0]]
   cur.execute('''SELECT Basketball.away_team_score, Basketball_teams_stadiums.team
               FROM Basketball JOIN Basketball_teams_stadiums
               ON Basketball.visitor_team_id = Basketball_teams_stadiums.id''')
   for game in cur:
       if game[1] not in score_dict:
           score_dict[game[1]]=game[0]
       else:
           score_dict[game[1]]=score_dict[game[1]]+game[0]
       if game[1] not in team_dict:
           team_dict[game[1]]=[game[0]]
       else:
           team_dict[game[1]]=team_dict[game[1]]+[game[0]]
   return score_dict, team_dict
 
 
def pullHockey(cur, con):
   #pulls out data from db about home team scores and away team scores and returns 2 lists for each sport
   score_dict = {}
   team_dict = {}
   cur.execute('''SELECT hockey_games.home_team_score, hockey_stadiums.team
               FROM hockey_games JOIN hockey_stadiums
               ON hockey_games.hometeam_id = hockey_stadiums.hometeam_id''')
   for game in cur:
       if game[1] not in score_dict:
           score_dict[game[1]]=game[0]
       else:
           score_dict[game[1]]=score_dict[game[1]]+game[0]
       if game[1] not in team_dict:
           team_dict[game[1]]=[game[0]]
       else:
           team_dict[game[1]]=team_dict[game[1]]+[game[0]]
   cur.execute('''SELECT hockey_games.away_team_score, hockey_stadiums.team
               FROM hockey_games JOIN hockey_stadiums
               ON hockey_games.away_team_id = hockey_stadiums.hometeam_id''')
   for game in cur:
       if game[1] not in score_dict:
           score_dict[game[1]]=game[0]
       else:
           score_dict[game[1]]=score_dict[game[1]]+game[0]
       if game[1] not in team_dict:
           team_dict[game[1]]=[game[0]]
       else:
           team_dict[game[1]]=team_dict[game[1]]+[game[0]]
   return score_dict, team_dict
  
 
def pullSoccer(cur, con):
   #pulls out data from db about home team scores and away team scores and returns 2 lists for each sport  
   #score_dict is team:all scores combined, and team_dict is team: list of scores
   score_dict = {}
   team_dict = {}
   cur.execute('''SELECT Soccer.home_team_score, Soccer_teams_stadiums.team
               FROM Soccer JOIN Soccer_teams_stadiums
               ON Soccer.stadium_hometeam_id = Soccer_teams_stadiums.id''')
   for game in cur:
       if game[1] not in score_dict:
           score_dict[game[1]]=game[0]
       else:
           score_dict[game[1]]=score_dict[game[1]]+game[0]
       if game[1] not in team_dict:
           team_dict[game[1]]=[game[0]]
       else:
           team_dict[game[1]]=team_dict[game[1]]+[game[0]]
   cur.execute('''SELECT Soccer.away_team_score, Soccer_teams_stadiums.team
               FROM Soccer JOIN Soccer_teams_stadiums
               ON Soccer.away_team_id = Soccer_teams_stadiums.id''')
   for game in cur:
       if game[1] not in score_dict:
           score_dict[game[1]]=game[0]
       else:
           score_dict[game[1]]=score_dict[game[1]]+game[0]
       if game[1] not in team_dict:
           team_dict[game[1]]=[game[0]]
       else:
           team_dict[game[1]]=team_dict[game[1]]+[game[0]]
   return score_dict, team_dict
 
 
def sortScores(dic, dic1):
   sorted_dic = {k: v for k, v in sorted(dic.items(), key=lambda item: item[1], reverse=True)}
   #print(sorted_dic)
   #print(dic1)
   return sorted_dic, dic1
 
 
def normalize(dic, dic1):
   #takes in xlist and ylist and returns normalized values
   #team_means is a dictionary of teams:team_means
   team_means = {}
   means_lst = []
   stand = []
   normalized_scores = {}
   for team in dic1:
       team_means[team]=sum(dic1.get(team))/len(dic1.get(team))
   for x in team_means:
       means_lst.append(team_means.get(x))
   all_mean = sum(means_lst)/len(means_lst) 
   for team in dic1:
       for score in dic1.get(team):
           stand.append(score)
   standard_deviation = statistics.stdev(stand)
   for team in dic1:
       normalized_scores[team]=abs((team_means.get(team)-all_mean)/(standard_deviation))
   return normalized_scores
 
 
def visualize_scatter(sorted_teams, normalized, name):
   top_ten = []
   norm_ten = {}
   count = 1
   for team in sorted_teams[0].keys():
           top_ten.append(team)
   #print(sorted_teams[0])
   #print(top_ten[:10])
   for team in top_ten[:10]:
           norm_ten[team]=normalized.get(team)
           count=count+1
   sorted_norm = {k: v for k, v in sorted(norm_ten.items(), key=lambda item: item[1], reverse=True)}
   xlist = list(sorted_norm.keys())
   ylist = list(sorted_norm.values())
  
   fig1 = go.Bar(x = xlist,y = ylist)
   layout = go.Layout(title = go.layout.Title(text='Normalized Score data for top 10 ' + name + ' teams',xref='paper',x = 0,),
       xaxis = go.layout.XAxis(
           title = go.layout.xaxis.Title(
               text = 'Top 10 Teams by Score'
           )
       ),
       yaxis = go.layout.YAxis(
           title = go.layout.yaxis.Title(
               text = 'Normalized Average Scores'
           )
       )
   )
   fig2 = go.Figure(data=fig1, layout=layout)
   fig2.show()
 
  
 
 
cur, conn = setUpDatabase('Sports.db')
basketball_dicts = pullBasketball(cur, conn)
soccer_dicts = pullSoccer(cur, conn)
hockey_dicts = pullHockey(cur, conn)
 
sorted_basketball = sortScores(basketball_dicts[0], basketball_dicts[1])
sorted_soccer = sortScores(soccer_dicts[0], soccer_dicts[1])
sorted_hockey = sortScores(hockey_dicts[0], hockey_dicts[1])
 
normalized_soc = normalize(sorted_soccer[0], sorted_soccer[1])
normalized_bask = normalize(sorted_basketball[0], sorted_basketball[1])
normalized_hock = normalize(sorted_hockey[0], sorted_hockey[1])
 
 
processed = visualize_scatter(sorted_soccer, normalized_soc, 'Soccer')
processed = visualize_scatter(sorted_basketball, normalized_bask, 'Basketball')
processed = visualize_scatter(sorted_hockey, normalized_hock, 'Hockey')
 

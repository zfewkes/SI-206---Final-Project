#data processing

import matplotlib
import matplotlib.pyplot as plt
import sqlite3
import os
import seaborn as sns
import numpy as np
import pandas as pd

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def game_score_plot(all_scores, cur, conn):
   
    sns.set_theme()
    ax = sns.distplot(all_scores['basketball'], kde_kws={'bw_adjust' : 1.2})
    ax.set_title('Aggregate Basketball Score Densities and KDE')
    ax.set_xlabel('Scores')
    plt.show()

    ax = sns.distplot(all_scores['hockey'], color = 'r', kde_kws={'bw_adjust' : 1.8})
    ax.set_title('Aggregate Hockey Score Densities and KDE')
    ax.set_xlabel('Scores')
    plt.show()

    ax = sns.distplot(all_scores['soccer'], color = 'black', kde_kws={'bw_adjust' : 1.8})
    ax.set_title('Aggregate Soccer Score Densities and KDE')
    ax.set_xlabel('Scores')
    plt.show()

    ax = sns.distplot(all_scores['basketball'])
    ax = sns.distplot(all_scores['hockey'], color = 'r')
    ax = sns.distplot(all_scores['soccer'], color = 'black')
    plt.legend(labels=['Basketball', 'Hockey', 'Soccer'])
    ax.set_title('All Densities and KDE')
    ax.set_xlabel('Scores')
    plt.show()

#getting certain data from the Database
def working_agg_scores(names, cur, conn):
    score_dict = {}
    for name in names:
        cur.execute('''SELECT agg_score FROM ''' + name)
        score_list = []
        for item in cur:
            score_list.append(item[0])
        score_dict[name] = score_list
        del score_list
    return score_dict

def working_home_scores(names, cur, conn):
    score_dict = {}
    for name in names:
        cur.execute('''SELECT home_team_score FROM ''' + name)
        score_list = []
        for item in cur:
            score_list.append(item[0])
        score_dict[name] = score_list
        del score_list
    return score_dict

def working_away_scores(names, cur, conn):
    score_dict = {}
    for name in names:
        cur.execute('''SELECT away_team_score FROM ''' + name)
        score_list = []
        for item in cur:
            score_list.append(item[0])
        score_dict[name] = score_list
        del score_list
    return score_dict

def calc_median_std(all_scores, cur, conn):
    #Using numpy arrays to calculate mean, median, and standard deviation
    #for the entire sport
    #stored as a dictionary with the sport as a key, and the values as
    #dictionaries with the mean, median, and mode as keys and the values
    #cooresponding to those vals for the sport.

    stats_dict = {}
    hockey_arr = np.array(all_scores['hockey'])
    stats_dict['hockey'] = {}
    stats_dict['hockey']['mean'] = np.mean(hockey_arr)
    stats_dict['hockey']['median'] = np.median(hockey_arr)
    stats_dict['hockey']['std'] = np.std(hockey_arr)

    hockey_arr = np.array(all_scores['soccer'])
    stats_dict['soccer'] = {}
    stats_dict['soccer']['mean'] = np.mean(hockey_arr)
    stats_dict['soccer']['median'] = np.median(hockey_arr)
    stats_dict['soccer']['std'] = np.std(hockey_arr)

    hockey_arr = np.array(all_scores['basketball'])
    stats_dict['basketball'] = {}
    stats_dict['basketball']['mean'] = np.mean(hockey_arr)
    stats_dict['basketball']['median'] = np.median(hockey_arr)
    stats_dict['basketball']['std'] = np.std(hockey_arr)

    #print('here')

#gets a dictionary with the sports as keys and the 
#values as a list of the team name, mean, median, and standard 
#deviation in that order
#just take all the data as it comes 
#write to each thingy 
#to collect --> loop throught id's?
def calc_med_mean_std_per_team(cur, conn):

    team_stats_dict = {'soccer' : [], 'hockey': [], 'basketball': []}
    team_scores_dict = {}
    
    #basketball
    # I want the scores of all the games in which each played
    #two steps ---> 1.all home and  2. all away
    cur.execute('''SELECT Basketball.home_team_score, Basketball_teams_stadiums.team
                FROM Basketball JOIN Basketball_teams_stadiums
                ON Basketball.home_team_id = Basketball_teams_stadiums.id''')

    for item in cur:
        team_scores_dict[item[1]] = team_scores_dict.get(item[1], []) + [item[0]]

    #GETTING VISITOR TEAM DATA
    cur.execute('''SELECT Basketball.away_team_score, Basketball_teams_stadiums.team
                FROM Basketball JOIN Basketball_teams_stadiums
                ON Basketball.visitor_team_id = Basketball_teams_stadiums.id''')

    for item in cur:
        team_scores_dict[item[1]] = team_scores_dict.get(item[1], []) + [item[0]]

    #Getting the stats------------------------------------------------------------
    
    for item in team_scores_dict:
        team_np_arr = np.array(team_scores_dict[item])
        team_stats_dict['basketball'].append({'team': item, 
        'mean' : np.mean(team_np_arr), 
        'median' : np.median(team_np_arr),
        'std' : np.std(team_np_arr)
        })

    #done with bball--------------------------------------------------------------



def main():

    #collecting the data from the database----------------------------------------
    cur, conn = setUpDatabase('Sports.db')
    names = ['Basketball', 'hockey_games', 'Soccer']
    agg_scores = working_agg_scores(names, cur, conn)
    home_scores = working_home_scores(names, cur, conn)
    away_scores = working_away_scores(names, cur, conn)

    all_scores = {}
    print(len(home_scores['hockey_games']))
    all_scores['hockey'] = home_scores['hockey_games'] + away_scores['hockey_games']
    all_scores['soccer'] = home_scores['Soccer'] + away_scores['Soccer']
    all_scores['basketball'] = home_scores['Basketball'] + away_scores['Basketball']
    print(len(all_scores['hockey']))

    #Finished data collection------------------------------------------------------
    
    #data processing---------------------------------------------------------------
    stats_dict = calc_median_std(all_scores, cur, conn)
    calc_med_mean_std_per_team(cur, conn)





    #end data processing-----------------------------------------------------------

    #visualizations----------------------------------------------------------------
    game_score_plot(all_scores, cur, conn)





    #end visualizations------------------------------------------------------------



main()

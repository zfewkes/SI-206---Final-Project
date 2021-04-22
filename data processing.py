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
    #getting the total number of scores and dividing them by the total
    #sum to get a mean value and also the median and standard deviation. 
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

    print('here')
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
    




    #end data processing-----------------------------------------------------------

    #visualizations----------------------------------------------------------------
    game_score_plot(all_scores, cur, conn)





    #end visualizations------------------------------------------------------------



main()

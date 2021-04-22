#data processing

import matplotlib
import matplotlib.pyplot as plt
import sqlite3
import os
import seaborn as sns
import numpy as np

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def game_score_plot(agg_scores, cur, conn):
   
    sns.set_theme()
    ax = sns.distplot(agg_scores['Basketball'])
    ax.set_title('Basketball Densities and KDE')
    ax.set_xlabel('Scores')
    plt.show()

    ax = sns.distplot(agg_scores['hockey_games'], color = 'r')
    ax.set_title('Hockey Densities and KDE')
    ax.set_xlabel('Scores')
    plt.show()

    ax = sns.distplot(agg_scores['Soccer'], color = 'black')
    ax.set_title('Soccer Densities and KDE')
    ax.set_xlabel('Scores')
    plt.show()

    ax = sns.distplot(agg_scores['Basketball'])
    ax = sns.distplot(agg_scores['hockey_games'], color = 'r')
    ax = sns.distplot(agg_scores['Soccer'], color = 'black')
    plt.legend(labels=['Basketball', 'Hockey', 'Soccer'])
    ax.set_title('All Densities and KDE')
    ax.set_xlabel('Scores')
    plt.show()

def working_agg_scores(names, cur, conn):
    score_dict = {}
    for name in names:
        cur.execute('''SELECT agg_score FROM ''' + name + ''' LIMIT 200''')
        score_list = []
        for item in cur:
            score_list.append(item[0])
        score_dict[name] = score_list
        del score_list
    return score_dict

def normalized_scores(agg_scores, cur, conn):
    

def main():
    cur, conn = setUpDatabase('Sports.db')
    names = ['Basketball', 'hockey_games', 'Soccer']
    agg_scores = working_agg_scores(names, cur, conn)
    #print(agg_scores)
    game_score_plot(agg_scores, cur, conn)



main()

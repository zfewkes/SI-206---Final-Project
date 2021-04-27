#data processing

import matplotlib.pyplot as plt
import sqlite3
import os
import seaborn as sns
import numpy as np
import json
import plotly.graph_objects as go

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

#this is a seaborn graph of the kde and the general distribution
def game_score_plot(all_scores):
   
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
def working_agg_scores(names, cur):
    score_dict = {}
    for name in names:
        cur.execute('''SELECT agg_score FROM ''' + name)
        score_list = []
        for item in cur:
            score_list.append(item[0])
        score_dict[name] = score_list
        del score_list
    return score_dict


def working_home_scores(names, cur):
    score_dict = {}
    for name in names:
        cur.execute('''SELECT home_team_score FROM ''' + name)
        score_list = []
        for item in cur:
            score_list.append(item[0])
        score_dict[name] = score_list
        del score_list
    return score_dict


def working_away_scores(names, cur):
    score_dict = {}
    for name in names:
        cur.execute('''SELECT away_team_score FROM ''' + name)
        score_list = []
        for item in cur:
            score_list.append(item[0])
        score_dict[name] = score_list
        del score_list
    return score_dict


def calc_agg_mean_median_std(all_scores):
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
    return stats_dict
    #print('here')

#gets a dictionary with the sports as keys and the 
#values as a list of the team name, mean, median, and standard 
#deviation in that order
#just take all the data as it comes 
#write to each thingy 
#to collect --> loop throught id's?
def calc_med_mean_std_per_team(cur):

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
    
    #Soccer-----------------------------------------------------------------------
    team_scores_dict = {}
    cur.execute('''SELECT Soccer.home_team_score, Soccer_teams_stadiums.team
                FROM Soccer JOIN Soccer_teams_stadiums
                ON Soccer.stadium_hometeam_id = Soccer_teams_stadiums.id''')

    for item in cur:
        team_scores_dict[item[1]] = team_scores_dict.get(item[1], []) + [item[0]]

    #GETTING VISITOR TEAM DATA
    cur.execute('''SELECT Soccer.away_team_score, Soccer_teams_stadiums.team
                FROM Soccer JOIN Soccer_teams_stadiums
                ON Soccer.away_team_id = Soccer_teams_stadiums.id''')

    for item in cur:
        team_scores_dict[item[1]] = team_scores_dict.get(item[1], []) + [item[0]]

    for item in team_scores_dict:
        team_np_arr = np.array(team_scores_dict[item])
        team_stats_dict['soccer'].append({'team': item, 
        'mean' : np.mean(team_np_arr), 
        'median' : np.median(team_np_arr),
        'std' : np.std(team_np_arr)
        })
    
    #end soccer--------------------------------------------------------------------
    #Hockey------------------------------------------------------------------------
    team_scores_dict = {}
    cur.execute('''SELECT hockey_games.home_team_score, hockey_stadiums.team
                FROM hockey_games JOIN hockey_stadiums
                ON hockey_games.hometeam_id = hockey_stadiums.hometeam_id''')

    for item in cur:
        team_scores_dict[item[1]] = team_scores_dict.get(item[1], []) + [item[0]]

    #GETTING VISITOR TEAM DATA
    cur.execute('''SELECT hockey_games.away_team_score, hockey_stadiums.team
                FROM hockey_games JOIN hockey_stadiums
                ON hockey_games.away_team_id = hockey_stadiums.hometeam_id''')

    for item in cur:
        team_scores_dict[item[1]] = team_scores_dict.get(item[1], []) + [item[0]]

    for item in team_scores_dict:
        team_np_arr = np.array(team_scores_dict[item])
        team_stats_dict['hockey'].append({'team': item, 
        'mean' : np.mean(team_np_arr), 
        'median' : np.median(team_np_arr),
        'std' : np.std(team_np_arr)
        })

    return team_stats_dict


    #end hockey--------------------------------------------------------------------

def write_out_json(filename, team_stats):
    """
    This function encodes the cache dictionary (CACHE_DICT) into JSON format and
    writes the JSON to the cache file (CACHE_FNAME) to save the search results.
    """
    json_file = json.dumps(team_stats)

    dir = os.path.dirname(__file__)
    outFile = open(os.path.join(dir, filename), 'w')
    outFile.write(json_file)  #writes over the file... Doesn't save it!
    outFile.close()

#finds the teams who's median score is the highest (in terms of standard deviation)
#away from its own distributions median
def find_top_teams(agg_stats, team_stats):
    #basketball!
    bball_mean_score = agg_stats['basketball']['mean']
    bball_std = agg_stats['basketball']['std']
    dist_from_avg = {}
    for item in team_stats['basketball']:
        dist_from_avg[item['team']] = (item['mean'] - bball_mean_score) / bball_std

    #Soccer!
    soc_mean_score = agg_stats['soccer']['mean']
    soc_std = agg_stats['soccer']['std']
    for item in team_stats['soccer']:
        dist_from_avg[item['team']] = (item['mean'] - soc_mean_score) / soc_std

    #Hockey!
    hoc_mean_score = agg_stats['hockey']['mean']
    hoc_std = agg_stats['hockey']['std']
    for item in team_stats['hockey']:
        dist_from_avg[item['team']] = (item['mean'] - hoc_mean_score) / hoc_std



    #calculating best teams...
    tup_dist_from_avg = dist_from_avg.items()

    tup_dist_from_avg = sorted(tup_dist_from_avg, key = lambda t: t[1], reverse=True)
    return tup_dist_from_avg

#a simple plotly bar graph
def plot_top_teams(top_teams):
    
    teams = []
    scores = []
    for i in range(10):
        teams.append(top_teams[i][0])
        scores.append(top_teams[i][1])

    fig = go.Figure([go.Bar(x=teams, y=scores)])
    title_str = "Top 10 teams by standard deviation(s) above mean"
    fig.update_layout(title = title_str, xaxis_tickangle=-45, barmode='group',
                  xaxis = {'tickmode':'linear'}, xaxis_title="Teams",
    yaxis_title="Standard deviations from sport mean")
    fig.show()

def main():

    #collecting the data from the database----------------------------------------
    cur, conn = setUpDatabase('Sports.db')
    names = ['Basketball', 'hockey_games', 'Soccer']
    #agg_scores = working_agg_scores(names, cur)
    home_scores = working_home_scores(names, cur)
    away_scores = working_away_scores(names, cur)

    all_scores = {}
    #print(len(home_scores['hockey_games']))
    all_scores['hockey'] = home_scores['hockey_games'] + away_scores['hockey_games']
    all_scores['soccer'] = home_scores['Soccer'] + away_scores['Soccer']
    all_scores['basketball'] = home_scores['Basketball'] + away_scores['Basketball']
    #print(len(all_scores['hockey']))

    #Finished data collection------------------------------------------------------
    #data processing---------------------------------------------------------------
    agg_stats_dict = calc_agg_mean_median_std(all_scores)
    team_stats_dict = calc_med_mean_std_per_team(cur)

    write_out_json('all_stats.json', team_stats_dict)
    write_out_json('agg_stats.json', agg_stats_dict)

    top_teams = find_top_teams(agg_stats_dict, team_stats_dict)

    #end data processing-----------------------------------------------------------
    #visualizations----------------------------------------------------------------
    game_score_plot(all_scores)
    plot_top_teams(top_teams)




    #end visualizations------------------------------------------------------------



main()

import json
import os 
import sqlite3
#import chart_studio.plotly as py
import plotly.graph_objs as go


def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn


def calculation(conn, cur):
    
    cur.execute('''SELECT Soccer_teams_stadiums.stadium,avg(home_team_score) FROM Soccer
        INNER JOIN Soccer_teams_stadiums ON Soccer.stadium_hometeam_id=Soccer_teams_stadiums.id
        GROUP BY stadium_hometeam_id''')
    stadium_dict = {}
    rows = cur.fetchall()
    for row in rows:
        stadium_dict[row[0]] = row[1]
    return stadium_dict


def write_file(stadium_dict):
    json_file = json.dumps(stadium_dict)
    f = open("soccer_calculations.json","w")
    f.write(json_file)
    f.close()

    
def sort_tuples(stadium_dict, number):
    stadium_goal_tuples = stadium_dict.items()
    tuple_list = []
    for tup in stadium_goal_tuples:
        tuple_list.append(tup)
    stadium_goal_sorted = sorted(tuple_list, key=lambda tup: tup[1], reverse = True)

    return stadium_goal_sorted[:number]


def create_graph(stadium_goal_sorted):
    stadium_list = []
    score_list = []

    for t in stadium_goal_sorted:
        stadium_list.append(t[0])
        score_list.append(t[1])

    colors=["rgba(160,90,160,.9)",
            "rgba(140,220,150,.9)",
            "rgba(240,110,160,.9)",
            "rgba(20,210,250,.9)",
            "rgba(210,210,0,.9)",
            "rgba(160,90,160,.9)",
            "rgba(140,220,150,.9)",
            "rgba(240,110,160,.9)",
            "rgba(20,210,250,.9)",
            "rgba(210,210,0,.9)",
            "rgba(160,90,160,.9)",
            "rgba(140,220,150,.9)",
            "rgba(240,110,160,.9)",
            "rgba(20,210,250,.9)",
            "rgba(210,210,0,.9)",
            "rgba(160,90,160,.9)",
            "rgba(140,220,150,.9)",
            "rgba(240,110,160,.9)",
            "rgba(20,210,250,.9)",
            "rgba(210,210,0,.9)"]

    trace1 = go.Bar(x = stadium_list,y = score_list,marker = dict(color = colors[:len(stadium_goal_sorted)]))

    data = trace1
    layout = go.Layout(
        title = go.layout.Title(
            text='Top 10 Premier League Stadiums by Average Hometeam Goals Scored',
            xref='paper',
            x = 0,   
        ),
        xaxis = go.layout.XAxis(
            title = go.layout.xaxis.Title(
                text = 'Premier League Stadiums'
            )
        ),
        yaxis = go.layout.YAxis(
            title = go.layout.yaxis.Title(
                text = 'Average Goals Made At Home'
            )
        )
    )

    figure = go.Figure(data=data,layout=layout)
    figure.show()


def main():
    cur, conn = setUpDatabase('Sports.db')
    stadium_dict = calculation(conn, cur)
    stadium_goal_sorted = sort_tuples(stadium_dict, 10)
    write_file(stadium_goal_sorted)
    create_graph(stadium_goal_sorted)

main()

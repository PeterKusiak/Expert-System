from flask import Flask, render_template, request
from engine import Engine
import json

URL_PREFIX = ''

app = Flask(__name__)
#engine = Engine(D2KNearestNeighbors())
engine = Engine("")

def get_api_string(recommendations, prob):
    recommendations = list(map(str, recommendations))
    return json.dumps({'x': recommendations, 'prob_x': prob})

@app.route("/")
def index():
    return render_template('index.html')

@app.route(URL_PREFIX + "/api/suggest/")
def api():
    if 'x' not in request.args or 'y' not in request.args or 'z' not in request.args:
        return 'Invalid request'
    my_team = request.args['x'].split(',')
    if len(my_team) == 1 and my_team[0] == '':
        my_team = []
    else:
        my_team = map(int, my_team)

    their_team = request.args['y'].split(',')
    if len(their_team) == 1 and their_team[0] == '':
        their_team = []
    else:
        their_team = map(int, their_team)

    medal_lvl = request.args['z'].split(',')
    if len(medal_lvl) == 1 and medal_lvl[0] == '':
        medal_lvl = 1
    else:
        medal_lvl = medal_lvl[0]

    prob_recommendation_pairs,prob = engine.recommend(my_team, their_team,medal_lvl)
    recommendations = [hero for prob, hero in prob_recommendation_pairs]
    return get_api_string(recommendations, round(prob, 2))

if __name__ == "__main__":
    app.debug = False
    app.run()

from flask import Flask, render_template, request, jsonify
import json, logging, os, atexit

###########
from model import BoidFlockers
###################
app = Flask(__name__, static_url_path='')
model = BoidFlockers()
def updatePositions():
    global flock
    positions = []
    for boid in flock:
        boid.apply_behaviour(flock)
        boid.update()
        pos = boid.edges()
        positions.append(pos)
    return positions

def positionsToJSON(ps):
    posDICT = []
    for p in ps:
        pos = {
            "x" : p[0],
            "z" : p[1],
            "y" : p[2]
        }
        posDICT.append(pos)
    return json.dumps(posDICT)
# On IBM Cloud Cloud Foundry, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8000
port = int(os.getenv('PORT', 8000))

#########################
@app.route('/')
def root():
    return jsonify([{"message":"Hello World from IBM Cloud!"}])

@app.route('/A01336625',methods=['GET','POST'])
def A01336625():
    positions = model.step()
    return positionsToJSON(positions)
################################################################ NUEVO

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
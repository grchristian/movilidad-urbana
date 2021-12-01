from flask import Flask, render_template, request, jsonify
import json, logging, os, atexit

###########
import numpy as np
#from boid import Boid
from model import TrafficModel
###################
app = Flask(__name__, static_url_path='')

# On IBM Cloud Cloud Foundry, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8000
port = int(os.getenv('PORT', 8000))

#########################
#width = 12
#height = 12

# Set the number of agents here:
model = TrafficModel(2,7)
'''
def updatePositions():
    global flock
    positions = []
    for boid in flock:
        boid.apply_behaviour(flock)
        boid.update()
        pos = boid.edges()
        positions.append(pos)
    return positions
'''
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
############################## NUEVO

@app.route('/')
def root():
    return jsonify([{"message":"Hello World from IBM Cloud!"}])

@app.route('/controlTrafico',methods=['GET','POST'])
def controlTrafico():
    #positions = updatePositions()
    positions = model.step()
    resp = "{\"data\":" + positionsToJSON(positions) + "}"
    return resp.encode('utf-8')
################################################################ NUEVO

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
#from flask import Flask, render_template, request, jsonify
#import json, logging, os, atexit

from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid

from agents import Wall, VisualNode, TrafficLight, Road, Vehicles, ParkingLot
from model import TrafficModel

import random

def agent_portrayal(agent):

  portrayal = {}

  if type(agent) is Wall:
    portrayal = {
      "Shape": "rect",
      "Color": 'black',
      "Filled": "true",
      "Layer": 0,
      "w": 1,
      "h": 1,
    }

  if type(agent) is ParkingLot:
    if agent.hasCapacity():
      color = 'orange'
    else:
      color = 'purple'

    portrayal = {
      "Shape": "rect",
      "Color": color,
      "Filled": "true",
      "Layer": 3,
      "w": 1,
      "h": 1,
    }

  if type(agent) is VisualNode:
    portrayal = {
      "Shape": "circle",
      "Color": 'red',
      "Filled": "true",
      "Layer": 1,
      "r": 0.2
    }

  if type(agent) is TrafficLight:
    if agent.horiz == True:
      w, h = .25, .5
      color = 'green'
    else:
      w, h = .5, .25
      color = 'red'

    if agent.current_cycle == 1:
      color = 'green'
    else:
      color = 'red'

    portrayal = {
      "Shape": "rect",
      "Color": color,
      "Filled": "true",
      "Layer": 3,
      "w": w,
      "h": h,
    }

  if type(agent) is Road:
    portrayal = {
      "Shape": "rect",
      "Color": 'white',
      "Filled": "true",
      "Layer": 1,
      "w": 1,
      "h": 1,
    }

  if type(agent) is Vehicles:
    portrayal = {
      "Shape": "circle",
      "Color": 'blue',
      "Filled": "true",
      "Layer": 2,
      "r": 0.5
    }

  return portrayal


rows, cols = 20, 20
rows += 1
cols += 1
grid = CanvasGrid(agent_portrayal, rows, cols, 500, 500)

server = ModularServer(TrafficModel, [grid], "Road Traffic", 
  {
    'n_agents_per_iter': 2,
    'width': rows, 
    'height': cols
  }
)

server.port = 8521  # Default
server.launch()

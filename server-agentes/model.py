from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation

from agents import TrafficLight, Vehicles, Wall, Road, ParkingLot

class TrafficModel(Model):
  example = [
    ((0, 10), (21, 10)), # (0,10) , (20,10) = derecha +
    ((20, 11), (-1, 11)), # (20,11) , (0,11) = izquierda -

    ((10, 20), (10, -1)), # (10,20) , (10,0) = abajo -
    ((11, 0), (11, 21)), # (11,0) , (11,20) = arriba +
  ]

  def __init__(self, n_agents_per_iter=4, max_agents=20, road_list=example, width=21, height=21):
    self.grid = MultiGrid(width, height, True)
    self.schedule = RandomActivation(self)

    #Agent Gen
    self.n_agents_per_iter = n_agents_per_iter
    self.iter = 0

    #MaxAgents
    self.max_agents = max_agents
    self.n_agents = 0

    self.vehicles = []
    self.lights = []

    # Create Walls
    for x in range(width):
      for y in range(height):
        wall = Wall(x, y)
        self.grid.place_agent(wall, (x, y))

    # Create Road
    for road in road_list:
      start, end = road
      calcX = end[0] - start[0]
      calcY = end[1] - start[1]
      goes = ''
      cond = None

      if not calcX == 0:
        if calcX > 0:
          goes = 'R'
          cond = 0
        else:
          goes = 'L'
          cond = 1
      elif not calcY == 0:
        if calcY > 0:
          goes = 'U'
          cond = 0
        else:
          goes = 'D'
          cond = 1

      x = start[0]
      y = start[1]
      while x != end[0]:
        cell = self.grid.get_cell_list_contents((x, y), True)

        if any(isinstance(elem, Wall) for elem in cell):
          self.grid.remove_agent(cell[0])

        if any(isinstance(elem, Road) for elem in cell):
          cell[0].dir.append(goes)
        else:
          r = Road(0, self, x, y)
          r.dir.append(goes)
          self.grid.place_agent(r, (x, y))

        if cond == 0:
          x += 1
        else:
          x -= 1

      while y != end[1]:
        cell = self.grid.get_cell_list_contents((x, y), True)

        if any(isinstance(elem, Wall) for elem in cell):
          self.grid.remove_agent(cell[0])

        if any(isinstance(elem, Road) for elem in cell):
          cell[0].dir.append(goes)
        else:
          r = Road(1, self, x, y)
          r.dir.append(goes)
          self.grid.place_agent(r, (x, y))

        if cond == 0:
          y += 1
        else:
          y -= 1
    
    self.grid.get_cell_list_contents((10, 0), True)[0].dir[0] = 'R'
    self.grid.get_cell_list_contents((19, 10), True)[0].dir[0] = 'U'
    self.grid.get_cell_list_contents((0, 11), True)[0].dir[0] = 'D'
    self.grid.get_cell_list_contents((11, 20), True)[0].dir[0] = 'L'

    # Create Lights
    self.traff = (9, 10)
    self.traffic_light = TrafficLight(0, self, self.traff, True)
    self.grid.place_agent(self.traffic_light, self.traff)

    self.traff2 = (10, 12)
    self.traffic_light2 = TrafficLight(1, self, self.traff2, False)
    self.grid.place_agent(self.traffic_light2, self.traff2)

    self.traffic_light.lights.append(self.traffic_light2) # connect Lights
    self.traffic_light2.lights.append(self.traffic_light) # connect Lights

    self.lights.append(self.traffic_light)
    self.lights.append(self.traffic_light2)

    # Create Vehicles
    pos = [(1,10), (3,10), (10,19)]
    for i in range(3):
      self.vehicle_pos = pos[i]
      self.vehicle = Vehicles(i, self, self.vehicle_pos)
      self.grid.place_agent(self.vehicle, self.vehicle_pos)
      self.vehicles.append(self.vehicle)

    # Create Parking Lot 
    self.park_lot_pos = (12, 3)
    self.park_lot = ParkingLot(self.park_lot_pos, 6)
    self.grid.place_agent(self.park_lot, self.park_lot_pos)

    self.park_lot_pos = (16, 12)
    self.park_lot2 = ParkingLot(self.park_lot_pos, 6)
    self.grid.place_agent(self.park_lot2, self.park_lot_pos)
    
    # Run
    self.running = True

  def generate_random_cars(self):
    pos = [(0, 10), (19, 11), (10, 20), (11, 0)]

    if self.iter == 5:
      # Si hay un agente abajo de el, no poner
      for i in range(self.n_agents_per_iter):
        if self.n_agents == self.max_agents:
          print('limite')
          continue
        else:
          cell = self.grid.get_cell_list_contents(pos[i], True)
          if not any(isinstance(elem, Vehicles) for elem in cell):
            self.vehicle = Vehicles(i, self, pos[i])
            self.grid.place_agent(self.vehicle, pos[i])
            self.vehicles.append(self.vehicle)
            self.n_agents += 1
            print('add')
      self.iter = 0
    else:
      self.iter += 1
  
  def step(self):
    self.generate_random_cars()
    ps = []
    for vehicle in self.vehicles:
      # checar si se sale del tablero
      
      vehicle.move()

      xy = vehicle.pos
      p = [xy[0],xy[1],0]
      ps.append(p)

    for light in self.lights:
      light.check()

    self.schedule.step()
    return ps

  def run_model(self, n):
    for i in range(n):
      self.step()

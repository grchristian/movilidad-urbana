from mesa import Agent
import random
  
# Visual Node
class VisualNode(Agent):
  def __init__(self, x, y):
    super().__init__(x, y)

# Visual Board
class Road(Agent):
  def __init__(self, unique_id, model, x, y):
    super().__init__(unique_id, model)
    # direccion aqui
    self.dir = [] # U D L R

# Visual Board
class Wall(Agent):
  def __init__(self, x, y):
    super().__init__(x, y)

# ESTACIONAMIENTO
class ParkingLot(Agent):
  def __init__(self, pos, capacity=10):
    super().__init__(pos, capacity)
    self.pos = pos
    self.capacity = capacity
    #self.used = 1
    self.used = random.randint(0,2)

  def hasCapacity(self):
    if self.capacity > self.used:
      return True
    else:
      return False

  def park(self):
    self.used += 1

    if self.used == self.capacity:
      return 'Last Car'

# LUCES DE TRAFICO
class TrafficLight(Agent):
  def __init__(self, u_id, model, pos, horiz=True):

    super().__init__(u_id, model)
    self.pos = pos
    self.horiz = horiz
    self.lights = []
    self.current_cycle = 1
    self.counter = 0

  def status(self):
    if self.lights[0].current_cycle == 0:
      self.current_cycle = 1
    else:
      self.current_cycle = 0

  def check(self):
    # Checamos status de las luces paralelas
    self.status()

    # Checamos direccion de calle para saber donde checar a los agentes
    dirRoad = self.model.grid.get_cell_list_contents((self.pos[0], self.pos[1]), True)[0].dir

    if 'D' in dirRoad:
      self.x = 0
      self.y = 1
    elif 'R' in dirRoad:
      self.x = -1
      self.y = 0
    elif 'U' in dirRoad:
      self.x = 0
      self.y = -1
    elif 'L' in dirRoad:
      self.x = 1
      self.y = 0
             
    vehicle_cell = self.model.grid.get_cell_list_contents((self.pos[0] + self.x, self.pos[1] + self.y), True)

    if self.counter == 3:
      self.current_cycle = 0
      self.counter = 0
      self.lights[0].current_cycle = 1

    # Cambiar status del coche con el semaforo
    for vehicle in vehicle_cell:
      if type(vehicle) == Vehicles:
        if self.current_cycle == 1:
          vehicle.canMove = True
        else:
          vehicle.canMove = False

        self.counter = 0

      else:
        self.counter += 1

# VEHICULOS
class Vehicles(Agent):
  def __init__(self, u_id, model, pos):
    super().__init__(u_id, model)
    self.original_pos = pos
    self.pos = self.original_pos
    self.x = self.pos[0]
    self.y = self.pos[1]
    self.canMove = True # Para semaforo
    self.isParked = False

  def step(self):
    self.move()

  def move(self):
    # Cada que se mueva, checar si hay algun estacionamiento alrededor con capacidad
    if not self.isParked:
      self.checkNearby()

    # Checar contenidos de la celda en la que esta el agente
    cell = self.model.grid.get_cell_list_contents((self.x, self.y), True)[0].dir

    # Si la celda en la que esta el agente tiene mas de una direccion, elegir una dir random a ir
    if len(cell) > 1 and self.canMove and not self.isParked:

      pick = cell[random.randint(0, len(cell)-1)]
      
      if pick == 'R':
        self.x += 1

      elif pick == 'D':
        self.y -= 1

      elif pick == 'L':
        self.x -= 1

      elif pick == 'U':
        self.y += 1
      
      # Ir a direccion
      if not self.isParked:
        self.model.grid.move_agent(self, (self.x, self.y))

    # Else si tiene una dir, checar a cual ir y ver si esta disponible el lugar para ir
    else:
      self.checkFront()
    
  def checkFront(self):
    cell = self.model.grid.get_cell_list_contents((self.x, self.y), True)[0].dir

    if 'R' in cell and self.canMove and not self.isParked:
      if self.model.grid.out_of_bounds((self.x + 1, self.y)):
        self.x = self.original_pos[0]
        self.y = self.original_pos[1]
        self.model.grid.move_agent(self, (self.x, self.y))
        return

      if not (any(isinstance(x, Vehicles) for x in self.model.grid.get_cell_list_contents((self.x + 1, self.y), True))):
        self.x += 1

    elif 'D' in cell and self.canMove and not self.isParked:
      if self.model.grid.out_of_bounds((self.x + 1, self.y)):
        self.x = self.original_pos[0]
        self.y = self.original_pos[1]
        self.model.grid.move_agent(self, (self.x, self.y))
        return

      if not (any(isinstance(x, Vehicles) for x in self.model.grid.get_cell_list_contents((self.x, self.y - 1), True))):
        self.y -= 1

    elif 'L' in cell and self.canMove and not self.isParked:
      if self.model.grid.out_of_bounds((self.x + 1, self.y)):
        self.x = self.original_pos[0]
        self.y = self.original_pos[1]
        self.model.grid.move_agent(self, (self.x, self.y))
        return

      if not (any(isinstance(x, Vehicles) for x in self.model.grid.get_cell_list_contents((self.x - 1, self.y), True))):
        self.x -= 1

    elif 'U' in cell and self.canMove and not self.isParked:
      if self.model.grid.out_of_bounds((self.x + 1, self.y)):
        self.x = self.original_pos[0]
        self.y = self.original_pos[1]
        self.model.grid.move_agent(self, (self.x, self.y))
        return

      if not (any(isinstance(x, Vehicles) for x in self.model.grid.get_cell_list_contents((self.x, self.y + 1), True))):
        self.y += 1
    
    if not self.isParked:
      self.model.grid.move_agent(self, (self.x, self.y))

  def checkNearby(self):
    check = self.model.grid.get_neighbors((self.x, self.y), 0,1, True)

    for park_lot in check:
      if type(park_lot) == ParkingLot:
        if park_lot.hasCapacity():
          self.model.grid.move_agent(self, park_lot.pos)
          self.isParked = True
          park_lot.park()
          
#Lucía Barrenechea
#15 de noviembre del 2023
from mesa import Agent
import networkx as nx
import matplotlib.pyplot as plt
import math

class RandomAgent(Agent):
    """
    Agent that moves randomly.
    Attributes:
        unique_id: Agent's ID 
        direction: Randomly chosen direction chosen from one of eight directions
    """
    def __init__(self, unique_id, model):
        """
        Creates a new random agent.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
        """
        super().__init__(unique_id, model)
        self.direction = 4
        self.steps_taken = 0
        self.scanned_positions = []
        self.battery = 99
        self.navigatable = []
        self.allMoves = []
        #adds chargin stations to allMoves
        #self.allMoves+=self.model.charging_station
        self.model.deletedCount=0
        self.last=[]
        self.check=1
        self.chargingLocation=[]
        self.clean=0
        self.deleted=0
        #self.model.charging_station=[]

    def get_deleted_count(self):
        return self.deleted

    def move(self):
        """ 
        Determines if the agent can move in the direction that was chosen
        """
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True, # Boolean for whether to use Moore neighborhood (including diagonals) or Von Neumann (only up/down/left/right).
            include_center=True) 
        #getcelllistcontents, getneighborhood
        # Checks which grid cells are empty
        freeSpaces = list(map(self.model.grid.is_cell_empty, possible_steps))
         # Checks which grid cells are dirty.
        dirtySpaces= list(map(self.dirtyspaces, possible_steps))
        #Checks which grid cells have not been visited.
        chargeSpaces = list(map(self.chargingstation, possible_steps))
        #Checks which grid cells have no agent.
        agentSpaces = list(map(self.agentcheck, possible_steps))
        #Checks which grid cells have not been visited.
        notVisited = list(map(self.notVisited, possible_steps))

        #Stores list of possible moves
        next_moves = [p for p,f in zip(possible_steps, freeSpaces) if f == True]
        next_movesd = [s for s,d in zip(possible_steps, dirtySpaces) if d == True]
        next_movesc = [s for s,c in zip(possible_steps, chargeSpaces) if c == True]
        next_movesR = [s for s,r in zip(possible_steps, agentSpaces) if r == True]
        next_movesv = [s for s,v in zip(possible_steps, notVisited) if v == True]
        

        if len(next_movesc)>0: #If a charging station is found
            for x in next_movesc:
                if x not in self.chargingLocation:
                    self.chargingLocation.append(x)
            for x in self.chargingLocation:
                print("locations: ",x)
        if len(next_movesd) > 0: #If a dirty space is found
            available_moves = [move for move in next_movesd if move not in next_movesR]
            if available_moves:
                next_move = self.random.choice(available_moves)
                print(next_move)
                if next_move not in self.allMoves:
                    self.allMoves.append(next_move)
                self.model.grid.move_agent(self, next_move)
                self.steps_taken += 1
                self.model.deleted_count+=1
                return True
        else: #If an empty and not visited space is found
            common_moves = [value for value in next_movesv if value in next_moves]#stores values that are empty and unvistited.
            if len(common_moves)>0:
                next_move = self.random.choice(common_moves)
                print(next_move)
                # self.scanGrid(possible_steps)
                if next_move not in self.allMoves:
                    self.allMoves.append(next_move)
                self.model.grid.move_agent(self, next_move)
                self.steps_taken+=1
            else: #if a empty space is ofund
                next_move = self.random.choice(next_moves)
                self.allMoves.append(next_move)
                print("next move",next_move)
                if next_move not in self.allMoves:
                    self.allMoves.append(next_move)
                self.model.grid.move_agent(self, next_move)
                self.steps_taken+=1
   
   #Uses a library to implement aStar from networkx
    def a_star_search(self, graph, start, goal):
        path = nx.astar_path(graph, start, goal)
        print("path",path)
        return path
    
    #Used to calculate the closest charging station
    def calculate_distance(self, coord1, coord2):
        x1, y1 = coord1
        x2, y2 = coord2
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    #Used to find the closest charging station
    def find_nearest_charging_station(self, current_position, charging_stations):
        nearest_station = None
        min_distance = float(10000)  # Initialize with a large value

        for station in charging_stations:
            distance = self.calculate_distance(current_position, station)
            if distance < min_distance:
                min_distance = distance
                nearest_station = station
        return nearest_station
    
    #Used to get to a charging station
    def backHome(self):
        print("In back home")
        G = nx.Graph()
        coordinates=self.allMoves+self.chargingLocation #add coordinates of charging station to been
        G.add_nodes_from(coordinates)
        for i, coord in enumerate(coordinates):
            if i==0:
                G.add_edge(coord, (1,1))
            x, y = coord
            neighbors = [(x + 1, y), (x - 1, y), (x + 1, y+1), (x - 1, y+1),(x, y+1), (x - 1, y-1),(x, y-1), (x + 1, y-1)]
    # Add edges to neighbors if they exist in the coordinates list
            for neighbor in neighbors:
                if neighbor in coordinates:
                    print("edge",coord,neighbor)
                    G.add_edge(coord, neighbor)      
        self.start_node = self.pos
        self.last.append(self.start_node)
       
        goal_node = self.find_nearest_charging_station(self.start_node, self.chargingLocation)
        print(goal_node)
        print("GRAPH")
        for x in G:
            print(x)
        path = self.a_star_search(G, self.start_node, goal_node)
        print(path)
        count=1
        if count < len(path):
            print("Moving to:", path[count])
            self.steps_taken+=1
            self.model.grid.move_agent(self, path[count])
            self.battery -= 1
            count += 1
        else:
            print("BATTERY FULL")
            self.steps_taken+=1
            self.battery=100
        print("END")

    #Used to continue cleaning from the last psition.
    def continueCleaning(self):
        print("Back Cleaning")
        G = nx.Graph()
        coordinates=self.allMoves+self.chargingLocation #add coordinates of charging station to been
        G.add_nodes_from(coordinates)
        #G.add_edges_from([(coordinates[i], coordinates[i + 1]) for i in range(len(coordinates) - 1)])
        for i, coord in enumerate(coordinates):
            if i==0:
                G.add_edge(coord, (1,1))
            x, y = coord
            neighbors = [(x + 1, y), (x - 1, y), (x + 1, y+1), (x - 1, y+1),(x, y+1), (x - 1, y-1),(x, y-1), (x + 1, y-1)]
    # Add edges to neighbors if they exist in the coordinates list
            for neighbor in neighbors:
                if neighbor in coordinates:
                    print("edge",coord,neighbor)
                    G.add_edge(coord, neighbor)
        #G.add_edge(path[-2], goal_node)        
        goal_node = self.last[0]
        print("goal node is:",goal_node)
        self.start_node = self.pos
        path = self.a_star_search(G, self.start_node, goal_node)
        print(path)
        count=1
        if count < len(path):
            print("Moving to:", path[count])
            self.model.grid.move_agent(self, path[count])
            self.battery -= 1
            count += 1
            self.steps_taken+=1
        # for x in path:
        #     self.model.grid.move_agent(self, path[count])
        #     self.battery-=1
        #     print("battery",self.battery)
        #     count+=1
        #self.check=1
        #self.battery=100
        
    def Navigate(self, pos, contents):
        print("content check", contents)
        if contents == [] and pos not in self.navigatable:
            # Add to the navigatable list
            #print("navigatable", pos)
            self.navigatable.append(pos)
            return True
            #print("Navigatable:", self.navigatable)
        # print("TEST")
        #Acomoda la lista usando el orden de las posiciones.
            #self.scanned_positions = sorted(self.scanned_positions + [positions_and_agents], key=lambda x: (x[0][0], x[0][1]))
        # for x in self.navigatable:
        #     print(x,"\n")
        # print("ETEST")
        return False
    #If a trash is found battery -1
    def cleanTrash(self):
        contents = self.model.grid.get_cell_list_contents([self.pos])
        for agent in contents:
            if isinstance(agent, DirtyAgent):
                print("Checking cleaning",agent)
                self.model.grid.remove_agent(agent)
                print("Checking cleaning 2",agent)
                self.model.deletedCount+=1
                self.battery-=1
                self.deleted+=1
    #Used to determine if a dirty space.
    def dirtyspaces(self, pos):
        contents = self.model.grid.get_cell_list_contents(pos)
        for agent in contents:
            if not(isinstance(agent,RandomAgent)):
                if isinstance(agent, DirtyAgent):
                    return True
            return False
    #Used to determine if a charging station.
    def chargingstation(self, pos):
        contents = self.model.grid.get_cell_list_contents(pos)
        for agent in contents:
            if not(isinstance(agent,RandomAgent)):
                if isinstance(agent, ChargingStation):
                    return True
        return False
    #Used to determine if a rumba agent.
    def agentcheck(self, pos):
        contents = self.model.grid.get_cell_list_contents(pos)
        for agent in contents:
            if isinstance(agent, RandomAgent):
                return True
        return False
    #Used to determine if not visited yet.
    def notVisited(self, pos):
        contents = self.model.grid.get_cell_list_contents(pos)
        for agent in contents:
            #print("pruba",agent)
            if pos not in self.allMoves:
                return True
        return False
    
    def step(self):
        """ 
        self_init
        agregar bateeria si queda
        Determines the new direction it will take, and then moves
        """
        if self.clean==1: #If a trash is found agent is in position
            self.cleanTrash()
            self.clean=0
        elif self.battery >= 60 and self.battery < 100 and self.check==1:
            if self.move() == True:
                self.clean=1
            print("Bateria",self.battery)
            self.battery -= 1
            self.last=[]
            print("NORMAL")
        elif self.battery >= 60 and self.battery <= 100 and self.check==0:
            self.continueCleaning()
            print("checking position" ,self.pos, self.last[0])
            if self.pos == self.last[0]:
                print("SAME")
                self.check=1
            print(" ")
            print("CLEAN")
        else:
            print("BACK HOME")
            print(self.check, self.battery)
            self.check=0
            self.backHome()
        print("Printing all moves")
        # for x in self.allMoves:
        #     print(x)
        # print("This is deleted", self.model.deleted_count)
            
class ObstacleAgent(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass  

class DirtyAgent(Agent):
    """
    Dirty agent. Just to add obstacles to the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass  

class ChargingStation(Agent):
    """
    Dirty agent. Just to add obstacles to the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass  

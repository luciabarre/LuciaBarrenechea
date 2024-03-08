from mesa import Agent
import networkx as nx
import matplotlib.pyplot as plt

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
        self.allMoves.append((1,1))
        self.last=[]
        self.check=1
        self.deleted=0
        self.clean=0
    #Used for data collector
    def get_deleted_count(self):
        """
        Returns the value of the deleted count variable.
        """
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
        notVisited = list(map(self.notVisited, possible_steps))

        next_moves = [p for p,f in zip(possible_steps, freeSpaces) if f == True]
        next_movesd = [s for s,d in zip(possible_steps, dirtySpaces) if d == True]
        next_movesv = [s for s,v in zip(possible_steps, notVisited) if v == True]
        self.scanGrid(possible_steps)
        if len(next_movesd)>0: #stores positions with trash
            next_move = self.random.choice(next_movesd)
            print(next_move)
            # self.scanGrid(possible_steps)
            if next_move not in self.allMoves:
                self.allMoves.append(next_move)
            self.model.grid.move_agent(self, next_move)
            self.steps_taken+=1
            return True
        else:
            common_moves = [value for value in next_movesv if value in next_moves]#stores values that are empty and unvistited.
            if len(common_moves)>0:
                next_move = self.random.choice(common_moves)
                print(next_move)
                # self.scanGrid(possible_steps)
                if next_move not in self.allMoves:
                    self.allMoves.append(next_move)
                self.model.grid.move_agent(self, next_move)
                self.steps_taken+=1
            else:
                next_move = self.random.choice(next_moves) #stores available positions (empty)
                self.allMoves.append(next_move)
                print("next move",next_move)
                if next_move not in self.allMoves:
                    self.allMoves.append(next_move)
                self.model.grid.move_agent(self, next_move)
                #self.scanGrid(self.pos)
                self.steps_taken+=1
                #print("no basura")
        print("ALL MOVES")
        for x in self.allMoves:
            print(x)
   
   #Algoritmo A* para encontrar el camino mas corto. libreria networkx.
    def a_star_search(self, graph, start, goal):
        path = nx.astar_path(graph, start, goal)
        print("path",path)
        return path
    
    #Regresa a la ruma a la base
    def backHome(self):
        print("In back home")
        G = nx.Graph()
        coordinates=self.allMoves
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
        self.start_node = self.pos
        self.last.append(self.start_node)
        goal_node = (1, 1)
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

    #Regresa a la rumba a la ultima posición antes de regresar a cargar pila
    def continueCleaning(self):
        print("Back Cleaning")
        G = nx.Graph()
        coordinates=self.allMoves
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
        goal_node = self.last[0] #Ultimo registrado antes de regresar a cargar pila
        print("goal node is:",goal_node)
        self.start_node = self.pos
        path = self.a_star_search(G, self.start_node, goal_node)#Encontrar el camino mas corto al objetivo.
        print(path)
        count=1
        if count < len(path):
            print("Moving to:", path[count])
            self.model.grid.move_agent(self, path[count])
            self.battery -= 1
            count += 1
            self.steps_taken+=1
    #Guarda las posiciones de los agentes vecinos que no han sido visitados.  
    def notVisited(self, pos):
        contents = self.model.grid.get_cell_list_contents(pos)
        for agent in contents:
            #print("pruba",agent)
            if pos not in self.allMoves:
                return True
        return False
    #Guarda las posiciones escaneadas de vecinos para mappear el grid.
    def scanGrid(self, pos):
        for p in pos:
            contents = self.model.grid.get_cell_list_contents(p)
            positions_and_agents = (p, contents)
            #self.Navigate(p, contents)
            for i, (stored_pos, _) in enumerate(self.scanned_positions):
                if p == stored_pos:
                    #print("Already scanned:", p)
                    # Replace the existing element with the new element
                    self.scanned_positions[i] = positions_and_agents
                    break
            else:
                self.scanned_positions.append(positions_and_agents)
                #print("Newly scanned:", p)
            #Acomoda la lista usando el orden de las posiciones.
            #self.scanned_positions = sorted(self.scanned_positions + [positions_and_agents], key=lambda x: (x[0][0], x[0][1]))
        # for x in self.scanned_positions:
        #     print(x,"\n")
    
    # def Navigate(self, pos, contents):
    #     print("content check", contents)
    #     if contents == [] and pos not in self.navigatable:
    #         # Add to the navigatable list
    #         #print("navigatable", pos)
    #         self.navigatable.append(pos)
    #         return True
    #         #print("Navigatable:", self.navigatable)
    #     # print("TEST")
    #     #Acomoda la lista usando el orden de las posiciones.
    #         #self.scanned_positions = sorted(self.scanned_positions + [positions_and_agents], key=lambda x: (x[0][0], x[0][1]))
    #     # for x in self.navigatable:
    #     #     print(x,"\n")
    #     # print("ETEST")
    #     return False
    
    #If a trash is found battery -1
    def cleanTrash(self):
        contents = self.model.grid.get_cell_list_contents([self.pos])
        for agent in contents:
            if isinstance(agent, DirtyAgent):
                self.model.grid.remove_agent(agent)
                self.battery-=1
                self.deleted+=1
                
    #Guarda las posiciones de los agentes vecinos que son basura.
    def dirtyspaces(self, pos):
        contents = self.model.grid.get_cell_list_contents(pos)
        for agent in contents:
            if isinstance(agent, DirtyAgent):
                return True
        return False
    
    #Se realiza en cada step    
    def step(self):
        """ 
        self_init
        agregar bateeria si queda
        Determines the new direction it will take, and then moves
        """
        
        if self.clean==1: #Si la rumba esta sobre un agente sucio
            self.cleanTrash()
            self.clean=0
        elif self.battery >= 60 and self.battery < 100 and self.check==1:#Si la rumba tiene pila
            if self.move() == True:
                self.clean=1
            self.cleanTrash()
            print("Bateria",self.battery)
            self.battery -= 1
            self.last=[]
            print("NORMAL")
        elif self.battery >= 60 and self.battery <= 100 and self.check==0:#Si la rumba esta regresando despues de cargar pila
            self.continueCleaning()
            print("checking position" ,self.pos, self.last[0])
            if self.pos == self.last[0]:
                print("SAME")
                self.check=1
            print(" ")
            print("CLEAN")
        else:#Si la rumaba no tiene pila
            print("BACK HOME")
            print(self.check, self.battery)
            self.check=0
            self.backHome()
            
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

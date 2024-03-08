#Lucía Barrenechea
#16 de noviembre del 2023
from mesa import Model, agent
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa import DataCollector
from agent import RandomAgent, ObstacleAgent, DirtyAgent, ChargingStation

class RandomModel(Model):
    """ 
    Creates a new model with random agents.
    Args:
        N: Number of agents in the simulation
        height, width: The size of the grid to model
    """
    def __init__(self, N, width, height):
        self.num_agents = N
        # Multigrid is a special type of grid where each cell can contain multiple agents.
        self.grid = MultiGrid(20,20,torus = False) 
        self.percentage = 0
        # RandomActivation is a scheduler that activates each agent once per step, in random order.
        self.schedule = RandomActivation(self)
        self.running = True
        self.allmoves=[]
        self.dirty=[]
        self.charging_station=[]
        self.deleted_count = 0
        self.datacollector = DataCollector( 
        agent_reporters={
        "Steps": lambda a: a.steps_taken if isinstance(a, RandomAgent) else 0}
        ,
        model_reporters={
                "Deleted_Percentage": lambda model: model.percentage,
                "Remaining_Percentage": lambda model: 100 - model.percentage,
            }
        
        )

        # Creates the border of the grid
        border = [(x,y) for y in range(height) for x in range(width) if y in [0, height-1] or x in [0, width - 1]]

        def get_all_moves(self):
            return self.allMoves

        def add_to_all_moves(self, move):
            self.allMoves.append(move)
        # Add obstacles to the grid
        for pos in border:
            obs = ObstacleAgent(pos, self)
            self.grid.place_agent(obs, pos)

        # Function to generate random positions
        pos_gen = lambda w, h: (self.random.randrange(w), self.random.randrange(h))
        
    
        #add agent to a random empty cell
        for i in range(self.num_agents):
            a = RandomAgent(i+1000, self) 
            self.schedule.add(a)

            pos = pos_gen(self.grid.width, self.grid.height)
            while (not self.grid.is_cell_empty(pos)):
                pos = pos_gen(self.grid.width, self.grid.height)
            self.charging_station.append(pos)
            self.grid.place_agent(a, pos)
            
        #add charging starion to a random pos in charging_station list
        for i in range(self.num_agents):
            a = ChargingStation(i+1100, self) 
            self.schedule.add(a)
            self.grid.place_agent(a, self.charging_station[i])
        
        #add obstacle agent to a random empty cell
        for i in range(self.num_agents*2):
    
            a = ObstacleAgent(i+1500, self) 
            self.schedule.add(a)

            pos = pos_gen(self.grid.width, self.grid.height)
            while (not self.grid.is_cell_empty(pos)):
                pos = pos_gen(self.grid.width, self.grid.height)

            self.grid.place_agent(a, pos)
        
        #add dirty agent to a random empty cell.
        for i in range(self.num_agents*4):
        
            a = DirtyAgent(i+1600, self) 
            self.schedule.add(a)

            pos = pos_gen(self.grid.width, self.grid.height)
            while (not self.grid.is_cell_empty(pos)):
                pos = pos_gen(self.grid.width, self.grid.height)
            self.dirty.append(pos)
            self.grid.place_agent(a, pos)
        
        self.datacollector.collect(self)
    
    #Calculate the percentage of deleted agents.
    def calcpercentage(self):
        self.percentage = (self.deleted_count/(self.num_agents*4))*100
        
    
    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()
        self.calcpercentage()
        self.datacollector.collect(self)
    
        if self.deleted_count == self.num_agents*4 :
            self.running = False
            print("Simulation Ended")
        print("Deleted count:", self.deleted_count)
        
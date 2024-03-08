#Lucía Barrenechea
# 16 de noviembre del 2023
from mesa import Model, agent
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa import DataCollector
from agent import RandomAgent, ObstacleAgent, DirtyAgent

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
        self.grid = MultiGrid(width,height,torus = False) 

        # RandomActivation is a scheduler that activates each agent once per step, in random order.
        self.schedule = RandomActivation(self)
        self.percentage = 0
        self.running = True
        self.deleted_count = 0  
        self.dirty=[]
        # DataCollector collects data from agents and from the model at each step of the simulation.    
        self.datacollector = DataCollector( 
        agent_reporters={"Steps": lambda a: a.steps_taken if isinstance(a, RandomAgent) else 0},
        model_reporters={
                "Deleted_Percentage": lambda model: model.percentage,
                "Remaining_Percentage": lambda model: 100 - model.percentage,
            })

        # Creates the border of the grid
        border = [(x,y) for y in range(height) for x in range(width) if y in [0, height-1] or x in [0, width - 1]]

        # Add obstacles to the grid
        for pos in border:
            obs = ObstacleAgent(pos, self)
            self.grid.place_agent(obs, pos)

        # Function to generate random positions
        pos_gen = lambda w, h: (self.random.randrange(w), self.random.randrange(h))
        
    
        a = RandomAgent(1000, self) 
        self.schedule.add(a)

        self.grid.place_agent(a, (1,1))
        #add obstacle agent to a random empty cell
        for i in range(self.num_agents*2):
    
            a = ObstacleAgent(i+1500, self) 
            self.schedule.add(a)

            pos = pos_gen(self.grid.width, self.grid.height)
            while (not self.grid.is_cell_empty(pos)):
                pos = pos_gen(self.grid.width, self.grid.height)

            self.grid.place_agent(a, pos)
        
        #add dirty agent to a random empty cell.
        for i in range(self.num_agents*2):
        
            a = DirtyAgent(i+1600, self) 
            self.schedule.add(a)

            pos = pos_gen(self.grid.width, self.grid.height)
            while (not self.grid.is_cell_empty(pos)):
                pos = pos_gen(self.grid.width, self.grid.height)
            self.dirty.append(pos)
            self.grid.place_agent(a, pos)
            
        
        self.datacollector.collect(self)
    
    #Calcula el porcentage de agentes eliminados
    def calcpercentage(self):
        self.percentage = (self.deleted_count/(self.num_agents*4))*100
        
    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()
        self.deleted_count = self.schedule.agents[0].get_deleted_count()
        self.calcpercentage()
        self.datacollector.collect(self)
        if self.deleted_count == self.num_agents*2 :
            self.running = False
        print("Deleted count:", self.deleted_count)
        
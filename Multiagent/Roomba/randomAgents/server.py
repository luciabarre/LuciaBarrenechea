from model import RandomModel, ObstacleAgent, DirtyAgent
from mesa.visualization import CanvasGrid, BarChartModule,  PieChartModule
from mesa.visualization import ModularServer

def agent_portrayal(agent):
    if agent is None: return
    
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "Color": "red",
                 "r": 0.5}

    if (isinstance(agent, ObstacleAgent)):
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.2
    
    if (isinstance(agent, DirtyAgent)):
        portrayal["Color"] = "green"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.2

    return portrayal

model_params = {"N":5, "width":10, "height":10}

grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)

bar_chart = BarChartModule(
    [{"Label":"Steps", "Color":"#AA0000"}], 
    scope="agent", sorting="ascending", sort_by="Steps")
pieChart_deleted_count = PieChartModule(
    [{"Label": "Deleted_Percentage", "Color": "#00AA00"}
     ,{"Label": "Remaining_Percentage", "Color": "#AA0000"}])
#model.py: class RandomModel(Model):

server = ModularServer(RandomModel, [grid, bar_chart, pieChart_deleted_count], "Random Agents", model_params)
                       
server.port = 8521 # The default
server.launch()
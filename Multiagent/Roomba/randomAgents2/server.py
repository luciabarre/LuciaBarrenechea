#Lucia Barrenechea
#16 de noviembre del 2023
from model import RandomModel, ObstacleAgent, DirtyAgent, ChargingStation
from mesa.visualization import CanvasGrid, BarChartModule, PieChartModule
from mesa.visualization import ModularServer

def agent_portrayal(agent):
    if agent is None: return
    
    portrayal = {"Shape": "circle",
                 "Filled": "false",
                 "Layer": 1,
                 "Color": "red",
                 "r": 0.5}

    if (isinstance(agent, ObstacleAgent)):
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.8
    
    if (isinstance(agent, DirtyAgent)):
        portrayal["Color"] = "green"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.5
    if (isinstance(agent, ChargingStation)):
        portrayal["Color"] = "orange"
        portrayal["Layer"] = 0
        portrayal["r"] = 0.4

    return portrayal

model_params = {"N":4, "width":20, "height":20}

grid = CanvasGrid(agent_portrayal, 20, 20, 500, 500)

bar_chart = BarChartModule(
    [{"Label":"Steps", "Color":"#AA0000"}], 
    scope="agent", sorting="ascending", sort_by="Steps", canvas_width=500)

pieChart_deleted_count = PieChartModule(
    [{"Label": "Deleted_Percentage", "Color": "#00AA00"}
     ,{"Label": "Remaining_Percentage", "Color": "#AA0000"}])

#Used to viualize in the server.
server = ModularServer(RandomModel, [grid, pieChart_deleted_count, bar_chart], "Random Agents", model_params)
                       
server.port = 8521 # The default
server.launch()
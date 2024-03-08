from mesa import Agent

class TreeCell(Agent):
    """
        A tree cell.
        
        Attributes:
            x, y: Grid coordinates
            condition: Can be "Fine" or "Burned Out"
            unique_id: (x,y) tuple.

            unique_id isn't strictly necessary here, but it's good practice to give one to each agent anyway.
    """

    def __init__(self, pos, model):
        """
        Create a new tree.

        Args:
            pos: The tree's coordinates on the grid.
            model: standard model reference for agent.
        """
        super().__init__(pos, model)
        self.pos = pos
        self.condition = "Fine"
        self._next_condition = None

    #Step defines how the trees will react.
    def step(self):
        """
        If the tree is on fire, spread it to fine trees nearby.
        """
        conditionsAlive = ["000","010","101","111"]
        conditionsDead = ["001","011","100","110"]
        check="000"
        for neighbor in self.model.grid.iter_neighbors(self.pos, True):
            x, y = neighbor.pos
            selfx, selfy = self.pos
            dx=selfx-x
            dy=selfy-y
            if selfy==49: #Checks the top row.
                print("hello", selfy, y)
                print(selfx,x,selfy,y)
                print(neighbor.condition)
                #self._next_condition = "Burned Out"
                if dx==0 and dy==49 and neighbor.condition == "Burned Out":
                    print("Vecino abajooo", y, selfy, x, selfx)
                    check = check[:1] + "1" + check[2:]
                elif dx==-1 and dy==49 and neighbor.condition == "Burned Out":
                    print("Vecino Izquierda abajo")
                    check = "1" + check[1:]
                elif dx==1 and dy==49  and neighbor.condition == "Burned Out":
                    print("Vecino derecha abajo")
                    check = check[:2] + "1"
            else:
                if (selfx, selfy + 1) == (x, y) and neighbor.condition == "Burned Out":
                    print("Vecino Arriba")
                    check = check[:1] + "1" + check[2:]
                elif (selfx +1, selfy + 1) == (x, y) and neighbor.condition == "Burned Out":
                    print("Vecino Izquierda")
                    check = "1" + check[1:]
                elif (selfx -1, selfy + 1) == (x, y) and neighbor.condition == "Burned Out":
                    print("Vecino derecha")
                    check = check[:2] + "1"
                #Checks when cell in in the sides
                elif dx==-49 and dy==-1  and neighbor.condition == "Burned Out":
                    print("Vecino derecha")
                    check = check[:2] + "1"
                elif dx==49 and dy==-1  and neighbor.condition == "Burned Out":
                    print("Vecino Izquierda")
                    check = "1" + check[1:]
                #Checks when cell is in the corners.
                elif dx==-49 and dy==49  and neighbor.condition == "Burned Out":
                    print("Vecino derecha")
                    check = check[:2] + "1"
                elif dx==49 and dy==49  and neighbor.condition == "Burned Out":
                    print("Vecino Izquierda")
                    check = "1" + check[1:]
        #Used to check the possible conditions  
            if check in conditionsAlive:
                print(check)
                self._next_condition = "Fine"
            elif check in conditionsDead:
                self._next_condition = "Burned Out"
                
    def advance(self):
        """
        Advance the model by one step.
        """
        if self._next_condition is not None:
            self.condition = self._next_condition
        
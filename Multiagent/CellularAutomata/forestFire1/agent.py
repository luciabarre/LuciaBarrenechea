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
        conditions = ["001","011","100","110"]
        check="000"
        if self.condition=="Fine":
            for neighbor in self.model.grid.iter_neighbors(self.pos, True):
                x, y = neighbor.pos
                selfx, selfy = self.pos
                if (selfx, selfy + 1) == (x, y) and neighbor.condition == "Burned Out":
                    print("Vecino Arriba")
                    check = check[:1] + "1" + check[2:]
                elif (selfx +1, selfy + 1) == (x, y) and neighbor.condition == "Burned Out":
                    print("Vecino Izquierda")
                    check = "1" + check[1:]
                    print("izqui", check)
                elif (selfx -1, selfy + 1) == (x, y) and neighbor.condition == "Burned Out":
                    print("Vecino derecha")
                    check = check[:2] + "1"
                    print("derecha", check)
                if check in conditions:
                    print("In condition: ", check)
                    self._next_condition = "Burned Out"
                else:
                    self._next_condition = "Fine"
                    
    def advance(self):
        """
        Advance the model by one step.
        """
        if self._next_condition is not None:
            self.condition = self._next_condition
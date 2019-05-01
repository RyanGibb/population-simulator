
class Tile:
    def __init__(self):
        self.predator = None
        self.prey = None
        self.food = False

    def get_char(self):
        if self.predator != None:
            return "C"
        elif self.prey != None:
            return "H"
        elif self.food == True:
            return "."
        else:
            return " "

class Creature:
    def __init__(self, starting_health):
        self.health = starting_health
        self.display()

    def display(self):
        pass

    def __repr__(self):
        return "Creature: current health {}".format(self.health)

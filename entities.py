
class Tile:
    def __init__(self):
        self.entity = None
        self.food = False

    def get_char(self):
        if isinstance(self.entity, Predator):
            return "C"
        if isinstance(self.entity, Prey):
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
        return "Creature: health {}".format(self.health)

class Predator(Creature):
    def __init__(self, starting_health):
        Creature.__init__(self, starting_health)

class Prey(Creature):
    def __init__(self, starting_health):
        Creature.__init__(self, starting_health)


import sys
import os
import random
import time
from entities import *


stop = False
wait_secs = 0.1

# start_prey_per_tile = 0.05
# start_predators_per_tile = 0.005
# start_food_per_tile = 0.5
# growth_per_tile = 0.005
# atttrition = 1
# eat_food_health = 10
# eat_prey_health_modifier = 0.4

start_prey_per_tile = 0.05
start_predators_per_tile = 0.005
start_food_per_tile = 0.5
growth_per_tile = 0.003
atttrition = 1
eat_food_health = 10
eat_prey_health_modifier = 0.6

# start_prey_per_tile = 0.0005
# start_predators_per_tile = 0
# start_food_per_tile = 0.5
# growth_per_tile = 0
# atttrition = 0
# eat_food_health = 0
# eat_prey_health_modifier = 0

starting_health = 100
reproduce_health = 200

x_size = 200
y_size = 50

output_file = "output.csv"

def print_world():
    #os.system('clear')
    print("Predators: {} \tPrey: {} \tFood: {}".format(len(predators), len(prey), tiles - len(no_food)))
    print('-' * (x_size + 2))
    for y in range(y_size):
        print("|", end="")
        for x in range(x_size):
            print(world[y][x].get_char(), end="")
        print("|")
    print('-' * (x_size + 2))


def get_moves(tile_condition, x, y):
    moves = []
    for delta_x in range (-1, 2, 1):
        possible_x = (x + delta_x)
        if possible_x >= x_size or possible_x < 0:
            continue
        for delta_y in range (-1, 2, 1):
            possible_y = (y + delta_y)
            if possible_y >= y_size or possible_y < 0:
                continue
            if tile_condition(world[possible_y][possible_x]):
                assert delta_y != 0 or delta_x != 0
                moves.append((possible_x, possible_y))
    return moves

def tick():
    global prey, predators
    new_predators = []
    for x, y in predators:
        p = world[y][x].entity
        assert isinstance(p, Predator)
        p.health -= atttrition
        if p.health <= 0:
            world[y][x].entity = None
            if (x, y) in no_food:
                world[y][x].food = True
                no_food.remove((x, y))
            # predators.remove((x, y))
            continue
        # moves anywhere but onto another predator
        moves = get_moves(lambda tile: not isinstance(tile.entity, Predator), x, y)
        if len(moves) > 0:
            new_x, new_y = random.choice(moves)
            new_p = world[new_y][new_x].entity
            if isinstance(new_p, Prey):
                p.health += new_p.health * eat_prey_health_modifier
                # not strictly needed: world[y][x].entity = None
                prey.remove((new_x, new_y))
            if p.health > reproduce_health:
                world[new_y][new_x].entity = Predator(p.health / 2)
                p.health = p.health / 2
                new_predators.append((x, y))
            else:
                world[y][x].entity = None
                world[new_y][new_x].entity = p
                # predators.remove((x, y))
            new_predators.append((new_x, new_y))
    predators = new_predators

    new_prey = []
    for x, y in prey:
        p = world[y][x].entity
        assert isinstance(p, Prey)
        p.health -= atttrition
        if world[y][x].food == True:
            world[y][x].food = False
            no_food.append((x, y))
            p.health += eat_food_health
        if p.health <= 0:
            world[y][x].entity = None
            if (x, y) in no_food:
                world[y][x].food = True # 1
                no_food.remove((x, y))
            # prey.remove((x, y))
            continue
        # moves anywhere but onto another prey OR predator
        moves = get_moves(lambda tile: tile.entity == None, x, y)
        if len(moves) > 0:
            new_x, new_y = random.choice(moves)
            if p.health > reproduce_health:
                world[new_y][new_x].entity = Prey(p.health / 2)
                p.health = p.health / 2
                new_prey.append((x, y))
            else:
                world[y][x].entity = None
                world[new_y][new_x].entity = p
                # prey.remove((x, y))
            assert x != new_x or y != new_y
            # print("x {} y {}".format(x, y))
            # print("new x {} new y {}".format(new_x, new_y))
            new_prey.append((new_x, new_y))

    prey = new_prey

    for i in range(growth):
        if len(no_food) <= 0:
            continue
        x, y = random.choice(no_food)
        world[y][x].food = True
        no_food.remove((x, y))


def run():
    print_world()
    while not stop:
        tick()
        print_world()
        time.sleep(wait_secs)


def main():
    global tiles
    global start_prey
    global start_predators
    global start_food
    global growth
    tiles = int(x_size * y_size)
    start_prey = int(tiles * start_prey_per_tile)
    start_predators = int(tiles * start_predators_per_tile)
    start_food = int(tiles * start_food_per_tile)
    growth = int(tiles * growth_per_tile)

    global world
    global predators
    global prey
    global no_food
    world = [[Tile() for x in range(x_size)] for y in range(y_size)]
    predators = [None] * start_predators
    prey = [None] * start_prey
    no_creatures = [(x, y) for x in range(x_size) for y in range(y_size)]
    no_food = [(x, y) for x in range(x_size) for y in range(y_size)]
    for i in range(start_predators):
        x, y = random.choice(no_creatures)
        world[y][x].entity = Predator(starting_health)
        predators[i] = (x, y)
        no_creatures.remove((x, y))
    for i in range(start_prey):
        x, y = random.choice(no_creatures)
        world[y][x].entity = Prey(starting_health)
        prey[i] = (x, y)
        no_creatures.remove((x, y))
    for i in range(start_food):
        x, y = random.choice(no_food)
        world[y][x].food = True
        no_food.remove((x, y))
    run()


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        start_prey = int(sys.argv[1])
    main()

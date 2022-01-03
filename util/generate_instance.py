import random
import numpy as np


def write_instance(size=None, density=None, file_loc=None):
    x_len, y_len = 0, 0
    agents_num = 0
    obstacles_num = 0

    if size == None:
        x_len = 7
        y_len = 7
        
    area = x_len * y_len

    if density == None:
        agents_num = (area) // 15
        obstacles_num = (area) // 7
        # print(obstacles_num)

    if file_loc == None:
        file_loc = '../content/instances/new_instance.txt'

    new_map = np.zeros((area,), dtype=int)
    # print(new_map)

    obstacle_loc = random.sample(range(area), obstacles_num) # a list of 'area' random locations on the map

    start_loc = []
    goal_loc = []
    for a in range(agents_num):
        aloc = None
        while aloc == None:
            loc = random.sample(range(area), 1)
            if loc[0] not in obstacle_loc and loc[0] not in start_loc:
                aloc = loc
        start_loc += aloc
        
    for a in range(agents_num):
        aloc = None
        while aloc == None:
            loc = random.sample(range(area), 1)
            if loc[0] not in obstacle_loc and loc[0] not in goal_loc:
                aloc = loc
        goal_loc += aloc

    new_map[obstacle_loc] = 1
    # print(obstacle_loc)
    new_map_2d = np.reshape(new_map, (x_len,y_len)) # create a 2D list[x][y]
    # print(new_map)
    map_dict = {
        0: ". ", # no obstacle
        1: "@ " # obstacle

    }
    new_instance = ""

    new_instance += str(y_len) + " " + str(x_len) + "\n" # size y, y of the map

    # create map
    for x in range(x_len):
        for y in range(y_len):
            cell = new_map_2d[x][y]
            new_instance += map_dict[cell]
        new_instance += "\n"

    new_instance += str(agents_num) + "\n"

    for a in range(agents_num):
        # print(start_loc[a])
        
        x1 = start_loc[a] % x_len
        y1 = start_loc[a] // y_len
        # print(str(x1) + " " + str(y1) + " ")
        new_instance += str(y1) + " " + str(x1) + " "
        x2 = goal_loc[a] % x_len
        y2 = goal_loc[a] // y_len        
        new_instance += str(y2) + " " + str(x2) + "\n"


    file = open(file_loc, "w")
    file.write(new_instance)

    file.close()
    return
    

if __name__ == '__main__':
    write_instance(file_loc="static/content/instances/new_instance.txt")

    
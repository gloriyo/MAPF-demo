#!/usr/bin/python

import os
import sys

import json

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)

print(sys.path)

from cbs_basic_all_nodes import CBSSolver as CBSSolverCT

from cbs_basic import CBSSolver as CBSSolver

# from util.cbs.icbs_cardinal_bypass import ICBS_CB_Solver # only cardinal dectection and bypass
# from util.cbs.icbs_complete import ICBS_Solver # all improvements including MA-CBS
# from util.single_agent_planner import get_sum_of_cost
from visualize_demo import Animation, Figure


import argparse
import glob
from pathlib import Path

SOLVER = "ICBS_CB"

def create_plot(instance_file, map_file):
    my_map, starts, goals = import_mapf_instance(instance_file)
    figure = Figure(my_map, starts, goals)
    # figure.show()
    figure.save(map_file)

def print_mapf_instance(my_map, starts, goals):
    print('Start locations')
    print_locations(my_map, starts)
    print('Goal locations')
    print_locations(my_map, goals)


def print_locations(my_map, locations):
    starts_map = [[-1 for _ in range(len(my_map[0]))] for _ in range(len(my_map))]
    for i in range(len(locations)):
        starts_map[locations[i][0]][locations[i][1]] = i
    to_print = ''
    for x in range(len(my_map)):
        for y in range(len(my_map[0])):
            if starts_map[x][y] >= 0:
                to_print += str(starts_map[x][y]) + ' '
            elif my_map[x][y]:
                if isinstance(my_map[x][y], str):
                    to_print += my_map[x][y] + ' '
                else:
                    to_print += '@ '

            else:
                to_print += '. '
        to_print += '\n'
    print(to_print)


def import_mapf_instance(filename):
    f = Path(filename)
    if not f.is_file():
        raise BaseException(filename + " does not exist.")
    f = open(filename, 'r')
    # first line: #rows #columns
    line = f.readline()
    rows, columns = [int(x) for x in line.split(' ')]
    rows = int(rows)
    columns = int(columns)
    # #rows lines with the map
    my_map = []
    for r in range(rows):
        line = f.readline()
        my_map.append([])
        for cell in line:
            if cell == '@':
                my_map[-1].append(True)
            elif cell == '.':
                my_map[-1].append(False)
            elif cell.strip():
                my_map[-1].append(cell.strip())
                print(cell)
    # #agents
    line = f.readline()
    num_agents = int(line)
    # #agents lines with the start/goal positions
    starts = []
    goals = []
    for a in range(num_agents):
        line = f.readline()
        sx, sy, gx, gy = [int(x) for x in line.split(' ')]
        starts.append((sx, sy))
        goals.append((gx, gy))
    f.close()
    return my_map, starts, goals

def create_animation_CT(instance_file, output_fig_dir, solver, disjoint):
    my_map, starts, goals = import_mapf_instance(instance_file)
    print_mapf_instance(my_map, starts, goals) 

    if solver == "CBS":
        cbs = CBSSolverCT(my_map, starts, goals)
        solution = cbs.find_solution(disjoint)

        if solution is not None:
            # print(solution)
            gen_nodes, exp_nodes, num_nodes_gen, num_nodes_exp = [solution[i] for i in range(4)]
            if gen_nodes is None:
                raise BaseException('No nodes generated')  
        else:
            raise BaseException('No nodes generated') 
    
    for i, node in enumerate(gen_nodes):
        animation = Animation(my_map, starts, goals, node['paths'])
        # animation.save("output.mp4", 1.0)
        figure_file = output_fig_dir 
        figure_file += "_d_" if disjoint else "_s_"
        figure_file += str(node['node_i']) + ".gif"
        animation.save(figure_file, 1)

    return solution

def create_animation(instance_file, figure_file, solver=False, disjoint=True):
    if not solver:
        solver = "ICBS_CB"
    my_map, starts, goals = import_mapf_instance(instance_file)
    print_mapf_instance(my_map, starts, goals)

    if solver == "CBS":
        cbs = CBSSolver(my_map, starts, goals)
        solution = cbs.find_solution(disjoint)

        if solution is not None:
            # print(solution)
            paths, nodes_gen, nodes_exp, time = [solution[i] for i in range(4)]
            if paths is None:
                raise BaseException('No solutions')  
        else:
            raise BaseException('No solutions')

    elif solver == "ICBS_CB":
        cbs = ICBS_CB_Solver(my_map, starts, goals)
        solution = cbs.find_solution(disjoint)

        if solution is not None:
            # print(solution)
            paths, nodes_gen, nodes_exp = [solution[i] for i in range(3)]
            if paths is None:
                raise BaseException('No solutions')  
        else:
            raise BaseException('No solutions')

    elif solver == "ICBS":
        cbs = ICBS_Solver(my_map, starts, goals)
        solution = cbs.find_solution(disjoint)

        if solution is not None:
            # print(solution)
            paths, nodes_gen, nodes_exp = [solution[i] for i in range(3)]
            if paths is None:
                raise BaseException('No solutions')  
        else:
            raise BaseException('No solutions')

    animation = Animation(my_map, starts, goals, paths)
    # animation.save("output.mp4", 1.0)
    animation.save(figure_file, 1)

    return solution



if __name__ == '__main__':

    # ## disjoint splitting ##
    # solver = "CBS"
    # disjoint = True    
    
    # # input_instance = ".demo_disjoint_ct/instances/instance.txt"
    # # output_fig = "..static/content/figures/maps/map_disjoint.png"

    # input_instance = "demo_disjoint_ct/instances/exp0.txt"
    # output_fig = "demo_disjoint_ct/figures/disjoint0.png"

    # print(input_instance)



    # create_plot(input_instance, output_fig)


    # # input_instance = glob.glob("static/content/instances/new_instance.txt")

    # results = create_animation(input_instance, output_fig, "CBS", True)
    # cost = get_sum_of_cost(results[0])

    # print("***printing results***")
    # print('cost:  ', cost)
    # print('paths: ', results[0])
    # print('n_gen: ', results[1])
    # print('n exp: ', results[2])
    # print('time:  ', results[3])

  ## disjoint splitting ##
    solver = "CBS"
    disjoint = True    
    
    # input_instance = ".demo_disjoint_ct/instances/instance.txt"
    # output_fig = "..static/content/figures/maps/map_disjoint.png"

    input_instance = "demo_disjoint_ct/instances/exp0.txt"
    output_fig = "demo_disjoint_ct/figures/disjoint0.gif"

    output_CT_figs_dir = "demo_disjoint_ct/figures/disjoint"

    print(input_instance)

    output_map = "demo_disjoint_ct/figures/disjoint0.png"
    create_plot(input_instance, output_map)


    # input_instance = glob.glob("static/content/instances/new_instance.txt")

    solution = create_animation_CT(input_instance, output_CT_figs_dir, "CBS", disjoint)
    CT_gen_nodes, CT_exp_nodes, num_nodes_gen, num_nodes_exp = [solution[i] for i in range(4)]
    
    result_file = open("demo_disjoint_ct/results/disjoint.txt", "w", buffering=1)


    for node in CT_gen_nodes:
        result_file.write("id: {}, cost:{}\n".format(node['node_i'], node['cost']))
        if "exp_i" in node:
            result_file.write("{}th expanded\n".format(node['exp_i']))
        result_file.write("\tcollision\n")
        if node['collisions']:
            result_file.write("\t")
            result_file.write(json.dumps(node['collisions'][0]))
            result_file.write("\n")
        else:
            result_file.write("\tno collision\n")
        result_file.write("\tconstraints\n")
        if node['constraints']:
            for c in node['constraints']:
                result_file.write("\t")
                result_file.write(json.dumps(c))
                result_file.write("\n")
        else:
            result_file.write("\tno constraints\n")
        result_file.write("\n\n")

    result_file.close()


    ## standard splitting ##
    solver = "CBS"
    disjoint = False    
    
    # input_instance = ".demo_disjoint_ct/instances/instance.txt"
    # output_fig = "..static/content/figures/maps/map_disjoint.png"

    input_instance = "demo_disjoint_ct/instances/exp0.txt"
    output_fig = "demo_disjoint_ct/figures/standard0.gif"

    output_CT_figs_dir = "demo_disjoint_ct/figures/standard"

    print(input_instance)

    output_map = "demo_disjoint_ct/figures/standard0.png"
    create_plot(input_instance, output_map)


    # input_instance = glob.glob("static/content/instances/new_instance.txt")

    solution = create_animation_CT(input_instance, output_CT_figs_dir, "CBS", disjoint)
    CT_gen_nodes, CT_exp_nodes, num_nodes_gen, num_nodes_exp = [solution[i] for i in range(4)]
    
    result_file = open("demo_disjoint_ct/results/standard.txt", "w", buffering=1)


    for node in CT_gen_nodes:
        result_file.write("id: {}, cost:{}\n".format(node['node_i'], node['cost']))
        if "exp_i" in node:
            result_file.write("{}th expanded\n".format(node['exp_i']))
        result_file.write("\tcollision\n")
        if node['collisions']:
            result_file.write("\t")
            result_file.write(json.dumps(node['collisions'][0]))
            result_file.write("\n")
        else:
            result_file.write("\tno collision\n")
        result_file.write("\tconstraints\n")
        if node['constraints']:
            for c in node['constraints']:
                result_file.write("\t")
                result_file.write(json.dumps(c))
                result_file.write("\n")
        else:
            result_file.write("\tno constraints\n")
        result_file.write("\n\n")

    result_file.close()







    # results = create_animation(input_instance, output_fig, "CBS", disjoint)
    # cost = get_sum_of_cost(results[0])

    # print("***printing results***")
    # print('cost:  ', cost)
    # print('paths: ', results[0])
    # print('n_gen: ', results[1])
    # print('n exp: ', results[2])
    # print('time:  ', results[3])

    ## standard splitting ##

    # # input_instance = glob.glob("code/instances/exp2_1.txt")
    # for file in input_instance:

    #     print("***Import an instance***")
    #     print(file)
    #     my_map, starts, goals = import_mapf_instance(file)
    #     print_mapf_instance(my_map, starts, goals)

    #     if solver == "CBS":
    #         print("***Run CBS***")
    #         cbs = CBSSolver(my_map, starts, goals)
    #         solution = cbs.find_solution(disjoint)

    #         if solution is not None:
    #             # print(solution)
    #             paths, nodes_gen, nodes_exp = [solution[i] for i in range(3)]
    #             if paths is None:
    #                 raise BaseException('No solutions')  
    #         else:
    #             raise BaseException('No solutions')

    #     elif solver == "ICBS_CB":
    #         print("***Run CBS***")
    #         cbs = ICBS_CB_Solver(my_map, starts, goals)
    #         solution = cbs.find_solution(disjoint)

    #         if solution is not None:
    #             # print(solution)
    #             paths, nodes_gen, nodes_exp = [solution[i] for i in range(3)]
    #             if paths is None:
    #                 raise BaseException('No solutions')  
    #         else:
    #             raise BaseException('No solutions')

    #     elif solver == "ICBS":
    #         print("***Run CBS***")
    #         cbs = ICBS_Solver(my_map, starts, goals)
    #         solution = cbs.find_solution(disjoint)

    #         if solution is not None:
    #             # print(solution)
    #             paths, nodes_gen, nodes_exp = [solution[i] for i in range(3)]
    #             if paths is None:
    #                 raise BaseException('No solutions')  
    #         else:
    #             raise BaseException('No solutions')


    #     elif solver == "Independent":
    #         print("***Run Independent***")
    #         solver = IndependentSolver(my_map, starts, goals)
    #         paths, nodes_gen, nodes_exp = solver.find_solution()
    #     elif solver == "Prioritized":
    #         print("***Run Prioritized***")
    #         solver = PrioritizedPlanningSolver(my_map, starts, goals)
    #         paths, nodes_gen, nodes_exp = solver.find_solution()
    #     else:
    #         raise RuntimeError("Unknown solver!")

    #     cost = get_sum_of_cost(paths)


    #     print("***Test paths on a simulation***")
    #     animation = Animation(my_map, starts, goals, paths)
    #     # animation.save("output.mp4", 1.0)
    #     animation.save('static/content/figures/test_fig.gif', 1)
    #     animation.show()
        


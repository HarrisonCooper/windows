# -*- coding: utf-8 -*-
"""
Correct overlap

@author: Marzieh Tehrani
@commented: Harrison Paul Cooper, 2017
@updated: Harrison Paul Cooper, 2018
@last_updated: Harrison Paul Cooper, 23/04/2018
"""
import random
import numpy as np


import matplotlib.pyplot as plt


def initiate_OC(env):
    """
    Main overlap function.

    Adds the three agents to the list cells and their positions to the list values
    :param env: The size of the environment and number and type of agents present
    :return: An environment where no cells are overlapping
    """
    cells = []
    for cell in env.senescent_cells:
        cells.append(cell)
    for cell in env.proliferating_cells:
        cells.append(cell)    
    for cell in env.quiescent_cells:
        cells.append(cell)

    values = [[[0 for k in range(2)] for j in range(1)] for i in range(len(cells))]

    for cell in range(len(cells)):
        # initial position and displacement values for all the cells (t=0)
        values[cell][0] = [cells[cell].pos[0], cells[cell].pos[1]]  # [xi, yi]

    plot_values = [[0 for j in range(0)] for i in range(2)]  # row1 = tally, row2 = overlap error
    check_overlap(env, cells, values, plot_values, OCM_it=0)


def check_overlap(env, cells, values, plot_values, OCM_it):
    """
    Checks to see if any two cells are overlapping.

    :param env: The size of the environment and number and type of agents present
    :param cells: List of each agent currently in iteration
    :param values: Array of each cells xi, yi position
    :param plot_values: row1 = tally, row2 = overlap error
    :param OCM_it:
    :return: List of overlapping cells
    """
    overlap_tally = 0    
    overlap_error = 0
    overlap = [[0 for k in range(len(cells))] for j in range(len(cells))]
    
    for i in range(len(overlap)):
        xi = values[i][len(values[i])-1][0]
        yi = values[i][len(values[i])-1][1]
        ri = cells[i].radius
        for j in range(i, len(overlap)):
            if i != j:
                xj = values[j][len(values[j])-1][0]
                yj = values[j][len(values[j])-1][1]
                rj = cells[j].radius
                
                if not rj:
                    rj = ri

                overlap[i][j] = np.sqrt((xj-xi)**2+(yj-yi)**2) - (ri+rj)

                if overlap[i][j] < -(ri+rj)/100.0:
                    overlap_tally += 1
                    overlap_error += overlap[i][j]
    
    plot_values[0].append(overlap_tally)
    plot_values[1].append(overlap_error*-1.0)

    if overlap_tally > 0 and OCM_it < 200:
        correct_overlap(env, cells, values, plot_values, OCM_it)
        
    if overlap_tally == 0 and OCM_it < 200:
        update_pos_ABM(env, values)    
        display_plot_values(plot_values, OCM_it)

    if overlap_tally >= 0 and OCM_it == 200:
        update_pos_ABM(env, values)
        update_radii(env, cells, overlap)
        display_plot_values(plot_values, OCM_it)

        
def correct_overlap(env, cells, values, plot_values, OCM_it):
    """
    Any overlapping cells have different localised positions tested to see if that corrects them.

    :param env: The size of the environment and number and type of agents present
    :param cells: List of each agent currently in iteration
    :param values: Array of each cells xi, yi position
    :param plot_values: row1 = tally, row2 = overlap error
    :param OCM_it:
    :return: List of positions overlapping cells need to be moved to
    """
    for i in range(len(values)):
        ri = cells[i].radius
        xi = values[i][len(values[i])-1][0]  # current x value (most updated)
        yi = values[i][len(values[i])-1][1]  # current y value (most updated)

        neighbour = []  # neighbour ([0:prev_xj, 1:prev_yi, 2:prev_uxj, 3:prev_uyj, 4:kij, 5:kijx, 6:kijy])

        for j in range(len(values)):
            if i != j:
                xj = values[j][len(values[j])-1][0]
                yj = values[j][len(values[j])-1][1]
                rj = cells[j].radius
                dist_ij = np.sqrt((xj-xi)**2+(yj-yi)**2)

                if not ri:
                    ri = rj

                if not rj:
                    rj = ri

                if (dist_ij-(ri+rj)) < -(ri+rj)/100.0:
                    Lij = ri + rj
                    dist_ijx = abs(xj-xi)
                    dist_ijy = abs(yj-yi)
                    uijx = (xj-xi)/dist_ij
                    uijy = (yj-yi)/dist_ij
                    neighbour.append([Lij, dist_ijx, dist_ijy, uijx, uijy])

        if len(neighbour) > 0:
            totalx = 0
            totaly = 0 
            for j in range(len(neighbour)):
                Lij = neighbour[j][0]
                dist_ijx = neighbour[j][1]
                dist_ijy = neighbour[j][2]
                uijx = neighbour[j][3]
                uijy = neighbour[j][4]
                totalx = totalx + (uijx*(dist_ijx-Lij))
                totaly = totaly + (uijy*(dist_ijy-Lij))

            new_xi = xi + 0.1*totalx
            new_yi = yi + 0.1*totaly

            # To ensure cells don't move off model
            if new_xi > (env.size - ri):
                new_xi = (env.size - ri)-random.random()*0.02

            if new_xi < ri:
                new_xi = ri+random.random()*0.02

            if new_yi > (env.size - ri):
                new_yi = (env.size - ri)-random.random()*0.02

            if new_yi < ri:
                new_yi = ri+random.random()*0.02    
    
            values[i].append([new_xi, new_yi])

        if len(neighbour) > 3:  # parameter: changeable for confluence
            if not cells[i].iscluster:
                cells[i].iscluster = True
        else:
            cells[i].iscluster = False

    check_overlap(env, cells, values, plot_values, OCM_it+1)


def update_pos_ABM(env, values):
    """
    Updates overlapping cells positions.

    :param env: The size of the environment and number and type of agents present
    :param values: Array of each cells xi, yi position
    :return: Updated cells positions
    """
    i = 0        
    for agent in env.senescent_cells:
        npos = np.zeros(2)
        npos[0] = values[i][len(values[i])-1][0]
        npos[1] = values[i][len(values[i])-1][1]
        agent.move_cell(npos)
        i += 1
    for agent in env.proliferating_cells:
        npos = np.zeros(2)
        npos[0] = values[i][len(values[i])-1][0]
        npos[1] = values[i][len(values[i])-1][1]
        agent.move_cell(npos)
        i += 1
    for agent in env.quiescent_cells:
        npos = np.zeros(2)
        npos[0] = values[i][len(values[i])-1][0]
        npos[1] = values[i][len(values[i])-1][1]
        agent.move_cell(npos)
        i += 1


def update_radii(env, cells, overlap):
    """

    :param env:
    :param cells:
    :param overlap:
    :return:
    """
    for i in range(len(overlap)):
        ri = cells[i].radius
        for j in range(len(overlap)):
            rj = cells[j].radius
            if overlap[i][j] < -(ri+rj)/50.0:
                cells[i].radius = ri - overlap[i][j]/-10.0
                cells[j].radius = rj - overlap[i][j]/-10.0

    i = 0
    for agent in env.senescent_cells:
        agent.radius = cells[i].radius
        i += 1
    for agent in env.proliferating_cells:
        agent.radius = cells[i].radius
        i += 1
    for agent in env.quiescent_cells:
        agent.radius = cells[i].radius
        i += 1


def display_plot_values(plot_values, OCM_it):
    """
    Displays graph of number of overlapping cells each OCM_it

    :param plot_values: row1 = tally, row2 = overlap error
    :param OCM_it:
    :return: Graph of overlapping cell numbers
    """
    time = []
    for i in range(OCM_it+1):
        time.append(i)
    f, axarr = plt.subplots(2, sharex=True)
    axarr[0].plot(time, plot_values[0])
    axarr[0].set_title('Number of pairs of overlapping cells')
    axarr[1].plot(time, plot_values[1])
    axarr[1].set_title('Total overlap error')
    axarr[1].set_xlabel('OCM_it')        

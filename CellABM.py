# -*- coding: utf-8 -*-
"""
CellAbm - Master Script

@author: Marzieh, 2014
@commented: Harrison Paul Cooper, 2017
@updated: Harrison Paul Cooper, 2018
@last_updated: Harrison Paul Cooper, 23/04/2018
"""
#%%
import numpy as np
import sys


from senescent_cells import sc
from proliferating_cells import pc
from quiescent_cells import qc
from environment import environment
from solver import agent_solve
from results import plot_2d, growth_curve
from overlap import initiate_OC


def CellABM(size, nsc, npc, steps, wsize, directory, freq=0, labels=False):
    """
    Main function that controls the rest of the program.

    Called on the command line with CellABM(size of environment, number of senescent cells, number of proliferating
    cells, number of steps, size of wound, save name for output graphs)
    :param size: The size of the environment, measured in micrometers
    :param nsc: The number of starting senescent cells
    :param npc: The number of starting proliferating cells
    :param steps: The number of iterations the simulation is to be run for
    :param wsize: The width of the intended wound, measured in micrometers
    :param directory: The name of the file where the output graphs will be saved
    :param freq:
    :param labels:
    :return: Several graphs showing progression of endothelial cells when wounded
    """
    sc.num_sc = 0
    pc.num_pc = 0
    qc.num_qc = 0

    env = environment(size)  # Initialise the environments size
    env.create_agents(nsc, npc)  # Populate the environment with initial cells

    num_cells = np.zeros((3, steps+1))
    num_cells[0, 0] = sc.num_sc
    num_cells[1, 0] = pc.num_pc
    num_cells[2, 0] = qc.num_qc

    initiate_OC(env)  # Correct any overlapping cells
    plot_2d(env, directory, labels, n_it=0)  # Create initial graph of cell positions

    counter = 0  # Counter to check if monolayer has been wounded
    count=[]
    
    for n_it in range(1, steps+1):
        print("iteration %s" % (str(n_it)))
        agent_solve(env)
        initiate_OC(env)
        
        if counter == 1:
            coun = num_cells_in_wound(env, wsize)
            count.append(coun)
            print(count)
        
        """
        Logic for confluence.

        When the number of quiescent cells has reached the threshold, indicating
        a monolayer of cells has formed, the environment simulates a wound by removing
        a strip of cells and continues with the simulation.
        When the number of quiescent cells has passed the threshold for a second time,
        the simulation detects this as a new confluence, halting the program.
        """
        if qc.num_qc >= (pc.num_pc/3):  # 4):
            if counter == 0:
                env.wound(wsize)  # Remove a strip of cells
                print("***WOUNDED***")
                timer = n_it
                counter += 1
            else:
                time = n_it - timer
                if time > 12:  # 2:  # Quiescent cells take an iteration or two to differentiate back to proliferating cells
                    print("CONFLUENCE DETECTED, time taken: %s itteration == %s hours." % (time, time*6))
                    print('Senescent cells = %s | Endothelial cells = %s | Quiescent cells = %s' % (sc.num_sc,
                                                                                                    pc.num_pc,
                                                                                                    qc.num_qc))
                    num_cells[0, n_it] = sc.num_sc
                    num_cells[1, n_it] = pc.num_pc
                    num_cells[2, n_it] = qc.num_qc
                    plot_2d(env, directory, labels, n_it)
                    growth_curve(num_cells, directory)
                    print(count)
                    sys.exit("End")
        
        if freq > 0:
            if not n_it % freq:
                plot_2d(env, directory, labels, n_it)
        else:
            plot_2d(env, directory, labels, n_it)

        num_cells[0, n_it] = sc.num_sc
        num_cells[1, n_it] = pc.num_pc
        num_cells[2, n_it] = qc.num_qc

        print('Senescent cells = %s | Endothelial cells = %s | Quiescent cells = %s' % (sc.num_sc, pc.num_pc,
                                                                                        qc.num_qc))

    growth_curve(num_cells, directory)
    print(count)
    return env, num_cells
    
#%%
    
def num_cells_in_wound(env, wsize):
        num=0
        xlength = wsize
        x1 = (env.size/2) - (xlength/2)
        x2 = (env.size/2) + (xlength/2)
        
        for n in range(len(env.senescent_cells)):
            if x1 < env.senescent_cells[n].pos[0] < x2:
                num+=1
                
        for n in range(len(env.proliferating_cells)):
            if x1 < env.proliferating_cells[n].pos[0] < x2:
                num+=1
                
        for n in range(len(env.quiescent_cells)):
            if x1 < env.quiescent_cells[n].pos[0] < x2:
                num+=1

        return num
# -*- coding: utf-8 -*-
"""
Methods to store and display results

@author: Marzieh, 2014
@commented: Harrison Paul Cooper, 2017
@updated: Harrison Paul Cooper, 2018
@last_updated: Harrison Paul Cooper, 23/04/2018
"""
import matplotlib.pyplot as plt
from matplotlib.patches import Circle


from senescent_cells import sc
from proliferating_cells import pc
from quiescent_cells import qc
import os
#%%


def plot_2d(env, directory, labels, n_it):
    """
    Each iteration shows position of agents in graph.

    Each agent has a different colour so is easily recognisable
    on the graph.
    :param env: Used to find number of each type of agent
    :param directory: Used as save location
    :param labels:
    :param n_it: Current iteration
    :return: A 2D graph of agents in the spatial environment
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, aspect='equal')

    for n in range(len(env.senescent_cells)):
        ax.add_artist(Circle((env.senescent_cells[n].pos[0], env.senescent_cells[n].pos[1]),
                             env.senescent_cells[n].radius, fc='g', alpha=0.5))
        if labels is True:
            ax.text(env.senescent_cells[n].pos[0]-0.7, env.senescent_cells[n].pos[1]-0.5,
                    str(env.senescent_cells[n].ID), fontsize=7)
    
    for n in range(len(env.proliferating_cells)):
        ax.add_artist(Circle((env.proliferating_cells[n].pos[0], env.proliferating_cells[n].pos[1]),
                             env.proliferating_cells[n].radius, fc='r', alpha=0.5))
        if labels is True:
            ax.text(env.proliferating_cells[n].pos[0]-0.7, env.proliferating_cells[n].pos[1]-0.5,
                    str(env.proliferating_cells[n].ID), fontsize=7)
            
    for n in range(len(env.quiescent_cells)):
        ax.add_artist(Circle((env.quiescent_cells[n].pos[0], env.quiescent_cells[n].pos[1]),
                             env.quiescent_cells[n].radius, fc='b', alpha=0.5))
        if labels is True:
            ax.text(env.quiescent_cells[n].pos[0]-0.7, env.quiescent_cells[n].pos[1]-0.5,
                    str(env.quiescent_cells[n].ID), fontsize=7)
    
    plt.axis([0, env.size, 0, env.size])
    
    if n_it == 0:  # Initial iteration
        figname = 'Initial Setup \n No of Senescent cells = %s \n No of Proliferating cells = %s \n ' \
                  'No of Quiescent cells = %s' % (str(sc.num_sc), str(pc.num_pc), str(qc.num_qc))
        filename = 'Initial_Setup' 
    else:
        figname = 'Iteration %s \n No of Senescent cells = %s \n No of Proliferating cells = %s \n ' \
                  'No of Quiescent cells = %s' % (str(n_it), str(sc.num_sc), str(pc.num_pc), str(qc.num_qc))
        filename = "Iteration_" + str(n_it)
    
    ax.set_title(figname)
    save(filename, directory, '2d')
    plt.close(fig)
#%%


def growth_curve(num_cells, directory):
    """
    Number of each agent per iteration.

    Can be used to see rate of population change
    throughout the simulation.
    This is only output either when all iterations have completed
    or if a confluence has formed after a wound.
    :param num_cells: Matrix containing number of each agent at each iteration
    :param directory: Name of save file to be created
    :return: A graph showing change in number of agents over time
    """
    fig = plt.figure()
    plt.plot(num_cells[0, :], 'g', label='Senescent cells')
    plt.hold(True)
    plt.plot(num_cells[1, :], 'r', label='Proliferating cells')
    plt.plot(num_cells[2, :], 'b', label='Quiescent cells')
    fig.suptitle('growth_curve')
    plt.xlabel('interation')
    plt.ylabel('number of cells')
    plt.legend(loc="upper left", bbox_to_anchor=[0, 1], ncol=2, shadow=True, fancybox=True)
    save('growth_curve.png', directory)
#%%


def save(filename, directory, sub=''):
    """
    Saves graphs into user defenced directory.

    :param filename: Name of the save file
    :param directory: Name of the save directory
    :param sub:
    :return: File structure of graphs showing simulation progression
    """
    if directory:
        d = directory
    else:
        d = 'CellAbm_Output'
    if not os.path.exists(d):
        os.makedirs(d)
    os.chdir(d)
    if sub != '':
        if not os.path.exists(sub):
            os.makedirs(sub)
        os.chdir(sub)
        plt.savefig(filename)
        os.chdir('..')
    else:
        plt.savefig(filename)
    os.chdir('..')    
#%%

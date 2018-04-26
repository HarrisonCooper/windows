# -*- coding: utf-8 -*-
"""
Creating environment and initial model cells (inc pos, direc and stage info)

@author: Marzieh, 2014
@commented: Harrison Paul Cooper, 2017
@updated: Harrison Paul Cooper, 2018
@last_updated: Harrison Paul Cooper, 23/04/2018
"""
import numpy as np
import math
import random


from senescent_cells import sc
from proliferating_cells import pc
from quiescent_cells import qc
from numpy.random import rand


class environment:
    """
    Controls the instantiation of the initial cells and wound

    Public methods:
    :create_agents: Instantiation of initial cells
    :wound: Creation of simulated wound
    """
    def __init__(self, size):
        """
        How the environment is defined.

        :param size: Size of environment in micrometers
        """
        self.size = size

    def create_agents(self, nsc, npc):
        """
        Populates simulation with starting cells.

        Creates a user defined number of senescent and proliferating
        cells, giving them a random size (within a range), a random position,
        a random stage (age, within a range), a random direction, a set
        turnover (number of times divided and appends them to the list
        of cells.
        :param nsc: User defined starting number of senescent cells
        :param npc: User defined starting number of proliferating cells
        :return: Three lists containing the different starting cell agents
        """
        senescent_cells = []
        proliferating_cells = []
        quiescent_cells = []
        print(nsc, npc)

        for s in range(nsc):
            ID = s
            radius = random.randint(10,50) 
            area = math.pi*(radius*radius)
            pos = [radius+(round(rand(), 3))*(self.size-(2*radius)), radius+(round(rand(), 3))*(self.size-(2*radius))]
            stage = np.ceil(rand()*4380)
            direc = rand()*2*np.pi
            turnover = 1
            senescent_cells.append(sc(ID, stage, pos, direc, turnover, radius, area))


        for p in range(npc):
            ID = p
            radius = random.randint(5,10)
            area = math.pi*(radius*radius)
            pos = [radius+(round(rand(), 3))*(self.size-(2*radius)), radius+(round(rand(), 3))*(self.size-(2*radius))]
            stage = np.ceil(rand()*4)
            direc = rand()*2*np.pi
            turnover = 1
            proliferating_cells.append(pc(ID, stage, pos, direc, turnover, radius, area))

        #if list type is seperate (each agent type has its own list)
        self.senescent_cells = senescent_cells
        self.proliferating_cells = proliferating_cells
        self.quiescent_cells = quiescent_cells

    def wound(self, wsize):
        """
        Creates the user defined wound.

        The wound is across the entire Y axis and centered on the X axis.
        From meeting with medical expert, Paul, he stated a wound size of 100 and 500
        microns is a typical scratch assay size, but larger sizes would be good.
        :param wsize: User defined wound size in micrometers
        :return: The environment with cells removed from wounded area
        """
        xlength = wsize
        x1 = (self.size/2) - (xlength/2)
        x2 = (self.size/2) + (xlength/2)
        
        for n in range(len(self.senescent_cells)):
            if x1 < self.senescent_cells[n].pos[0] < x2:
                self.senescent_cells[n].kill_cell()

        for n in range(len(self.senescent_cells)):
            if self.senescent_cells[n].pos[0] > x1 and self.senescent_cells[n].pos[0] < x2:
                self.senescent_cells[n].kill_cell()
                
        for n in range(len(self.proliferating_cells)):
            if x1 < self.proliferating_cells[n].pos[0] < x2:
                self.proliferating_cells[n].kill_cell()
                
        for n in range(len(self.quiescent_cells)):
            if x1 < self.quiescent_cells[n].pos[0] < x2:
                self.quiescent_cells[n].kill_cell()
                
        # remove dead cells
        self.proliferating_cells = ([a for a in self.proliferating_cells if not a.dead])
        self.senescent_cells = ([a for a in self.senescent_cells if not a.dead])
        self.quiescent_cells = ([a for a in self.quiescent_cells if not a.dead])

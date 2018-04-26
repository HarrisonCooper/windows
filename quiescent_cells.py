#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 18:29:05 2018

@author: Harrison Paul Cooper, 2018
@last_updated: Harrison Paul Cooper, 23/4/18
"""
import random
import math

from general_cell import general_cell
from senescent_cells import sc


class qc(general_cell):
    """
    This is a subclass of general cell for the quiescent agent.

    Public methods:
    :senescence: When cell is old enough differentiates to senescent
    :proliferating: When cell can proliferate differentiates to proliferating
    Instance variables:
    :min_radius: The smallest the cell can be before dying
    :max_speed: How fast the cell moves per iteration
    :max_direc:
    :max_stage: How many iterations until the cell differentiates to senescent
    :num_qc: The total number of quiescent cells
    """
    min_radius = 4.9
    max_speed = 0  # Quiescent cells cannot move
    max_direc = round((2.0/3)*math.pi, 3)
    max_stage = 240  # each level = 6hrs of real time
    num_qc = 0
    
    def __init__(self, ID=[], stage=[], pos=[], direc=[], turnover=[], radius=[], area=[]):
        """
        How the quiescent cell is defined.

        :param ID: The unique identifier of the cell
        :param stage: The age of the cell
        :param pos: The position of the cell
        :param direc: The direction of the cell
        :param turnover: The age of the cell
        :param radius: The radius of the cell
        :param area: The area of the cell
        """
        general_cell.__init__(self, ID, stage, pos, direc, turnover, radius, area)
        self.__class__.num_qc += 1
    
    def __repr__(self):
        out = ('\nClass(qc)\nID : {0}\nStage : {1}\nPos : {2}\ndirec : {3}\n'. format(self.ID, self.stage,
                                                                                      self.pos, self.direc))
        return out

    def senescence(self):
        """
        Differentiate current (quiescent) cell into senescent cell.

        If the cell has passed its Hayflick limit, it will differentiate,
        else the cell remains unchanged and continues
        :return: Either aged cell or a new senescent cell in the same position
        """
        if self.stage == self.max_stage:  # Required minimum of 239 iterations
            self.kill_cell()
            senescent_pos = [self.pos[0], self.pos[1]]
            senescent_cell = sc(ID=sc.num_sc, stage=1, pos=senescent_pos, direc=random.random() * 2 * math.pi,
                                turnover=1, radius=self.radius, area=self.area)
            senescence = senescent_cell
        else:
            senescence = None
            self.stage += 1 
        return senescence
        
    def proliferating(self):
        """
        Differentiate current (quiescent) cell back to proliferating cell.

        :return: A new proliferating cell in the same position
        """
        from proliferating_cells import pc
        self.kill_cell()
        proliferating_pos = [self.pos[0], self.pos[1]]
        proliferating_cell = pc(ID=pc.num_pc, stage=1, pos=proliferating_pos, direc=random.random() * 2 * math.pi,
                                turnover=self.turnover, radius=self.radius, area=self.area)
        proliferating = proliferating_cell
        return proliferating

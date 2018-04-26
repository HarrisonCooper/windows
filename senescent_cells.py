# -*- coding: utf-8 -*-
"""
Agents - cancer cells (cc) 
Updated to Senescent Cells (sc)

@author: Marzieh, 2014
@commented: Harrison Paul Cooper, 2017
@updated: Harrison Paul Cooper, 2018
@last_updated: Harrison Paul Cooper, 23/04/2018
"""
import math


from general_cell import general_cell


class sc(general_cell):
    """
    This is a subclass of general cell for the senescent agent.

    Public methods:
    :growth: Increases area of cell
    Instance variables:
    :min_radius: The smallest the cell can be before dying
    :max_speed: How fast the cell moves per iteration
    :max_direc:
    :max_stage: How many iterations the cell can last for
    :num_sc: The total number of senescent cells
    """
    min_radius = 5
    max_speed = 0  # Senescent cells don't move
    max_direc = round((2.0/3)*math.pi, 3)
    max_stage = 4380  # represents 3 years
    num_sc = 0
    
    def __init__(self, ID=[], stage=[], pos=[], direc=[], turnover=[], radius=[], area=[]):
        """
        How the senescent cell is defined.

        :param ID: The unique identifier of the cell
        :param stage: The age of the cell
        :param pos: The position of the cell
        :param direc: The direction of the cell
        :param turnover: The age of the cell
        :param radius: The radius of the cell
        :param area: The area of the cell
        """
        general_cell.__init__(self, ID, stage, pos, direc, turnover, radius, area)
        self.__class__.num_sc += 1
    
    def __repr__(self):
        out = ('\nClass(sc)\nID : {0}\nStage : {1}\nPos : {2}\ndirec : {3}\n'. format(self.ID, self.stage, self.pos,
                                                                                      self.direc))
        return out

    def growth(self):
        """
        Increases area of cell.

        As long as cell is smaller than threshold, it will increase in size
        each iteration. Also each iteration its stage (age) is increased by 1
        :return: The cell with incremented stage and either the same size or larger
        """
        if self.radius < 50:
            self.radius += 0.8
            self.area = math.pi*(self.radius*self.radius)
            # self.area = self.area * (1.25)
            # self.radius = math.sqrt(self.area/math.pi)
        self.stage += 1
        return self

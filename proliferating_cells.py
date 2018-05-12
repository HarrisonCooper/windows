# -*- coding: utf-8 -*-
"""
Agents - stem cells (sc)
Updated to Proliferating Cells (pc)

@author: Marzieh, 2014
@commented: Harrison Paul Cooper, 2017
@updated: Harrison Paul Cooper, 2018
@last_updated: Harrison Paul Cooper, 23/04/2018
"""
import random
import math


from general_cell import general_cell
from senescent_cells import sc
from quiescent_cells import qc


class pc(general_cell):
    """
    This is a subclass of general cell for the proliferating agent.

    Public methods:
    :split_cell: Creation of daughter cell
    :senescence: When max_turnover is reached cell differentiates to senescent
    :mitosis: M phase of the cell cycle where the cell splits
    :growth: The cell doubles in size during one cycle
    :quiescence: When the cell can no longer proliferate it differentiates to quiescent
    Instance variables:
    :min_radius: The smallest the cell can be before dying
    :max_speed: How fast the cell moves per iteration
    :max_direc:
    :max_stage: How many iterations are in one cell cycle
    :max_turnover: How many times the cell can proliferate before becoming senescent
    :num_pc: The total number of proliferative cells
    """
    min_radius = 4.9
    max_speed = 180  # 360  # move at 1micrometer a min
    max_direc = round((2.0/3)*math.pi, 3)
    max_stage = 4
    max_turnover = 50  # Hayflick limit of 50
    num_pc = 0

    def __init__(self, ID=[], stage=[], pos=[], direc=[], turnover=[], radius=[], area=[]):
        """
        How the proliferating cell is defined.

        :param ID: The unique identifier of the cell
        :param stage: The age of the cell
        :param pos: The position of the cell
        :param direc: The direction of the cell
        :param turnover: The age of the cell
        :param radius: The radius of the cell
        :param area: The area of the cell
        """
        general_cell.__init__(self, ID, stage, pos, direc, turnover, radius, area)
        self.__class__.num_pc += 1

    def __repr__(self):
        out = ('\nClass(pc)\nID : {0}\nStage : {1}\nPos : {2}\ndirec : {3}\n'. format(self.ID, self.stage,
                                                                                      self.pos, self.direc))
        return out

    def split_cell(self):
        """
        During mitosis the cell divides into two daughter cells.

        The two cells are now half the size of the orignial cell
        :return: The new daughter cell
        """
        self.area /= 2
        self.radius = math.sqrt(self.area/math.pi)
        new_cell_pos = [self.pos[0]+random.uniform(-1, 1)*self.radius, self.pos[1]+random.uniform(-1, 1)*self.radius]
        new_cell = pc(ID=self.num_pc, stage=1, pos=new_cell_pos, direc=random.random() * 2 * math.pi,
                      turnover=1, radius=self.radius, area=self.area)
        self.stage = 1
        self.turnover += 1
        self.pos = [self.pos[0]+random.uniform(-1, 1)*self.radius, self.pos[1]+random.uniform(-1, 1)*self.radius]
        #print('new proliferating cell created with cell ID = %s' % str(new_cell.ID))
        return new_cell
        
    def senescence(self):
        """
        Differentiate current (proliferating) cell into senescent cell.

        If the cell has split enough times and passed its Hayflick limit,
        it will transition, else the cell remains unchanged and continues
        :return: Either unchanged cell or new senescent cell
        """
        if self.turnover == self.max_turnover:
            self.kill_cell()
            senescent_pos = [self.pos[0], self.pos[1]]
            senescent_cell = sc(ID=sc.num_sc, stage=1, pos=senescent_pos, direc=random.random() * 2 * math.pi,
                                turnover=1, radius=self.radius, area=self.area)
            senescence = senescent_cell
        else:
            senescence = None
        return senescence
        
    def mitosis(self):
        """
        Cell enters M phase.

        When the cell has passed through G0, G1, and G2, it will enter M phase
        where it splits into two identical daughter cells of half size.
        :return: Either unchanged cell or a new daughter cell
        """
        if self.stage == self.max_stage:
            new = self.split_cell()
        else:
            self.stage += 1
            new = None
        return new
        
    def growth(self):
        """
        At each stage of the cell cycle, the cell grows.

        Once a cell has been through each of the four stages, it will have
        doubled in size.
        :return: The grown cell
        """
        if self.stage == 1:  # 1:                 # Increase original size by 1/4
            self.area *= 1.25
        elif self.stage == 2:  # 2:               # Decrease by 1/4 to achieve original, then increase by 2/4
            sa = self.area / 1.25
            self.area = sa * 1.5
        elif self.stage == 3:  # 3:               # Decrease by 2/4 to achieve original, the increase by 3/4
            sa = self.area / 1.5
            self.area = sa * 1.75
        elif self.stage == 4:                               # Decrease by 3/4 to achieve original, then double
            sa = self.area / 1.75
            self.area = sa * 2
        self.radius = math.sqrt(self.area/math.pi)
        # print(self.stage)
        return self.mitosis()

    def quiescence(self):
        """
        Differentiate current (proliferating) cell into quiescent cell.

        When the cell is surrounded and is unable to proliferate anymore,
        it will turn quiescent. Here the original cell is removed from the
        simulation and a new cell of type quiescent it created.
        :return: A new quiescent cell
        """
        self.kill_cell()
        quiescent_pos = [self.pos[0], self.pos[1]]
        quiescent_cell = qc(ID=qc.num_qc, stage=1, pos=quiescent_pos, direc=random.random()*2*math.pi,
                            turnover=self.turnover, radius=self.radius, area=self.area)
        quiescent_cell.iscluster = True
        quiescence = quiescent_cell
        return quiescence

# -*- coding: utf-8 -*-
"""
Agents - general cell class

@author: Marzieh, 2014
@commented: Harrison Paul Cooper, 2017
@updated: Harrison Paul Cooper, 2018
@last_updated: Harrison Paul Cooper, 23/04/2018
"""
import random
import math


from messages import messages


class general_cell:
    """
    This is the super class of the three agents:
        Senescent
        Quiescent
        Proliferating

    Public methods:
    :process_message: Updates cells state
    :move_cell: Changes cells position
    :kill_cell: Removes cell from simulation
    :migrate: Looks for places the cell can move to
    :apoptosis: Cell death conditions
    """
    def __init__(self, ID=[], stage=[], position=[], direc=[], turnover=[], radius=[], area=[]):
        """
        How each cell is defined.

        These attributes vary per cell
        :param ID: The cells unique identifier
        :param stage: The age of the cell
        :param position: The [X, Y] position of the cell
        :param direc: The direction of the cell
        :param turnover: The number of times the cell can divide
        :param radius: The radius of the cell
        :param area: The area of the cell
        """
        self.ID = ID
        self.pos = position
        self.stage = stage
        self.direc = direc
        self.turnover = turnover
        self.radius = radius
        self.area = area
        self.dead = False
        self.iscluster = False
        
        # Messages passed to this agent
        self.messages = messages(self.pos, self.dead)

    def process_messages(self):
        """
        Sets messages assigned to cells.

        Called each iteration and used to determine whether the cell died this iteration
        or if its alive, where its new position (if it has one) is.
        :return: Current cell states
        """
        self.dead = self.messages.dead     # If this cell died in this iteration, set its current state as dead
        self.messages.pos = self.pos    # put position from this iteration into message

    def move_cell(self, new_pos):
        """
        Sets cells position to new position.

        :param new_pos: New position of cell
        :return: Updated cell position
        """
        self.pos = new_pos
    
    def kill_cell(self):
        """
        Kills cell.

        Sets the cell to dead and updates its message.
        :return: The updated cell state
        """
        self.dead = True
        self.messages.dead = True
        # print("%s ID%s is dead. radius = %s turnover = %s"
        #     % (self.__class__.__name__, self.ID, self.radius, self.turnover))
        
    def migrate(self, env):
        """
        Possible positions for cell to move.

        Will move the cell by a certain factor (involving its max speed,
        max direction). Stochastic movement and if cell is unable to move
        will try 9 more times before passing cell.
        :param env: The size of the environment and number and type of agents present
        :return: Updated position for the cell
        """
        mig = False
        cnt = 1
        direction = self.direc + random.uniform(-1*self.max_direc, self.max_direc)
        temppos = [0, 0]
        self.speed = random.random()*self.max_speed
        while not mig and cnt <= 10:
            temppos[0] = self.pos[0] + self.speed * math.cos(direction)
            temppos[1] = self.pos[1] + self.speed * math.sin(direction)
            # check that cell has not left edge of model - correct if so.
            if temppos[0]+self.radius < env.size and temppos[1]+self.radius < env.size and \
                temppos[0] >= self.radius and temppos[1] >= self.radius:
                mig = True
            cnt += 1
            direction = direction + (random.uniform(-1*self.max_direc, self.max_direc))
            # if cnt == 10:
            #    print("%s ID%s at position (%s, %s) could not move"
            #          % (self.__class__.__name__, self.ID, round(self.pos[0], 3), round(self.pos[1], 3)))
        if mig:
            self.direc = direction 
            self.move_cell(temppos)
                    
    def apoptosis(self):
        """
        Pre-programmed cell death.

        If the cell shrinks to be smaller than its minimum radius
        it is killed.
        :return: Updated cell state
        """
        if self.radius <= self.min_radius:
            self.kill_cell()

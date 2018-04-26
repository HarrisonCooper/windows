# -*- coding: utf-8 -*-
"""
Managing agent communication

@author: Marzieh, 2014
"""


class messages:
    """
    Class representing messages passed to agents. 
    Each agent contains its own message class which represents messages passed to it. 
    """
    def __init__(self, pos=[], dead=[], cluster=[]):
        self.pos = pos
        self.dead = dead
        self.cluster = cluster

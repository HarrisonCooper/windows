#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 16:30:43 2018

@author: Harrison Paul Cooper
"""
from senescent_cells import sc
import unittest
import random
import math


class TestSenescentCells(unittest.TestCase):

    def test_growth(self):
        senescent_cell1 = sc(ID=1, stage=1, pos=[0, 0], direc=random.random() * 2 * math.pi,
                            turnover=1, radius=5, area=25*math.pi)
        senescent_cell2 = sc(ID=2, stage=1, pos=[0, 0], direc=random.random() * 2 * math.pi,
                             turnover=1, radius=50, area=math.pi*(50*50))
        cell1 = sc.growth(senescent_cell1)
        self.assertEquals(cell1.stage, 2)
        self.assertEquals(cell1.radius, 5.8)
        self.assertEquals(cell1.area, math.pi*(cell1.radius*cell1.radius))
        cell2 = sc.growth(senescent_cell2)
        self.assertEquals(cell2.stage, 2)
        self.assertEquals(cell2.radius, 50)
        self.assertEquals(cell2.area, math.pi*(50*50))

if __name__ == '__main__':
    unittest.main()

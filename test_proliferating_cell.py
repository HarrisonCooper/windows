#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 12:15:44 2018

@author: Harrison Paul Cooper
"""
from quiescent_cells import qc
from senescent_cells import sc
from proliferating_cells import pc
import unittest
import random
import math


class TestProliferatingCells(unittest.TestCase):

    def setUp(self):
        self.pc1 = pc(ID=1, stage=1, pos=[0, 0], direc=random.random() * 2 * math.pi,
                      turnover=1, radius=5, area=25 * math.pi)
        self.pc2 = pc(ID=1, stage=2, pos=[0, 0], direc=random.random() * 2 * math.pi,
                      turnover=1, radius=5, area=self.pc1.area*1.25)
        self.pc3 = pc(ID=1, stage=3, pos=[0, 0], direc=random.random() * 2 * math.pi,
                      turnover=1, radius=5, area=self.pc1.area*1.5)
        self.pc4 = pc(ID=1, stage=4, pos=[0, 0], direc=random.random() * 2 * math.pi,
                      turnover=1, radius=5, area=self.pc1.area*1.75)
        self.pc5 = pc(ID=1, stage=1, pos=[0, 0], direc=random.random() * 2 * math.pi,
                      turnover=50, radius=5, area=25 * math.pi)

    def tearDown(self):
        self.pc1 = pc(ID=1, stage=1, pos=[0, 0], direc=random.random() * 2 * math.pi,
                      turnover=1, radius=5, area=25 * math.pi)
        self.pc2 = pc(ID=1, stage=2, pos=[0, 0], direc=random.random() * 2 * math.pi,
                      turnover=1, radius=5, area=self.pc1.area * 1.25)
        self.pc3 = pc(ID=1, stage=3, pos=[0, 0], direc=random.random() * 2 * math.pi,
                      turnover=1, radius=5, area=self.pc1.area * 1.5)
        self.pc4 = pc(ID=1, stage=4, pos=[0, 0], direc=random.random() * 2 * math.pi,
                      turnover=1, radius=5, area=self.pc1.area * 1.75)
        self.pc5 = pc(ID=1, stage=1, pos=[0, 0], direc=random.random() * 2 * math.pi,
                      turnover=50, radius=5, area=25 * math.pi)

    def test_senescence(self):

        self.assertEquals(self.pc1.__class__, pc)
        self.assertEquals(self.pc5.__class__, pc)

        pc1 = pc.senescence(self.pc1)
        pc5 = pc.senescence(self.pc5)

        self.assertEquals(pc1, None)
        self.assertEquals(pc5.__class__, sc)
        self.assertEquals(pc5.radius, 5)
        self.assertEquals(pc5.area, 25*math.pi)
        self.assertEquals(pc5.pos, [0, 0])
        self.assertEquals(pc5.stage, 1)
        self.assertEquals(pc5.turnover, 1)

    def test_quiescence(self):

        self.assertEquals(self.pc1.__class__, pc)

        pc1 = pc.quiescence(self.pc1)

        self.assertEquals(pc1.__class__, qc)
        self.assertEquals(pc1.turnover, 1)
        self.assertEquals(pc1.pos, [0, 0])
        self.assertEquals(pc1.radius, 5)
        self.assertEquals(pc1.area, 25*math.pi)
        self.assertEquals(pc1.stage, 1)

    def test_split_cell(self):

        old_area = self.pc1.area

        pc1 = pc.split_cell(self.pc1)

        self.assertEquals(pc1.__class__, pc)
        self.assertEquals(pc1.area, self.pc1.area)
        self.assertEquals(self.pc1.area, old_area/2)
        self.assertEquals(pc1.stage, 1)
        self.assertEquals(self.pc1.stage, 1)
        self.assertEquals(pc1.turnover, 1)
        self.assertEquals(self.pc1.turnover, 2)

    def test_mitosis(self):

        pc1 = pc.mitosis(self.pc1)
        pc4 = pc.mitosis(self.pc4)

        self.assertEquals(pc1, None)
        self.assertEquals(self.pc1.stage, 2)
        self.assertEquals(pc4.stage, 1)
        self.assertEquals(pc4.turnover, 1)
        self.assertEquals(pc4.__class__, pc)
        self.assertEquals(self.pc4.turnover, 2)
        self.assertEquals(self.pc4.area, pc4.area)

    def test_growth(self):

        original_area = self.pc1.area

        pc.growth(self.pc1)
        pc.growth(self.pc2)
        pc.growth(self.pc3)
        pc.growth(self.pc4)

        self.assertEquals(self.pc1.area, original_area*1.25)
        self.assertEquals(self.pc1.stage, 2)
        self.assertEquals(self.pc2.area, original_area*1.5)
        self.assertEquals(self.pc2.stage, 3)
        self.assertEquals(self.pc3.area, original_area*1.75)
        self.assertEquals(self.pc3.stage, 4)
        self.assertEquals(self.pc4.area, original_area)
        self.assertEquals(self.pc4.stage, 1)

        new_cell = pc.growth(self.pc3)
        self.assertEquals(new_cell.__class__, pc)
        self.assertEquals(new_cell.area, self.pc3.area)

if __name__ == '__main__':
    unittest.main()

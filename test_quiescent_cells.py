#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 17:03:04 2018

@author: Harrison Paul Cooper
"""
from quiescent_cells import qc
from senescent_cells import sc
from proliferating_cells import pc
import unittest
import random
import math


class TestQuiescentCells(unittest.TestCase):

    def setUp(self):
        self.qc1 = qc(ID=1, stage=1, pos=[0, 0], direc=random.random() * 2 * math.pi,
                      turnover=1, radius=5, area=25 * math.pi)
        self.qc2 = qc(ID=1, stage=240, pos=[0, 0], direc=random.random() * 2 * math.pi,
                      turnover=1, radius=5, area=25 * math.pi)

    def tearDown(self):
        pass

    def test_senescence(self):

        self.assertEquals(self.qc1.__class__, qc)
        self.assertEquals(self.qc2.__class__, qc)

        qc1 = qc.senescence(self.qc1)
        qc2 = qc.senescence(self.qc2)

        self.assertEquals(qc1, None)
        self.assertEquals(qc2.__class__, sc)
        self.assertEquals(qc2.radius, 5)
        self.assertEquals(qc2.area, 25*math.pi)
        self.assertEquals(qc2.pos, [0, 0])
        self.assertEquals(qc2.stage, 1)
        self.assertEquals(qc2.turnover, 1)

    def test_proliferating(self):

        qc1 = qc.proliferating(self.qc1)

        self.assertEquals(qc1.__class__, pc)
        self.assertEquals(qc1.turnover, 1)
        self.assertEquals(qc1.pos, [0, 0])
        self.assertEquals(qc1.radius, 5)
        self.assertEquals(qc1.area, 25*math.pi)
        self.assertEquals(qc1.stage, 1)

if __name__ == '__main__':
    unittest.main()
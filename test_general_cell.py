#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 12:40:52 2018

@author: Harrison Paul Cooper
"""
from quiescent_cells import qc
from senescent_cells import sc
from proliferating_cells import pc
from general_cell import general_cell
import unittest
import math
import random


class TestGeneralCell(unittest.TestCase):

    def setUp(self):
        self.general_cell1 = general_cell(ID=1, stage=1, position=[0, 0], direc=random.random() * 2 * math.pi,
                                          turnover=1, radius=5, area=25 * math.pi)

    def tearDown(self):
        pass

    def test_process_message(self):

        self.general_cell1.messages.dead = True
        self.assertEquals(self.general_cell1.dead, False)
        general_cell.process_messages(self.general_cell1)
        self.assertEquals(self.general_cell1.dead, True)

        self.general_cell1.pos = [1, 1]
        self.assertEquals(self.general_cell1.messages.pos, [0, 0])
        general_cell.process_messages(self.general_cell1)
        self.assertEquals(self.general_cell1.messages.pos, [1, 1])

    def test_move_cell(self):

        self.assertEquals(self.general_cell1.pos, [0, 0])
        general_cell.move_cell(self.general_cell1, [1, 1])
        self.assertEquals(self.general_cell1.pos, [1, 1])

    def test_kill_cell(self):

        self.assertEquals(self.general_cell1.dead, False)
        self.assertEquals(self.general_cell1.messages.dead, False)
        general_cell.kill_cell(self.general_cell1)
        self.assertEquals(self.general_cell1.dead, True)
        self.assertEquals(self.general_cell1.messages.dead, True)

    def test_apoptosis(self):
        self.general_cell1.min_radius = 4.9
        gc1 = general_cell.apoptosis(self.general_cell1)
        self.assertEquals(gc1, None)
        self.assertEquals(self.general_cell1.dead, False)
        self.general_cell1.min_radius = 10
        general_cell.apoptosis(self.general_cell1)
        self.assertEquals(self.general_cell1.dead, True)

if __name__ == '__main__':
    unittest.main()


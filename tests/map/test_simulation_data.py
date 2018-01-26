#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: xrayspectrummodeling.map.test_simulation_data
   :synopsis: Tests for the module :py:mod:`xrayspectrummodeling.map.simulation_data as simulation_data`

.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the module :py:mod:`xrayspectrummodeling.map.simulation_data as simulation_data`.
"""

###############################################################################
# Copyright 2017 Hendrix Demers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
###############################################################################

# Standard library modules.
import unittest
import os.path

# Third party modules.
from nose import SkipTest
import numpy as np

# Local modules.

# Project modules.
from xrayspectrummodeling import get_current_module_path
from xrayspectrummodeling.map.simulation_data import SimulationData
from xrayspectrummodeling.map.positions import Positions

# Globals and constants variables.


class TestSimulationData(unittest.TestCase):
    """
    TestCase class for the module `xrayspectrummodeling.map.simulation_data`.
    """

    def setUp(self):
        """
        Setup method.
        """

        unittest.TestCase.setUp(self)

        self.hdf5_file_path = get_current_module_path(__file__, "../../test_data/SimulationTestMapsMM2017.hdf5")

        if not os.path.isfile(self.hdf5_file_path):
            raise SkipTest

    def tearDown(self):
        """
        Teardown method.
        """

        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        """
        First test to check if the testcase is working with the testing framework.
        """

        # self.fail("Test if the testcase is working.")
        self.assert_(True)

    def generate_3x3_positions(self):
        position = Positions()
        position.x_pixels = 3
        position.y_pixels = 3
        position.minimum_x_nm = -5.0e3
        position.maximum_x_nm = 5.0e3
        position.minimum_y_nm = -5.0e3
        position.maximum_y_nm = 5.0e3

        return position

    def test_get_bse_map(self):
        """
        Test for method _generate.
        """
        position = self.generate_3x3_positions()

        bse_ref = np.array([[0.0651, 0.0654, 0.0659],
                            [0.0777, 0.0743, 0.0749],
                            [0.0704, 0.0696, 0.0734]])

        simulation_data = SimulationData(self.hdf5_file_path, position, None)

        bse = simulation_data.get_bse_map()
        # print(bse)

        shape = bse_ref.shape
        for i in range(shape[0]):
            for j in range(shape[1]):
                message = "(%s, %s)" % (j, i)
                self.assertAlmostEquals(bse_ref[j ,i], bse[j, i], 6, message)

        # self.fail("Test if the testcase is working.")

    def test_get_te_map(self):
        """
        Test for method get_te_map.
        """
        position = self.generate_3x3_positions()

        te_ref = np.array([[0.6784, 0.6754, 0.6734],
                           [0.6356, 0.6241, 0.6260],
                           [0.6379, 0.6391, 0.6405]])

        simulation_data = SimulationData(self.hdf5_file_path, position, None)

        te = simulation_data.get_te_map()
        # print(te)

        shape = te_ref.shape
        for i in range(shape[0]):
            for j in range(shape[1]):
                message = "(%s, %s)" % (j, i)
                self.assertAlmostEquals(te_ref[j ,i], te[j, i], 6, message)

        # self.fail("Test if the testcase is working.")

    def test_get_skirted_electron_map(self):
        """
        Test for method get_te_map.
        """
        position = self.generate_3x3_positions()

        se_ref = np.array([[0.2564, 0.2591, 0.2606],
                           [0.2866, 0.3015, 0.2990],
                           [0.2916, 0.2912, 0.2860]])

        simulation_data = SimulationData(self.hdf5_file_path, position, None)

        se = simulation_data.get_skirted_electron_map()
        # print(se)

        shape = se_ref.shape
        for i in range(shape[0]):
            for j in range(shape[1]):
                message = "(%s, %s)" % (j, i)
                self.assertAlmostEquals(se_ref[j ,i], se[j, i], 6, message)

        # self.fail("Test if the testcase is working.")

    def test_find_position_index(self):
        """
        Test for method find_position_index.
        """

        positions = self.generate_3x3_positions()

        simulation_data = SimulationData(self.hdf5_file_path, positions, None)

        position = np.array([-5.0e3, -5.0e3])
        index_x_ref = 0
        index_y_ref = 0
        index_x, index_y = simulation_data.find_position_index(positions, position)
        self.assertEquals(index_x_ref, index_x)
        self.assertEquals(index_y_ref, index_y)

        position = np.array([0.0e3, -5.0e3])
        index_x_ref = 1
        index_y_ref = 0
        index_x, index_y = simulation_data.find_position_index(positions, position)
        self.assertEquals(index_x_ref, index_x)
        self.assertEquals(index_y_ref, index_y)

        position = np.array([5.0e3, -5.0e3])
        index_x_ref = 2
        index_y_ref = 0
        index_x, index_y = simulation_data.find_position_index(positions, position)
        self.assertEquals(index_x_ref, index_x)
        self.assertEquals(index_y_ref, index_y)

        position = np.array([-5.0e3, 0.0e3])
        index_x_ref = 0
        index_y_ref = 1
        index_x, index_y = simulation_data.find_position_index(positions, position)
        self.assertEquals(index_x_ref, index_x)
        self.assertEquals(index_y_ref, index_y)

        position = np.array([0.0e3, 0.0e3])
        index_x_ref = 1
        index_y_ref = 1
        index_x, index_y = simulation_data.find_position_index(positions, position)
        self.assertEquals(index_x_ref, index_x)
        self.assertEquals(index_y_ref, index_y)

        position = np.array([5.0e3, 0.0e3])
        index_x_ref = 2
        index_y_ref = 1
        index_x, index_y = simulation_data.find_position_index(positions, position)
        self.assertEquals(index_x_ref, index_x)
        self.assertEquals(index_y_ref, index_y)

        position = np.array([-5.0e3, 5.0e3])
        index_x_ref = 0
        index_y_ref = 2
        index_x, index_y = simulation_data.find_position_index(positions, position)
        self.assertEquals(index_x_ref, index_x)
        self.assertEquals(index_y_ref, index_y)

        position = np.array([0.0e3, 5.0e3])
        index_x_ref = 1
        index_y_ref = 2
        index_x, index_y = simulation_data.find_position_index(positions, position)
        self.assertEquals(index_x_ref, index_x)
        self.assertEquals(index_y_ref, index_y)

        position = np.array([5.0e3, 5.0e3])
        index_x_ref = 2
        index_y_ref = 2
        index_x, index_y = simulation_data.find_position_index(positions, position)
        self.assertEquals(index_x_ref, index_x)
        self.assertEquals(index_y_ref, index_y)

        # self.fail("Test if the testcase is working.")


if __name__ == '__main__':  # pragma: no cover
    import nose
    nose.runmodule()

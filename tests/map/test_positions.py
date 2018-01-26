#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: mcxray.map.test_positions
   :synopsis: Tests for the module :py:mod:` positions`

.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the module :py:mod:` positions`.
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

# Third party modules.
import numpy as np

# Local modules.

# Project modules.
from xrayspectrummodeling.map.positions import Positions

# Globals and constants variables.


class TestPositions(unittest.TestCase):
    """
    TestCase class for the module ` positions`.
    """

    def setUp(self):
        """
        Setup method.
        """

        unittest.TestCase.setUp(self)

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

    def test_generate(self):
        """
        Test for method _generate.
        """

        position = Positions()
        position.x_pixels = 3
        position.y_pixels = 3
        position.minimum_x_nm = -5.0e3
        position.maximum_x_nm = 5.0e3
        position.minimum_y_nm = -5.0e3
        position.maximum_y_nm = 5.0e3

        positions = position._generate()

        positions_ref = [(-5.0e3, -5.0e3), (0.0e3, -5.0e3), (5.0e3, -5.0e3),
                        (-5.0e3, 0.0e3), (0.0e3, 0.0e3), (5.0e3, 0.0e3),
                        (-5.0e3, 5.0e3), (0.0e3, 5.0e3), (5.0e3, 5.0e3)]

        for positionRef, position in zip(positions_ref, positions):
            self.assertAlmostEqual(positionRef[0], position[0], 2)
            self.assertAlmostEqual(positionRef[1], position[1], 2)

        # self.fail("Test if the testcase is working.")

    def test_get_list(self):
        """
        Test for method _generate.
        """

        position = Positions()
        position.x_pixels = 3
        position.y_pixels = 3
        position.minimum_x_nm = -5.0e3
        position.maximum_x_nm = 5.0e3
        position.minimum_y_nm = -5.0e3
        position.maximum_y_nm = 5.0e3

        positions = position.get_list()

        positions_ref = [(-5.0e3, -5.0e3), (0.0e3, -5.0e3), (5.0e3, -5.0e3),
                        (-5.0e3, 0.0e3), (0.0e3, 0.0e3), (5.0e3, 0.0e3),
                        (-5.0e3, 5.0e3), (0.0e3, 5.0e3), (5.0e3, 5.0e3)]

        for positionRef, position in zip(positions_ref, positions):
            self.assertAlmostEqual(positionRef[0], position[0], 2)
            self.assertAlmostEqual(positionRef[1], position[1], 2)

        # self.fail("Test if the testcase is working.")

    def test_get_array(self):
        """
        Test for method _generate.
        """

        position = Positions()
        position.x_pixels = 3
        position.y_pixels = 3
        position.minimum_x_nm = -5.0e3
        position.maximum_x_nm = 5.0e3
        position.minimum_y_nm = -5.0e3
        position.maximum_y_nm = 5.0e3

        positions = position.get_array()

        positions_ref = np.array([(-5.0e3, -5.0e3), (0.0e3, -5.0e3), (5.0e3, -5.0e3),
                        (-5.0e3, 0.0e3), (0.0e3, 0.0e3), (5.0e3, 0.0e3),
                        (-5.0e3, 5.0e3), (0.0e3, 5.0e3), (5.0e3, 5.0e3)])

        shape = positions_ref.shape
        for i in range(shape[0]):
            for j in range(shape[1]):
                self.assertAlmostEqual(positions_ref[i ,j], positions[i, j], 2)

        # self.fail("Test if the testcase is working.")


if __name__ == '__main__':  # pragma: no cover
    import nose
    nose.runmodule()

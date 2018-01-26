#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: test_create_map

.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the module :py:mod:`create_map`.
"""

###############################################################################
# Copyright ${year} Hendrix Demers
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
from xrayspectrummodeling.map.create_map import change_energy_scale, change_energy_scale2


# Globals and constants variables.

class TestCreateMap(unittest.TestCase):
    """
    TestCase class for the module `${moduleName}`.
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

    def test_change_energy_scale(self):
        """
        First test to check if the testcase is working with the testing framework.
        """
        intensity_data = np.array([2.0, 4.0, 6.0, 8.0, 12.0, 0.0])
        rebinned_intensity_data_ref = [6.0, 14.0, 12.0]

        energies_keV = np.linspace(0.0, 5.0, len(intensity_data))
        energy_edges_keV = np.linspace(0.0, 5.0, int(len(intensity_data)/2) + 1)
        rebinned_intensity_data = change_energy_scale(energies_keV, intensity_data, energy_edges_keV)

        for rebinned_intensity_ref, rebinned_intensity in zip(rebinned_intensity_data_ref, rebinned_intensity_data):
            self.assertAlmostEqual(rebinned_intensity_ref, rebinned_intensity, 2)

        # self.fail("Test if the testcase is working.")

    def test_change_energy_scale2(self):
        """
        First test to check if the testcase is working with the testing framework.
        """
        intensity_data = np.array([2.0, 4.0, 6.0, 8.0, 12.0, 0.0])
        rebinned_intensity_data_ref = [6.0, 14.0, 12.0]

        energies_keV = np.linspace(0.0, 5.0, len(intensity_data))
        energy_edges_keV = np.linspace(0.0, 5.0, int(len(intensity_data)/2) + 1)
        rebinned_intensity_data = change_energy_scale2(energies_keV, intensity_data, energy_edges_keV)

        for rebinned_intensity_ref, rebinned_intensity in zip(rebinned_intensity_data_ref, rebinned_intensity_data):
            self.assertAlmostEqual(rebinned_intensity_ref, rebinned_intensity, 2)

        # self.fail("Test if the testcase is working.")


if __name__ == '__main__':  # pragma: no cover
    import nose

    nose.runmodule()

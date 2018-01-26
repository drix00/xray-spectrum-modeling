#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: mcxray.map.positions
   :synopsis: Module to _generate positions of the probe for the map.

.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Module to _generate positions of the probe for the map.
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

# Third party modules.
import numpy as np

# Local modules.

# Project modules.

# Globals and constants variables.


class Positions():
    def __init__(self):
        self.x_pixels = 0
        self.minimum_x_nm = 0.0
        self.maximum_x_nm = 0.0
        self._xs_nm = None

        self.y_pixels = 0
        self.minimum_y_nm = 0.0
        self.maximum_y_nm = 0.0
        self._ys_nm = None

    def _generate(self):
        self._xs_nm = np.linspace(self.minimum_x_nm, self.maximum_x_nm, self.x_pixels)
        self._ys_nm = np.linspace(self.minimum_y_nm, self.maximum_y_nm, self.y_pixels)
        probe_positions_nm =  np.transpose([np.tile(self.xs_nm, len(self.xs_nm)), np.repeat(self.ys_nm, len(self.ys_nm))])

        return probe_positions_nm

    def get_list(self):
        probe_positions_nm = self._generate()
        probe_positions_nm = [tuple(position_nm) for position_nm in probe_positions_nm]
        return probe_positions_nm

    def get_array(self):
        probe_positions_nm = self._generate()
        return probe_positions_nm

    @property
    def xs_nm(self):
        if self._xs_nm is None:
            self._generate()

        return self._xs_nm

    @property
    def ys_nm(self):
        if self._ys_nm is None:
            self._generate()

        return self._ys_nm

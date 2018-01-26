#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: mcxray.map.simulation_data
   :synopsis: Module to extract the simulation data from the hdf5 file.

.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Module to extract the simulation data from the hdf5 file.
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
import logging

# Third party modules.
import numpy as np
import h5py

# Local modules.
from pymcxray.mcxray import HDF5_PARAMETERS

# Project modules.

# Globals and constants variables.


class SimulationData():
    def __init__(self, hdf5_file_path, positions, symbols):
        self.hdf5_file_path = hdf5_file_path
        self.intensity_data_map = None
        self.positions = positions
        self.symbols = symbols

    def get_bse_map(self):
        result_name = "Backscattering coefficient"
        bse_map = self._get_electron_result(result_name)
        return bse_map

    def get_te_map(self):
        result_name = "Transmitted coefficient"
        te_map = self._get_electron_result(result_name)
        return te_map

    def get_skirted_electron_map(self):
        result_name = "Skirted coefficient"
        se_map = self._get_electron_result(result_name)
        return se_map

    def _get_electron_result(self, result_name):
        shape = (self.positions.x_pixels, self.positions.y_pixels)
        electron_result_map = np.zeros(shape, dtype=np.float)

        with h5py.File(self.hdf5_file_path, 'r', driver='core') as hdf5_file:

            simulations_group = hdf5_file["simulations"]

            for group in simulations_group.values():
                if not group.name.endswith(HDF5_PARAMETERS):
                    try:
                        index_x, index_y = self.find_position_index(self.positions, group.attrs["beamPosition"])
                        bse = group["ElectronResults"].attrs[result_name]
                        electron_result_map[index_y, index_x] = bse

                    except IndexError as message:
                        logging.debug(message)
                        logging.debug("%s", group.name)

        return electron_result_map

    def get_intensity_data(self, symbol):
        if self.intensity_data_map is None:
            self._extract_intensity_data()

        if symbol in self.intensity_data_map:
            return self.intensity_data_map[symbol]
        else:
            raise ValueError

    def _extract_intensity_data(self):
        self.intensity_data_map = {}

        shape = (self.positions.x_pixels, self.positions.y_pixels, 10, 9, 6)
        for symbol in self.symbols:
            self.intensity_data_map[symbol] = np.zeros(shape, dtype=np.float)

        with h5py.File(self.hdf5_file_path, 'r', driver='core') as hdf5_file:

            simulations_group = hdf5_file["simulations"]

            for group in simulations_group.values():
                if not group.name.endswith(HDF5_PARAMETERS):
                    try:
                        index_x, index_y = self.find_position_index(self.positions, group.attrs["beamPosition"])
                        for symbol in self.symbols:
                            intensity = group["Intensity"][symbol]
                            self.intensity_data_map[symbol][index_y, index_x] = intensity[...]

                    except IndexError as message:
                        logging.info(message)
                        logging.info("%s", group.name)

    def get_emitted_spectrum(self, position):
        with h5py.File(self.hdf5_file_path, 'r', driver='core') as hdf5_file:

            simulations_group = hdf5_file["simulations"]

            for group in simulations_group.values():
                if not group.name.endswith(HDF5_PARAMETERS):
                    try:
                        index_x, index_y = self.find_position_index(self.positions, group.attrs["beamPosition"])
                        energy_data = group["XraySpectraRegionsEmitted/energies_keV"][:]
                        intensity_data_1_ekeVsr = group["XraySpectraRegionsEmitted/total_1_ekeVsr"][:]

                    except IndexError as message:
                        logging.debug(message)
                        logging.debug("%s", group.name)

        return energy_data, intensity_data_1_ekeVsr

    def get_detected_spectrum(self, position):
        with h5py.File(self.hdf5_file_path, 'r', driver='core') as hdf5_file:

            simulations_group = hdf5_file["simulations"]

            for group in simulations_group.values():
                if not group.name.endswith(HDF5_PARAMETERS):
                    try:
                        index_x, index_y = self.find_position_index(self.positions, group.attrs["beamPosition"])
                        energy_data = group["XraySpectraSpecimenEmittedDetected/Energy (keV)"][:]
                        intensity_data = group["XraySpectraSpecimenEmittedDetected/Spectra Total"][:]

                    except IndexError as message:
                        logging.debug(message)
                        logging.debug("%s", group.name)

        return energy_data, intensity_data

    def find_position_index(self, positions, position):
        index_x = np.where(positions.xs_nm == position[0])[0][0]
        index_y = np.where(positions.ys_nm == position[1])[0][0]

        return index_x, index_y

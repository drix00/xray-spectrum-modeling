#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: create_test_map

.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Create map from the mcxray simulation.
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
import os
import os.path

# Third party modules.
import matplotlib.pyplot as plt
import numpy as np

# Local modules.

# Project modules.
from xrayspectrummodeling.map.positions import Positions
from xrayspectrummodeling.map.create_map import _create_electron_maps, _create_intensity_maps, _create_spectra, \
    _create_spectra_maps, _export_raw_map

# Globals and constants variables.


def run_maps(data_path):
    hdf5_file_path = os.path.join(data_path, "SimulationTestMapsMM2017.hdf5")
    hdf5_file_out_path = os.path.join(data_path, "map_mm2017_abstract_3x3.hdf5")

    figure_path = os.path.join(data_path, "figures")
    if not os.path.isdir(figure_path):
        os.makedirs(figure_path)

    position = Positions()
    position.x_pixels = 3
    position.y_pixels = 3
    position.minimum_x_nm = -5.0e3
    position.maximum_x_nm = 5.0e3
    position.minimum_y_nm = -5.0e3
    position.maximum_y_nm = 5.0e3

    # _create_electron_maps(data_path, hdf5_file_path, position)

    # _create_intensity_maps(data_path, hdf5_file_path, position)

    # _create_spectra(data_path, hdf5_file_path, position)

    _create_spectra_maps(data_path, hdf5_file_path, hdf5_file_out_path, position)

    _export_raw_map(hdf5_file_out_path)

    file_path = hdf5_file_out_path[:-5] + "_" + "map_100000_us" + ".raw"
    _read_raw_map(file_path)


def _read_raw_map(file_path):
    from pySpectrumFileFormat.Bruker.MapRaw.MapRawFormat import MapRawFormat

    map_raw = MapRawFormat(file_path)

    channels, datacube = map_raw.getDataCube()
    print(datacube.shape)

    plt.figure()
    plt.title("All regions")
    plt.semilogy(channels, datacube.sum(axis=(0,1)))

    plt.figure()
    plt.plot(channels, datacube[1,1,:])
    plt.close()

    x_data, y_data = map_raw.getSpectrum(1, 1)

    plt.figure()
    plt.semilogy(x_data, y_data)
    # plt.close()

    x_data, y_data = map_raw.getSumSpectrum()

    plt.figure()
    plt.plot(x_data, y_data)
    plt.close()

    image = map_raw.getTotalIntensityImage()
    plt.figure()
    plt.imshow(image, cmap="gray")
    plt.close()

    roi = (225, 235)
    image = map_raw.getRoiIntensityImage(roi)
    plt.figure()
    plt.imshow(image, cmap="gray")
    plt.close()

    plt.figure()
    plt.plot(x_data, np.linspace(0.0, 30.0, len(x_data)))
    plt.close()


if __name__ == '__main__':
    import sys

    logging.getLogger().setLevel(logging.INFO)

    if len(sys.argv) > 1:
        data_path = sys.argv[1]
    else:
        data_path = r"C:\hdemers\coding\github\xray-spectrum-modeling\test_data"

    logging.debug(sys.argv)
    logging.info(data_path)

    run_maps(data_path)

    logging.info("Done")
    plt.show()

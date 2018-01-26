#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: create_map_mm2017_abstract

.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Create map from the mcxray simulation for MM2017 abstract.
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


def run_map_mm2017_abstract(data_path):
    hdf5_file_path = os.path.join(data_path, "SimulationMapsMM2017.hdf5")
    hdf5_file_out_path = os.path.join(data_path, "map_mm2017_abstract_128x128.hdf5")

    position = Positions()
    position.x_pixels = 128
    position.y_pixels = 128
    position.minimum_x_nm = -5.0e3
    position.maximum_x_nm = 5.0e3
    position.minimum_y_nm = -5.0e3
    position.maximum_y_nm = 5.0e3

    _create_electron_maps(data_path, hdf5_file_path, position)

    _create_intensity_maps(data_path, hdf5_file_path, position)

    _create_spectra(data_path, hdf5_file_path, position)

    _create_spectra_maps(data_path, hdf5_file_path, hdf5_file_out_path, position)

    _export_raw_map(hdf5_file_out_path)

    file_path = hdf5_file_out_path[:-5] + "_" + "map_5000_us" + ".raw"
    _read_raw_map(file_path)


def _read_raw_map(file_path):
    from pySpectrumFileFormat.Bruker.MapRaw.MapRawFormat import MapRawFormat

    mapRaw = MapRawFormat(file_path)

    channels, datacube = mapRaw.getDataCube()
    print(datacube.shape)

    plt.figure()
    plt.title("All regions for 1 s")
    plt.semilogy(channels, datacube.sum(axis=(0,1)))

    plt.figure()
    plt.plot(channels, datacube[1,1,:])
    plt.close()

    xData, yData = mapRaw.getSpectrum(1, 1)

    plt.figure()
    plt.title("One spectrum for 1 s")
    plt.semilogy(xData, yData)
    # plt.close()

    xData, yData = mapRaw.getSumSpectrum()
    plt.figure()
    plt.title("Sum spectrum")
    plt.plot(xData, yData)
    # plt.close()

    image = mapRaw.getTotalIntensityImage()
    plt.figure()
    plt.title("Total intensity")
    plt.imshow(image, cmap="gray")
    # plt.close()

    roi = (225, 235)
    image = mapRaw.getRoiIntensityImage(roi)
    plt.figure()
    plt.title("Co intensity")
    plt.imshow(image, cmap="gray")
    # plt.close()

    plt.figure()
    plt.plot(xData, np.linspace(0.0, 30.0, len(xData)))
    plt.close()


if __name__ == '__main__':
    import sys

    logging.getLogger().setLevel(logging.INFO)

    if len(sys.argv) > 1:
        data_path = sys.argv[1]
    else:
        data_path = r"D:\work\Dropbox\hdemers\professional\results\simulations\mcxray\SimulationMapsMM2017\analyzes"

    logging.debug(sys.argv)
    logging.info(data_path)

    run_map_mm2017_abstract(data_path)

    logging.info("Done")
    plt.show()

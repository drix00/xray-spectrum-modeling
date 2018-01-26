#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: create_map
   :synopsis: Create map from the mcxray simulation.

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
import math
import os.path

# Third party modules.
import h5py
import matplotlib.pyplot as plt
from scipy.constants import e
from numpy.random import normal, poisson
import numpy as np

# Local modules.
from pymcxray.mcxray import HDF5_PARAMETERS

# Project modules.
from xrayspectrummodeling.map.simulation_data import SimulationData
from xrayspectrummodeling import get_current_module_path

# Globals and constants variables.
MAP_WIDTH = "width"
MAP_HEIGHT = "height"
MAP_DEPTH = "depth"
MAP_DATA_TYPE = "data type"
MAP_PIXEL_TIME_s = "pixel time (s)"
MAP_CURRENT_nA = "current nA"
MAP_NOMINAL_NUMBER_ELECTRONS = "nominal number electrons"
MAP_SOLID_ANGLE_rad = "solid angle (rad)"
MAP_DETECTOR_NOISE_eV = "detector noise (eV)"
MAP_DETECTOR_RESOLUTION_AT_MN_eV = "detector resolution at Mn Ka (eV)"
MAP_COMMENTS = "comments"

MAP_DATA_WIDTH_nm = "widths (nm)"
MAP_DATA_HEIGHT_nm = "heights (nm)"
MAP_DATA_DEPTH_keV = "energies (keV)"


class DetectorFunction(object):
    def __init__(self, electronic_noise_eV, fano_factor=0.125):
        self._electronic_noise_eV = electronic_noise_eV
        self._fano_factor = fano_factor
        self._electron_hole_pair_eV = 3.8
        self._numeric_factor = 2.0 * math.sqrt(2.0 * math.log(2.0))

    def getFwhm_eV(self, xrayEnergy_eV):
        term1 = self._electronic_noise_eV ** 2
        term2 = self._numeric_factor * self._numeric_factor * self._electron_hole_pair_eV * self._fano_factor * xrayEnergy_eV
        fwhm_eV = math.sqrt(term1 + term2)

        return fwhm_eV

    def get_fwhms_eV(self, xray_energies_eV):
        term1 = self._electronic_noise_eV ** 2
        term2 = self._numeric_factor * self._numeric_factor * self._electron_hole_pair_eV * self._fano_factor * xray_energies_eV
        fwhms_eV = np.sqrt(term1 + term2)

        return fwhms_eV

    def getSigma_keV(self, xrayEnergy_keV):
        xrayEnergy_eV = xrayEnergy_keV*1.0e3
        fwhm_eV = self.getFwhm_eV(xrayEnergy_eV)
        fwhm_keV = fwhm_eV/1.0e3

        sigma_keV = fwhm_keV/self._numeric_factor

        return sigma_keV

    def get_sigmas_keV(self, xray_energies_keV):
        xray_energies_eV = xray_energies_keV*1.0e3
        fwhms_eV = self.get_fwhms_eV(xray_energies_eV)
        fwhms_keV = fwhms_eV/1.0e3

        sigmas_keV = fwhms_keV/self._numeric_factor

        return sigmas_keV

    def getElectronicNoise_eV(self):
        return self._electronic_noise_eV


def get_efficiency():
    file_path = get_current_module_path(__file__,  r"../../data/mcxray_XrayDetectorEfficiency.csv")
    data = np.loadtxt(file_path, float, delimiter=',',)

    return data


def create_test_map(data_path, figure=True):
    compositions = {1: "Fe-1wt%Co", 2: "Fe-2wt%Co", 3: "Fe-5wt%Co",
                    4: "Co-1wt%Ni", 5: "Co-2wt%Ni", 6: "Co-5wt%Ni",
                    7: "Fe-1wt%Co-49.5Ni", 8: "Fe-2wt%Co-49.0Ni", 9: "Fe-5wt%Co-47.5Ni"}

    width = 3
    height = 3
    depth = 1024
    data_type = np.int32
    current_nA = 1.0
    solid_angle_rad = 0.00140035
    detector_noise_eV = 50

    efficiency = get_efficiency()

    xs_nm = np.linspace(-5.0e3, 5.0e3, width)

    hdf5_file_path = os.path.join(data_path, r"SimulationMapsMM2017_3x3.hdf5")
    print(hdf5_file_path)
    with h5py.File(hdf5_file_path, 'r', driver='core') as hdf5_file:
        simulations_group = hdf5_file["simulations"]
        print(simulations_group.name)

        times_s = [0.05, 0.1, 0.5, 1.0, 5.0, 10.0]

        hdf5_file_out_path = os.path.join(data_path, r"test_maps.hdf5")
        with h5py.File(hdf5_file_out_path, 'w', driver='core') as hdf5_file:
            maps_group = hdf5_file.require_group("maps")

            for time_s in times_s:
                _create_map(compositions, current_nA, data_type, depth, detector_noise_eV, efficiency, figure,
                            hdf5_file_out_path, height, maps_group, simulations_group, solid_angle_rad, time_s, width,
                            xs_nm)


def create_map_mm2017_abstract(data_path, figure=False):
    compositions = {1: "Fe-1wt%Co", 2: "Fe-2wt%Co", 3: "Fe-5wt%Co",
                    4: "Co-1wt%Ni", 5: "Co-2wt%Ni", 6: "Co-5wt%Ni",
                    7: "Fe-1wt%Co-49.5Ni", 8: "Fe-2wt%Co-49.0Ni", 9: "Fe-5wt%Co-47.5Ni"}

    width = 128
    height = 128
    depth = 1024
    data_type = np.int32
    current_nA = 1.0
    solid_angle_rad = 0.00140035
    detector_noise_eV = 50

    efficiency = get_efficiency()

    xs_nm = np.linspace(-5.0e3, 5.0e3, width)

    hdf5_file_path = os.path.join(data_path, r"SimulationMapsMM2017.hdf5")
    with h5py.File(hdf5_file_path, 'r', driver='core') as hdf5_file:
        simulations_group = hdf5_file["simulations"]

        times_s = [0.05, 0.1, 0.5, 1.0, 5.0, 10.0]

        hdf5_file_out_path = os.path.join(data_path, r"map_mm2017_abstract.hdf5")
        with h5py.File(hdf5_file_out_path, 'w', driver='core') as hdf5_file:
            maps_group = hdf5_file.require_group("maps")

            for time_s in times_s:
                _create_map(compositions, current_nA, data_type, depth, detector_noise_eV, efficiency, figure,
                            hdf5_file_out_path, height, maps_group, simulations_group, solid_angle_rad, time_s, width,
                            xs_nm)


def export_raw_test_map(data_path):
    from pySpectrumFileFormat.Bruker.MapRaw.ParametersFile import ParametersFile, BYTE_ORDER_LITTLE_ENDIAN, RECORED_BY_VECTOR, DATA_TYPE_SIGNED

    hdf5_file_out_path = os.path.join(data_path, r"analyzes\test_maps.hdf5")
    with h5py.File(hdf5_file_out_path, 'r', driver='core') as hdf5_file:
        maps_group = hdf5_file["maps"]

        for name, group in maps_group.items():
            if str(group.name).startswith("/maps/map"):
                map_data_set = group
                logging.info(group.name)
                logging.info(name)
                parameters_file = ParametersFile()
                parameters_file.width = map_data_set.attrs[MAP_WIDTH]
                parameters_file.height = map_data_set.attrs[MAP_HEIGHT]
                parameters_file.depth = map_data_set.attrs[MAP_DEPTH]
                parameters_file.offset = 0
                parameters_file.dataLength_B = 4
                parameters_file.dataType = DATA_TYPE_SIGNED
                parameters_file.byteOrder = BYTE_ORDER_LITTLE_ENDIAN
                parameters_file.recordBy = RECORED_BY_VECTOR
                parameters_file.energy_keV = 30.0
                parameters_file.pixel_size_nm = 0.0

                base_file_out_path = hdf5_file_out_path[:-5] + "_" + name.replace(' ', '_')
                parameters_file.write(base_file_out_path + ".rpl")

                shape = (parameters_file.height, parameters_file.width, parameters_file.depth)
                fp = np.memmap(base_file_out_path + ".raw", dtype=np.int32, mode='w+', shape=shape)
                fp[:] = map_data_set[:]
                del fp


def read_raw_test_map(data_path):
    from pySpectrumFileFormat.Bruker.MapRaw.MapRawFormat import MapRawFormat

    file_path = os.path.join(data_path, r"test_maps_map_1000000_us.raw")
    map_raw = MapRawFormat(file_path)

    channels, datacube = map_raw.getDataCube()
    plt.figure()
    plt.plot(channels, datacube[1,1,:])

    x_data, y_data = map_raw.getSpectrum(1, 1)

    plt.figure()
    plt.plot(x_data, y_data)

    x_data, y_data = map_raw.getSumSpectrum()

    plt.figure()
    plt.plot(x_data, y_data)

    image = map_raw.getTotalIntensityImage()
    plt.figure()
    plt.imshow(image, cmap="gray")

    roi = (210, 225)
    image = map_raw.getRoiIntensityImage(roi)
    plt.figure()
    plt.imshow(image, cmap="gray")


def export_raw_map_mm2017_abstract(data_path):
    from pySpectrumFileFormat.Bruker.MapRaw.ParametersFile import ParametersFile, BYTE_ORDER_LITTLE_ENDIAN, RECORED_BY_VECTOR, DATA_TYPE_SIGNED

    hdf5_file_out_path = os.path.join(data_path, r"map_mm2017_abstract.hdf5")
    with h5py.File(hdf5_file_out_path, 'r', driver='core') as hdf5_file:
        maps_group = hdf5_file["maps"]

        for name, group in maps_group.items():
            if str(group.name).startswith("/maps/map"):
                map_data_set = group
                logging.info(group.name)
                logging.info(name)
                parameters_file = ParametersFile()
                parameters_file.width = map_data_set.attrs[MAP_WIDTH]
                parameters_file.height = map_data_set.attrs[MAP_HEIGHT]
                parameters_file.depth = map_data_set.attrs[MAP_DEPTH]
                parameters_file.offset = 0
                parameters_file.dataLength_B = 4
                parameters_file.dataType = DATA_TYPE_SIGNED
                parameters_file.byteOrder = BYTE_ORDER_LITTLE_ENDIAN
                parameters_file.recordBy = RECORED_BY_VECTOR
                parameters_file.energy_keV = 30.0
                parameters_file.pixel_size_nm = 0.0

                base_file_out_path = hdf5_file_out_path[:-5] + "_" + name.replace(' ', '_')
                parameters_file.write(base_file_out_path + ".rpl")

                shape = (parameters_file.height, parameters_file.width, parameters_file.depth)
                fp = np.memmap(base_file_out_path + ".raw", dtype=np.int32, mode='w+', shape=shape)
                fp[:] = map_data_set[:]
                del fp


def read_raw_map_mm2017_abstract(data_path):
    from pySpectrumFileFormat.Bruker.MapRaw.MapRawFormat import MapRawFormat

    file_path = os.path.join(data_path, r"map_mm2017_abstract_map_10000000_us.raw")
    map_raw = MapRawFormat(file_path)

    channels, datacube = map_raw.getDataCube()
    print(datacube.shape)

    plt.figure()
    plt.title("All regions")
    plt.semilogy(channels, datacube.sum(axis=(0,1)))

    plt.figure()
    plt.title("Region 1")
    plt.semilogy(channels, datacube[0:32, 0:32, :].sum(axis=(0,1)))

    plt.figure()
    plt.title("Region 2")
    plt.semilogy(channels, datacube[32:32*3, 0:32, :].sum(axis=(0,1)))

    plt.figure()
    plt.title("Region 3")
    plt.semilogy(channels, datacube[32*3:, 0:32, :].sum(axis=(0,1)))

    plt.figure()
    plt.plot(channels, datacube[1,1,:])
    plt.close()

    x_data, y_data = map_raw.getSpectrum(1, 1)

    plt.figure()
    plt.plot(x_data, y_data)
    plt.close()

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


def bse_image_mm2017(data_path):
    hdf5_file_path = os.path.join(data_path, r"SimulationMapsMM2017.hdf5")
    with h5py.File(hdf5_file_path, 'r', driver='core') as hdf5_file:

        simulations_group = hdf5_file["simulations"]

        width = 128
        height = width
        data_type = np.float

        xs_nm = np.linspace(-5.0e3, 5.0e3, width)

        shape = (height, width)
        data = np.zeros(shape, dtype=data_type)

        for group in simulations_group.values():
            try:
                index_x = np.where(xs_nm == group.attrs["beamPosition"][0])[0][0]
                index_y = np.where(xs_nm == group.attrs["beamPosition"][1])[0][0]

                bse = group["ElectronResults"].attrs["Backscattering coefficient"]
                data[index_y, index_x] = bse
            except IndexError as message:
                logging.error(message)
                logging.info(group.name)

        plt.figure()
        plt.imshow(data, cmap='gray')
        plt.xticks([])
        plt.yticks([])

        figure_file_path = os.path.join(data_path, "bse_image.png")
        plt.savefig(figure_file_path)
        # plt.close()


def _create_electron_maps(data_path, hdf5_file_path, positions):
    symbols = ['Fe', 'Co', 'Ni']
    simulation_data = SimulationData(hdf5_file_path, positions, symbols)

    # BSE map
    bse_map = simulation_data.get_bse_map()
    plt.figure()
    plt.imshow(bse_map, cmap='gray')
    plt.xticks([])
    plt.yticks([])
    figure_file_path = os.path.join(data_path, "figures", "bse_image.png")
    plt.savefig(figure_file_path)
    # plt.close()

    # TE map
    te_map = simulation_data.get_te_map()
    plt.figure()
    plt.imshow(te_map, cmap='gray')
    plt.xticks([])
    plt.yticks([])
    figure_file_path = os.path.join(data_path, "figures", "te_image.png")
    plt.savefig(figure_file_path)
    plt.close()

    # skirted electron map
    se_map = simulation_data.get_skirted_electron_map()
    plt.figure()
    plt.imshow(se_map, cmap='gray')
    plt.xticks([])
    plt.yticks([])
    figure_file_path = os.path.join(data_path, "figures", "se_image.png")
    plt.savefig(figure_file_path)
    plt.close()

    # TE corrected map
    te_map = simulation_data.get_te_map()
    plt.figure()
    plt.imshow(te_map+se_map, cmap='gray')
    plt.xticks([])
    plt.yticks([])
    figure_file_path = os.path.join(data_path, "figures", "transmitted_electron_image.png")
    plt.savefig(figure_file_path)
    # plt.close()


def _create_intensity_maps(data_path, hdf5_file_path, positions):
    symbols = ['Fe', 'Co']
    simulation_data = SimulationData(hdf5_file_path, positions, symbols)

    intensity_data = {}
    for symbol in symbols:
        intensity_data[symbol] = simulation_data.get_intensity_data(symbol)

        # Ka map
        intensity_map = np.sum(intensity_data[symbol][:, :, :, 0:1, 1], axis=(2,3))
        logging.debug(intensity_data[symbol].shape)
        logging.debug(intensity_map.shape)
        try:
            plt.figure()
            plt.title("{} Ka generated".format(symbol))
            plt.imshow(intensity_map, cmap='gray')
            plt.colorbar()
            plt.xticks([])
            plt.yticks([])
            figure_file_path = os.path.join(data_path, "figures", "intensity_{}_ka_generated_image.png".format(symbol))
            plt.savefig(figure_file_path)
            plt.close()
        except ValueError as message:
            logging.error(message)
            logging.info(symbol)

        intensity_map = np.sum(intensity_data[symbol][:, :, :, 0:1, 3], axis=(2, 3))
        logging.info(intensity_data[symbol].shape)
        logging.info(intensity_map.shape)
        try:
            plt.figure()
            plt.title("{} Ka emitted".format(symbol))
            plt.imshow(intensity_map, cmap='gray')
            plt.colorbar()
            plt.xticks([])
            plt.yticks([])
            figure_file_path = os.path.join(data_path, "figures", "intensity_{}_ka_emitted_image.png".format(symbol))
            plt.savefig(figure_file_path)
            plt.close()
        except ValueError as message:
            logging.error(message)
            logging.info(symbol)

    intensity_data = {}
    for symbol in symbols:
        intensity_data[symbol] = simulation_data.get_intensity_data(symbol)

    for symbol in symbols:
        # Ka f-ratio map
        intensity_element_map = np.sum(intensity_data[symbol][:, :, :, 0:1, 3], axis=(2, 3))

        intensity_total_map = np.zeros_like(intensity_element_map)
        for symbol_total in symbols:
            intensity_total_map += np.sum(intensity_data[symbol_total][:, :, :, 0:1, 3], axis=(2, 3))

        fratio_element_map = intensity_element_map / intensity_total_map

        try:
            plt.figure()
            plt.title("{} Ka emitted".format(symbol))
            # plt.imshow(fratio_element_map, cmap='gray', norm=colors.LogNorm(vmin=0.001, vmax=1.0))
            plt.imshow(fratio_element_map, cmap='gray', vmin=0.0, vmax=1.0)
            plt.colorbar()
            plt.xticks([])
            plt.yticks([])
            figure_file_path = os.path.join(data_path, "figures", "fratio_{}_ka_emitted_image.png".format(symbol))
            plt.savefig(figure_file_path)
            # plt.close()
        except ValueError as message:
            logging.error(message)
            logging.info(symbol)


def _create_spectra(data_path, hdf5_file_path, positions):
    symbols = ['Fe', 'Co', 'Ni']
    simulation_data = SimulationData(hdf5_file_path, positions, symbols)

    for position in positions.get_list()[0:1]:
        energies_keV, spectrum = simulation_data.get_emitted_spectrum(position)
        plt.figure()
        title = "{0} ({1}, {2})".format("Emitted", position[0], position[1])
        plt.title(title)
        plt.semilogy(energies_keV, spectrum)
        plt.xlabel("Energy (keV)")
        plt.ylabel("Intensity (1/keV/e-/sr)")
        file_name = "{0}_{1}_{2}.png".format("Spectrum_Emitted", position[0], position[1])
        figure_file_path = os.path.join(data_path, "figures", file_name)
        plt.savefig(figure_file_path)
        plt.close()

        energies_keV, spectrum = simulation_data.get_detected_spectrum(position)
        plt.figure()
        title = "{0} ({1}, {2})".format("Detected", position[0], position[1])
        plt.title(title)
        plt.semilogy(energies_keV, spectrum)
        plt.xlabel("Energy (keV)")
        plt.ylabel("Intensity (photons)")
        plt.ylim(ymin=1)
        file_name = "{0}_{1}_{2}.png".format("Spectrum_Detected", position[0], position[1])
        figure_file_path = os.path.join(data_path, "figures", file_name)
        plt.savefig(figure_file_path)
        plt.close()

        # Calculated detected
        current_nA = 1.0
        solid_angle_rad = 0.00140035
        detector_noise_eV = 50
        efficiency = get_efficiency()
        time_s = 100.0
        depth = 128

        nominal_number_electrons, number_electrons = _compute_number_electrons(current_nA, time_s)
        logging.debug("{} {}".format(nominal_number_electrons, number_electrons))

        energy_data, intensity_data_1_ekeVsr = simulation_data.get_emitted_spectrum(position)
        intensity_efficiency_data_1_ekeVsr = intensity_data_1_ekeVsr * np.interp(energy_data, efficiency[:, 0],
                                                                                 efficiency[:, 1])
        plt.figure()
        title = "{} ({}, {})".format("Emitted * efficiency", position[0], position[1])
        plt.title(title)
        plt.semilogy(energy_data, intensity_data_1_ekeVsr, '.')
        plt.semilogy(energy_data, intensity_efficiency_data_1_ekeVsr, '.')
        plt.xlabel("Energy (keV)")
        plt.ylabel("Intensity (1/keV/e-/sr)")
        file_name = "{0}_{1}_{2}.png".format("Spectrum_Emitted_Efficiency", position[0], position[1])
        figure_file_path = os.path.join(data_path, "figures", file_name)
        plt.savefig(figure_file_path)
        plt.close()

        delta_energy_keV = energy_data[1] - energy_data[0]
        intensity_data = intensity_efficiency_data_1_ekeVsr * number_electrons * solid_angle_rad * delta_energy_keV

        plt.figure()
        title = "{} ({}, {}), t = {} s".format("Emitted counts", position[0], position[1], time_s)
        plt.title(title)
        plt.semilogy(energy_data, intensity_data, '.')
        plt.xlabel("Energy (keV)")
        plt.ylabel("Intensity (photons)")
        plt.ylim(ymin=1)
        file_name = "{}_{}_{}_t{}s.png".format("Spectrum_Emitted_Counts", position[0], position[1], time_s)
        figure_file_path = os.path.join(data_path, "figures", file_name)
        plt.savefig(figure_file_path)
        plt.close()

        energy_edges_keV = np.linspace(0.0, 30.0, depth + 1)
        energies_keV = np.linspace(0.0, 30.0, depth)
        counts_data = change_energy_scale2(energy_data, intensity_data, energy_edges_keV)

        plt.figure()
        title = "{} ({}, {}), t = {} s".format("Emitted counts", position[0], position[1], time_s)
        plt.title(title)
        plt.semilogy(energy_data, intensity_data, '-')
        plt.semilogy(energies_keV, counts_data, '.')
        plt.xlabel("Energy (keV)")
        plt.ylabel("Intensity (photons)")
        plt.ylim(ymin=1)
        file_name = "{}_{}_{}_t{}s.png".format("Spectrum_Emitted_Counts", position[0], position[1], time_s)
        figure_file_path = os.path.join(data_path, "figures", file_name)
        plt.savefig(figure_file_path)
        # plt.close()

        detector = DetectorFunction(detector_noise_eV)
        sigmas_keV = detector.get_sigmas_keV(energies_keV)
        fwhms_eV = detector.get_fwhms_eV(energies_keV*1.0e3)
        plt.figure()
        plt.title("Detector")
        plt.plot(energies_keV, sigmas_keV)
        plt.plot(energies_keV, fwhms_eV/1.0e3)
        plt.xlabel("Energy (keV)")
        plt.ylabel("Sigma (keV)")
        # plt.ylim(ymin=1)
        file_name = "{}_{}_{}_t{}s.png".format("Detector", position[0], position[1], time_s)
        figure_file_path = os.path.join(data_path, "figures", file_name)
        plt.savefig(figure_file_path)
        plt.close()

        plt.figure()
        title = "{} ({}, {}), t = {} s".format("Detected", position[0], position[1], time_s)
        plt.title(title)

        mean_intensity = np.zeros_like(energies_keV)
        number_repetitions = 50
        for repetition in range(number_repetitions):
            xrays = _compute_xrays(detector_noise_eV, energies_keV, counts_data)

            counts, _bin_edges = np.histogram(xrays, bins=energy_edges_keV)
            mean_intensity += counts
            # plt.semilogy(energies_keV, counts, label=repetition)
            logging.debug("{:d} {:d} {:d}".format(int(np.sum(counts_data)), len(xrays), int(np.sum(counts_data)-len(xrays))))
            logging.debug("{:d} {:d} {:d}".format(len(xrays), int(np.sum(counts)) , len(xrays) - int(np.sum(counts))))

        mean_intensity /= number_repetitions
        plt.semilogy(energies_keV, counts_data)
        plt.semilogy(energies_keV, mean_intensity)

        plt.xlabel("Energy (keV)")
        plt.ylabel("Intensity (photons)")
        plt.ylim(ymin=1)
        # plt.legend()
        file_name = "{}_{}_{}_t{}s.png".format("Spectrum_Detected", position[0], position[1], time_s)
        figure_file_path = os.path.join(data_path, "figures", file_name)
        plt.savefig(figure_file_path)
        # plt.close()


def compute_histogram(energy_data, intensity_data, energy_edges_keV):
    xrays = []
    for energy_keV, intensity in zip(energy_data, intensity_data):
        xrays.extend(np.full((int(round(intensity))), energy_keV).tolist())

    counts_data, _bin_edges = np.histogram(xrays, bins=energy_edges_keV)
    logging.info("{:d} {:d} {:d}".format(int(np.sum(intensity_data)), len(xrays), int(np.sum(intensity_data) - len(xrays))))

    return counts_data


def change_energy_scale(energy_data, intensity_data, energy_edges_keV):
    counts_data = np.zeros((len(energy_edges_keV)-1), dtype=np.float)

    for energy_keV, intensity in zip(energy_data, intensity_data):
        for i in range(len(energy_edges_keV)-1):
            if energy_keV >= energy_edges_keV[i] and energy_keV < energy_edges_keV[i+1]:
                counts_data[i] += intensity

    return counts_data


def change_energy_scale2(energy_data, intensity_data, energy_edges_keV):
    counts_data = np.zeros((len(energy_edges_keV)-1), dtype=np.float)

    for energy_keV, intensity in zip(energy_data[:-1], intensity_data[:-1]):
        i = np.searchsorted(energy_edges_keV, energy_keV, side="right")-1
        counts_data[i] += intensity

    return counts_data


def _create_spectra_maps(data_path, hdf5_file_path, hdf5_file_out_path, positions):
    logging.info("_create_spectra_maps")

    depth = 1024
    data_type = np.int32
    current_nA = 1.0
    solid_angle_rad = 0.00140035
    detector_noise_eV = 50

    efficiency = get_efficiency()

    with h5py.File(hdf5_file_path, 'r', driver='core') as hdf5_file:
        simulations_group = hdf5_file["simulations"]

        times_s = [0.005, 0.01, 0.05, 0.1, 0.5, 1.0, 5.0, 10.0, 50.0, 100.0, 500.0, 1000.0]
        times_s = [0.1]

        with h5py.File(hdf5_file_out_path, 'a', driver='core') as hdf5_file:
            maps_group = hdf5_file.require_group("maps")

            for time_s in times_s:
                _create_map(current_nA, data_type, depth, detector_noise_eV, efficiency, maps_group,
                            simulations_group, solid_angle_rad, time_s, positions)


def _create_map(current_nA, data_type, depth, detector_noise_eV, efficiency, maps_group, simulations_group,
                solid_angle_rad, time_s, positions):
    logging.info("_create_map {}".format(time_s))

    time_us = time_s * 1.0e6
    map_name = "map %i us" % (time_us)
    if map_name in maps_group:
        logging.info("Map already exist skip it: {}".format(map_name))
        return

    shape = (positions.y_pixels, positions.x_pixels, depth)
    data = np.zeros(shape, dtype=data_type)

    for group in simulations_group.values():
        if not group.name.endswith(HDF5_PARAMETERS):
            try:
                index_x = np.where(positions.xs_nm == group.attrs["beamPosition"][0])[0][0]
                index_y = np.where(positions.ys_nm == group.attrs["beamPosition"][1])[0][0]

                nominal_number_electrons, number_electrons = _compute_number_electrons(current_nA, time_s)

                delta_energy_keV, energy_data, intensity_data = _compute_intensity(efficiency, group, number_electrons,
                                                                                   solid_angle_rad, depth)
                xrays = _compute_xrays(detector_noise_eV, energy_data, intensity_data)

                counts, energies_keV = _compute_counts(data, depth, index_x, index_y, xrays)
            except IndexError:
                pass

    _write_map(current_nA, data, data_type, depth, detector_noise_eV, energies_keV, maps_group,
               nominal_number_electrons, shape, solid_angle_rad, time_s, positions)


def _write_map(current_nA, data, data_type, depth, detector_noise_eV, energies_keV, maps_group,
               nominal_number_electrons, shape, solid_angle_rad, time_s, positions):
    logging.info("_write_map {}".format(time_s))

    detector = DetectorFunction(detector_noise_eV)
    time_us = time_s * 1.0e6
    map_name = "map {} us".format(time_us)
    map_data_set = maps_group.require_dataset(map_name, shape, dtype=data_type)
    map_data_set[...] = data
    map_data_set.attrs[MAP_WIDTH] = positions.x_pixels
    map_data_set.attrs[MAP_HEIGHT] = positions.y_pixels
    map_data_set.attrs[MAP_DEPTH] = depth
    map_data_set.attrs[MAP_DATA_TYPE] = str(data_type)
    map_data_set.attrs[MAP_PIXEL_TIME_s] = time_s
    map_data_set.attrs[MAP_CURRENT_nA] = current_nA
    map_data_set.attrs[MAP_NOMINAL_NUMBER_ELECTRONS] = nominal_number_electrons
    map_data_set.attrs[MAP_SOLID_ANGLE_rad] = solid_angle_rad
    map_data_set.attrs[MAP_DETECTOR_NOISE_eV] = detector_noise_eV
    map_data_set.attrs[MAP_DETECTOR_RESOLUTION_AT_MN_eV] = detector.getFwhm_eV(5898.0)
    map_data_set.attrs[MAP_COMMENTS] = "data[X, Y, D]"
    width_data_set = maps_group.require_dataset(MAP_DATA_WIDTH_nm, (positions.x_pixels,), dtype=np.float)
    width_data_set[...] = positions.xs_nm
    height_data_set = maps_group.require_dataset(MAP_DATA_HEIGHT_nm, (positions.y_pixels,), dtype=np.float)
    height_data_set[...] = positions.ys_nm
    depth_data_set = maps_group.require_dataset(MAP_DATA_DEPTH_keV, (depth,), dtype=np.float)
    depth_data_set[...] = energies_keV
    map_data_set.dims.create_scale(width_data_set, "X (nm)")
    map_data_set.dims.create_scale(height_data_set, "Y (nm)")
    map_data_set.dims.create_scale(depth_data_set, "Energies (keV)")
    map_data_set.dims[0].attach_scale(width_data_set)
    map_data_set.dims[1].attach_scale(height_data_set)
    map_data_set.dims[2].attach_scale(depth_data_set)


def _compute_counts(data, depth, index_x, index_y, xrays):
    energy_edges_keV = np.linspace(0.0, 30.0, depth + 1)
    energies_keV = np.linspace(0.0, 30.0, depth)
    counts, _bin_edges = np.histogram(xrays, bins=energy_edges_keV)
    data[index_y, index_x, :] = counts
    return counts, energies_keV


def _compute_xrays(detector_noise_eV, energy_data, intensity_data):
    detector = DetectorFunction(detector_noise_eV)
    sigmas_keV = detector.get_sigmas_keV(energy_data)
    xrays = []
    for channel in range(len(energy_data)):
        nominal_number_xrays = intensity_data[channel]
        number_xrays = poisson(nominal_number_xrays)
        number_xrays = int(round(number_xrays))
        counts = normal(energy_data[channel], sigmas_keV[channel], size=number_xrays)
        xrays.extend(counts.tolist())

    return xrays


def _compute_intensity(efficiency, group, number_electrons, solid_angle_rad, depth):
    energy_data = group["XraySpectraRegionsEmitted/energies_keV"][:]
    intensity_data_1_ekeVsr = group["XraySpectraRegionsEmitted/total_1_ekeVsr"][:]
    intensity_data_1_ekeVsr *= np.interp(energy_data, efficiency[:, 0], efficiency[:, 1])
    delta_energy_keV = energy_data[1] - energy_data[0]
    intensity_data = intensity_data_1_ekeVsr * number_electrons * solid_angle_rad * delta_energy_keV

    energy_edges_keV = np.linspace(0.0, 30.0, depth + 1)
    energies_keV = np.linspace(0.0, 30.0, depth)
    counts_data = change_energy_scale2(energy_data, intensity_data, energy_edges_keV)

    return delta_energy_keV, energies_keV, counts_data


def _compute_number_electrons(current_nA, time_s):
    nominal_number_electrons = current_nA * 1.0e-9 * time_s / e
    try:
        number_electrons = poisson(nominal_number_electrons)
    except ValueError as message:
        number_electrons = normal(nominal_number_electrons, np.sqrt(nominal_number_electrons))
    return nominal_number_electrons, number_electrons


def _export_raw_map(hdf5_file_path):
    from pySpectrumFileFormat.Bruker.MapRaw.ParametersFile import ParametersFile, BYTE_ORDER_LITTLE_ENDIAN, \
        RECORED_BY_VECTOR, DATA_TYPE_SIGNED

    logging.info("_export_raw_map")

    with h5py.File(hdf5_file_path, 'r', driver='core') as hdf5_file:
        maps_group = hdf5_file["maps"]

        for name, group in maps_group.items():
            if str(group.name).startswith("/maps/map"):
                map_data_set = group
                logging.info(group.name)
                logging.info(name)
                parameters_file = ParametersFile()
                parameters_file.width = map_data_set.attrs[MAP_WIDTH]
                parameters_file.height = map_data_set.attrs[MAP_HEIGHT]
                parameters_file.depth = map_data_set.attrs[MAP_DEPTH]
                parameters_file.offset = 0
                parameters_file.dataLength_B = 4
                parameters_file.dataType = DATA_TYPE_SIGNED
                parameters_file.byteOrder = BYTE_ORDER_LITTLE_ENDIAN
                parameters_file.recordBy = RECORED_BY_VECTOR
                parameters_file.energy_keV = 30.0
                parameters_file.pixel_size_nm = 0.0

                base_file_out_path = hdf5_file_path[:-5] + "_" + name.replace(' ', '_')
                parameters_file.write(base_file_out_path + ".rpl")

                shape = (parameters_file.height, parameters_file.width, parameters_file.depth)
                fp = np.memmap(base_file_out_path + ".raw", dtype=np.int32, mode='w+', shape=shape)
                fp[:] = map_data_set[:]
                del fp


if __name__ == '__main__':
    import sys

    logging.getLogger().setLevel(logging.INFO)

    if len(sys.argv) > 1:
        data_path = sys.argv[1]
    else:
        data_path = r"D:\work\Dropbox\hdemers\professional\results\simulations\mcxray\SimulationMapsMM2017\analyzes"

    logging.debug(sys.argv)
    logging.info(data_path)

    # create_test_map(data_path, figure=True)
    # export_raw_test_map(data_path)
    # read_raw_test_map(data_path)
    # create_map_mm2017_abstract(data_path)
    # export_raw_map_mm2017_abstract(data_path)
    # read_raw_map_mm2017_abstract(data_path)

    # bse_image_mm2017(data_path)

    logging.info("Done")
    plt.show()

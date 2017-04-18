=====
Usage
=====

To use xray-spectrum-modeling in a project look in the `examples` folder.
You need reference spectrum from mcxray simulation saved in a hdf5 file.

To run the example, you need to specify a path were to find a the mcxray reference spectrum in hdf5 file.

.. code-block:: console

   $python create_test_map.py ../../test_data/map

.. note::

   On windows use the ``py`` command and not ``python`` if you have more than one python version installed.

---------------
create_test_map
---------------

To run this example, you need to specify a path were to find a the mcxray reference spectrum in hdf5 file.

.. code-block:: console

   $python create_test_map.py ../../test_data/map

This path is passed to the method `run_maps` parameter `data_path`.
The variable `data_path` hold the path were the input and output data is read and writen.

First you need reference spectrum from mcxray simulation saved in a hdf5 file and
an output file to save the data.

.. code-block:: python

    hdf5_file_path = os.path.join(data_path, "SimulationMapsMM2017_3x3.hdf5")
    hdf5_file_out_path = os.path.join(data_path, "map_mm2017_abstract_3x3.hdf5")

Currently the probe positions to create a map are not read from the mcxray hdf5 file.
You need to create it yourself and if the positions does not correspond at the position simulated,
bad pixel will occur and maybe a crash of the script.

.. code-block:: python

    position = Positions()
    position.x_pixels = 3
    position.y_pixels = 3
    position.minimum_x_nm = -5.0e3
    position.maximum_x_nm = 5.0e3
    position.minimum_y_nm = -5.0e3
    position.maximum_y_nm = 5.0e3

With the correct positions, you can create different maps and spectra:

* Electron map using `_create_electron_maps`
* Intensity map using `_create_intensity_maps`
* Spectra which model the EDS detector noise using `_create_spectra_maps`
* Export the spectra map into .raw files using `_export_raw_map`

.. code-block:: python

    _create_electron_maps(data_path, hdf5_file_path, position)

    _create_intensity_maps(data_path, hdf5_file_path, position)

    _create_spectra(data_path, hdf5_file_path, position)

    _create_spectra_maps(data_path, hdf5_file_path, hdf5_file_out_path, position)

    _export_raw_map(hdf5_file_out_path)

.. warning::

   `_create_spectra` need to be called before `_create_spectra_maps`

.. warning::

   `_create_spectra_maps` need to be called before `_export_raw_map`

.. note::

   You need to have the project `microanalysis_file_format <https://github.com/drix00/microanalysis_file_format>`_ installed to use `_export_raw_map`.

This example shows a good pratice when working with xray-spectrum-modeling.
Use a small set of position to test the simulation and the code creating the x-ray spectrum and map.
The script will be fast and can be run with the debugger.
When everything is OK, run the larger probe positions to have a reallistic map.

.. note::

   The time to create a map increases with larger dose.
   A 128x128 map with a high dose with a acquisition time of 1000 s can take between 30 minutes to 1 hour.

To verify the map creation, the method `_read_raw_map` can be used.
But you need to have the project `microanalysis_file_format <https://github.com/drix00/microanalysis_file_format>`_ installed.

.. code-block:: python

    file_path = hdf5_file_out_path[:-5] + "_" + "map_1000000_us" + ".raw"
    _read_raw_map(file_path)


--------------------------
create_map_mm2017_abstract
--------------------------

This example is very similar to the previous one, but it create a 128x128 maps.

The only difference is different hdf5 files are specified and the positions list is different.

.. code-block:: python

    hdf5_file_path = os.path.join(data_path, "SimulationMapsMM2017.hdf5")
    hdf5_file_out_path = os.path.join(data_path, "map_mm2017_abstract_128x128.hdf5")

    position = Positions()
    position.x_pixels = 128
    position.y_pixels = 128
    position.minimum_x_nm = -5.0e3
    position.maximum_x_nm = 5.0e3
    position.minimum_y_nm = -5.0e3
    position.maximum_y_nm = 5.0e3

The rest of the code is the same.
Obvoiusly you need to pass the correct path for the 128x128 data to the script.

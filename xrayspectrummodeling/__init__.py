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
import os.path
import logging
import configparser

# Third party modules.

# Local modules.

# Project modules.

# Globals and constants variables.
__author__ = """Hendrix Demers"""
__email__ = 'hendrix.demers@mail.mcgill.ca'
__version__ = '0.1.0'


def get_current_module_path(modulePath, relativePath=""):
    basepath = os.path.dirname(modulePath)
    #logging.debug(basepath)

    filepath = os.path.join(basepath, relativePath)
    #logging.debug(filepath)
    filepath = os.path.normpath(filepath)

    return filepath


def get_mcxray_program_name(configurationFile, default=None):
        """
        Read the configuration file for the MCXRay program name.

        The configuration file need to have this entry:
        [Paths]
        mcxrayProgramName=McXRayLite.exe

        """
        sectionName = "Paths"
        keyName = "mcxrayProgramName"

        programName = read_value_from_configuration_file(configurationFile, sectionName, keyName, default)

        return programName


def read_value_from_configuration_file(configurationFile, sectionName, keyName, default=None):
        config = configparser.SafeConfigParser()
        config.readfp(open(configurationFile))
        if config.has_section(sectionName):
                if config.has_option(sectionName, keyName):
                        value = config.get(sectionName, keyName)
                        return value
                else:
                    logging.error("Configuration file (%s) does not have this option in section %s: %s", configurationFile, keyName, sectionName)
                    if default == None:
                        raise configparser.NoOptionError(keyName, sectionName)
                    else:
                        return default
        else:
            logging.error("Configuration file (%s) does not have this section: %s", configurationFile, sectionName)
            if default == None:
                raise configparser.NoSectionError(sectionName)
            else:
                return default


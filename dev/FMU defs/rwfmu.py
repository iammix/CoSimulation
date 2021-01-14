from lxml import etree
from datetime import datetime
import xml.etree.ElementTree as ET
import jinja2 as jja2
import logging as log
import subprocess as sp
import os
import sys
import shutil
import zipfile
import re
import platform
import random, string
import struct


def rewrite_fmu(self):
    fmi_version = float(self.fmi_version)
    if (self.export_tool == 'openmodelica' or platform.system().lower() == 'linux'
            or (float(fmi_version) > 1.0 and self.needs_tool.lower() == 'true')):

        fmutmp = self.model_name + '.tmp'
        zipdir = fmutmp + '.zip'
        fmu_name = self.model_name + '.fmu'
        
        if os.path.exists(fmutmp):
            shutil.rmtree(fmutmp)

        if not os.path.exists(fmutmp):
            os.makedirs(fmutmp)
        
        # Copy file to temporary folder
        shutil.copy2(fmu_name, fmutmp)

        # Get the current working directory
        os.chdir(fmutmp)

        # Path to the temporary directory
        fmutmp_path = os.path.normpath(os.path.join(cwd, fmutmp))

        # Unzip folder which contains the FMU
        zip_ref = zipfile.ZipFile(fmu_name, 'r')
        zip_ref.extractall('.')
        zip_ref.close()

        # Delete the FMU which is no longer used
        if os.path.isfile(fmu_name):
            os.remove(fmu_name)

        if (float(fmi_version) > 1.0 and self.needs_tool.lower() == 'true'):
            s = ( 'The model description file will be rewritten to include the attributes {!s} set to true.').format(NEEDSEXECUTIONTOOL)
            log.info(s)
            tree = ET.parse(MODELDESCRIPTION)
            # Get the root of the tree
            root = tree.getroot()
            # Add the needsExecution tool attribute
            root.attrib[NEEDSEXECUTIONTOOL] = 'true'
            tree.write(MODELDESCRIPTION, xml_declaration=True)
        
        # Switch back to the current wd
        os.chdir(cwd)
        # Pass the directory which will be zipped and call the zipper function
        zip_fmu(fmutmp, includeDirInZip=False)
        
        if (os.path.exists(fmutmp)):
            shutil.rmtree(fmutmp)

        if (os.path.isfile(fmu_name)):
            os.remove(fmu_name)

        # Renamed file
        os.rename(zipdir, fmu_name)

        # Write Success packing
        s = 'The FMU {!s} is successfully re-created.'.format(fmu_name)
        log.info(s)
        s = 'The FMU {!s} is in {!s}.'.format(fmu_name, os.getcwd())
        log.info(s)
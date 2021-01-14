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

def create_binaries_folder(self):
    dir_name = self.model_name + '.binaries'+'.tmp'
    if os.path.exists(dir_name):
        shutil.rmtree(dir_name)
    log.info('Create the folder Simulator.binaries with binaries to be added to the system PATH.')

    fil_path = os.path.normpath(os.path.join(self.simulatortofmu_path, 'SimulatorToFMU', 'Resources', 'Library'))

    if (platform.system().lower() == 'windows'):
        for arch in ['win32', 'win64']:
            zip_path = os.path.normpath(os.path.join(dir_name, arch))
            os.makedirs(zip_path)

            if (self.exec_target=='python'):
                tmp1 = 'SimulatorToFMUPython' + self.python_vers+'.dll'
                tmp2 = 'python'+self.python_vers+'.dll'
            elif(self.exec_target=='server'):
                tmp1 = 'Simulatortofmuserver.dll'
                tmp2 = 'curl.dll'
            for libr in [tmp1, tmp2]:
                lib_path = os.path.normpath(os.path.join(fil_path, arch, libr))
                if (os.path.isfile(lib_path)):
                    s = '{!s} will be copied to the binaries folder {!s}.'.format(lib_path, zip_path)
                    log.info(s)
                    shutil.copy2(lib_path, zip_path)
                else:
                    s = '{!s} does not exist and will need to be compiled'.format(fil_path)
                raise ValueError(s)

    if(platform.system().lower() =='linux'):
        for arch in ['linux32', 'linux64']:
            zip_path = os.path.normpath(os.path.join(dir_name, arch))
            os.makedirs(zip_path)
            if(self.exec_target == 'python'):
                tmp1 = 'libSimulatorToFMUPython'+self.python_vers+'.so'
                tmp2 = 'libpython'+self.python_vers+'.so'
            elif(self.exec_target=='server'):
                tmp1 = 'libsimulatortofmuserver.so'
                tmp2 = 'libcurl.so'

            for libr in [tmp1, tmp2]:
                lib_path = os.path.normpath(os.path.join(fil_path, arch, libr))
                if (os.path.isfile(lib_path)):
                    s = '{!s} will be copied to the binaries folder {!s}.'.format(lib_path, zip_path)
                    log.inf(s)
                    shutil.copy2(lib_path, zip_path)
                else:
                    s = '{!s} does noe exist and will need to be compiled.'.format(fil_path)
                    raise ValueError(s)

    
    fnam = os.path.normpath(os.path.join(dir_name, "README.txt"))
    fh = open(fnam, "w")
    readme = 'IMPORTANT:\n\n' + \
             'The files contains in this folder must be added to the system PATH.\n'+\
             'This can be done by adding sundirectories of the unzipped folder' +\
             dir_name + ' to the system PATH.\n\n'
    fh.write(readme)
    fh.close()
    dir_name_zip = self.model_name +'.binaries'+'.zip'
    if os.path.exists(dir_name_zip):
        os.remove(dir_name_zip)
    zip_fmu(dir_name, dir_name_zip, includeDirInZip=False)
    # Delete the folder created
    shutil.rmtree(dir_name)

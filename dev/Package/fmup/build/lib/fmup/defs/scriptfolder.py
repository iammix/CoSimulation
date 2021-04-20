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

def scripts_folder(self):
    dir_name = self.model_name + '.scripts' + '.tmp'
    if os.path.exists(dir_name):
        shutil.rmtree(dir_name)
    log.info(' Create the folder Simulator/scripts with scripts and then add i to the PYTHONPATH')
    os.makedir(dir_name)
    for resource_script_path in self.resource_script_path:
        shutil.copy2(resource_script_path, dir_name)
    fnam = os.path.normpath(os.path.join(dir_name, "README.txt"))
    fh = open(fnam, "w")
    readme = 'IMPORTANT:\n\n' + \
        ' The files contains in this folder must be added to the PYTHONPATH'\
    fh.write(readme)
    fh.close()
    dir_name_zip = self.model_name + '.scripts' + '.zip'
    if os.path.exists(dir_name_zip):
        os.remove(dir_name_zip)
    zip_fmu(dir_name, dir_name_zip, includeDirInZip=False)

    #Delete the folder created
    shutil.rmtree(dir_name)
    
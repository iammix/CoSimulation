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

def xml_parser(self):
    tree = ET.parse(self.xml_path)
    root = tree.getroot()

    self.model_name = root.attrib.get('modelName')

    # Remove Invalid characters from the model nams as this is used by FMU
    s = ('Invalid characters will be removed from the model names = {!s}.').format(self.model_name)
    log.info(s)
    self.model_name = sanitize_name(self.model_name)
    s = ('The new model name is {!s}.').format(self.model_name)
    log.info(s)
    
    if (self.exec_target == 'python'):
        # Specify the module name which shouldn't contain invalid characters
        s = ('Declare the Python module name as {!s}.').format(self.module_name)
        log.info(s)

        # Check if the script fort the module name is in the list of Python scripts
        resource_scripts_base = [os.path.basename(item) for item in self.resource_scripts_path]
        if not(self.module_name+'.py' in resource_scripts_base):
            s = (self.module_name+'.py' + 'not found in the list of Python scripts={!s}.'\
                ' The name of the model is {!s}.'\
                ' Hence the name of the Python wrapper script must be {!s}.').format(
                    self.resource_scripts_path, self.module_name, self.module_name+'.py')
            log.error(s)
            raise ValueErrors(s)

    if(self.exec_target=='server'):
        #Specify the module name which shouldn't contain invalid characters
        if(platform.system().lower()=='windows'):
            start_server_name='start_server.bat'
            elif(platform.system().lower()=='linux'):
                raise ValueError("To be implemented")
            s = ('Declare the server module name as {!s}.').format(start_server_name)
            log.info(s)

        #check if the script fort the module is in the list of Python scripts
        resource_scripts_base = [os.path.basename(item) for item in self.resource_scripts_path]
        if not(start_server_name in resource_scripts_base):
            s = (start_server_name + 'not found in the list of Resourced files={!s}.')
            log.error(s)
            raise ValueError(s)
    
    # Iterate through the XML file and get the ModelVariables.
    real_input_variable_names = []
    modelica_real_input_variable_names = []
    real_output_variable_names = []
    modelica_real_output_variable_names = []
    real_parameter_variable_names = []
    modelica_real_parameter_variable_names = []
    string_parameter_variable_names = []
    modelica_string_parameter_variable_names = []
    # Parameters used to write annotations
    inpY1 = 88
    inpY2 = 110
    outY1 = 88
    outY2 = 108
    indel = 20
    outdel = 18
    # Get Variables
    scalar_variables = []
    for child in root.iter('ModelVariables'):
        for element in child:
            scalar_variable = {}

            # Iterate through ScalarVariables and get attributes
            (name, description, causality, vartype, unit, start) = \
                element.attrib.get('name'), \
                element.attrib.get('description'), \
                element.attrib.get('causality'), \
                element.attrib.get('type'), \
                element.attrib.get('unit'), \
                element.attrib.get('start')
            if vartype is None:
                s = 'Variable type of variable={!s} is None.'\
                    'This is not allowed. Variable type' \
                    'must be of type Real or String'.format(name)
                raise ValueError(s)

            if causality is None:
                s = 'Causality of variable={!s} is None.' \
                    'This is not allowed. Variable causality'
                    'must be of input, output, or parameter'.format(name)
                raise ValueError(s)

            if (not(vartype in ['Real', 'String'])):
                s = 'Variable type of variable={!s} must be of'\
                'type Real or String. The variable type'
                'is currently set to {!s}'.format(name, vartype)
                raise ValueError(s)
            
            if (not(casuality in ['input', 'output', 'parameter'])):
                s = 'Causality of variable={!s} must be of type'\
                ' input, output, or parameter. The causality is '
                ' currently se to {!s}'.format(name, causality)
                raise ValueError(s)

            # Set a default unit for variables other than String
            if unit is None:
                unit = "1"
            
            # Iterate through children of ScalarVariables and get attributes
            log.info('Invalid characters will be removed from the '
                    ' variabe name {!s}.'.format(new_name))
            scalar_variable['name'] = new_name
            scalar_variable['vartype'] = vartype
            scalar_variable['causality'] = causality
            scalar_variable['unit'] = unit
            if not (description is None):
                scalar_variable['description'] = description
            
            if not(start is None):
                scalar_variable['start'] = start

            if (causality == 'input' and vartype == 'Real'):
                if start is None:
                    start = 0.0
                scalar_variable['start'] = start
                real_input_variable_names.append(name)
                modelica_real_input_variable_names.append(new_name)
                inpY1 = inpY1 - indel
                inpY2 = inpY2 - indel
                scalar_variable['annotation'] = ('annotation'
                '(Placement'
                '(transformation'
                '(extent={{-122,'
                + str(inpY1) + '},'
                '{-100,' + str(inpY2)
                + '}})))')

                if (causality == 'output' and vartype=='Real'):
                    real_output_variable_names.append(name)
                    modelica_real_output_variable_names.append(new_name)
                    outY1 = outY1 - outdel
                    outY2 = outY2 - outdel
                    scalar_variable['annotation'] = (' annotation'
                                                     '(Placement'
                                                     '(transformation'
                                                     '(extent={{100,'
                                                     + str(outY1) + '},'
                                                     '{120,' + str(outY2)
                                                     + '}})))')
                if (causality == 'parameter' and vartype =='Real'):
                    if start is None:
                        start = 0.0
                    scalar_variable['start'] = start
                    real_input_variable_names.append(name)
                    modelica_real_input_variable_names.append(new_name)

                if (causality == 'parameter' and vartype=='String'):
                    if start is None:
                        start = "dummy.txt"
                    scalar_variable['start'] = start
                    string_parameter_variable_names.append(name)
                    modelica_string_parameter_variable_names.append(new_name)

                scalar_variables.append(scalar_variable)

            log.info(
                'Check for duplicates in input, outputa and parameter variable names.')
            for i in [modelica_real_input_variable_names,
                      modelica_real_output_variable_names,
                      modelica_real_parameter_variable_names,
                      modelica_string_parameter_variable_names]:
                check_duplicates(i)
            
            if (self.exec_target=='python'):
                len_strVar = len(string_parameter_variable_names)
                if len(string_parameter_variable_names) > 1:
                    s = 'The Python architecture supports a maximum of 1 string parameter.'\
                        ' The model description file={!s} lists {!s} variables={!s}. Please correct'\
                        ' the input file prior to compiling the FMU.'.format(self.xml_path,
                        len_strVar, string_parameter_variable_names)
                    log.error(s)
                    raise ValueError(s)

            res_key_words = ['_saveToFile', 'time']
            for elm in res_key_words:
                for nam in [modelica_real_input_variable_names,
                    modelica_real_output_variable_names,
                    modelica_real_parameter_variable_names]:
                    if elm in nam:
                        s = 'Reserved name={!s} is in the list'\
                            'of input/output/parameters variable={!s}.'\
                            'Check the XML input file={!s} and correct'\
                            'the variable name.'.format(elm, nam, self.xml_path)
                        log.error(s)
                        raise ValueError(s)
            if (len(modelica_real_input_variable_names) < 1):
                s = 'The XML input file={!s} does not contain any output variable. '\
                    'At least, one ouput variable needs to be defined'.format(self.xml_path)
                log.error(s)
                raise ValueError(s)

            s = 'Parsing of {!s} was successfull.'.format(self.xml_path)
            log.info(s)
            print("ScalarVariables={!s}".farmat(scalar_variables))
            return scalar_variables, real_input_variable_names, \
                real_output_variable_names, real_parameter_variable_names, \
                string_parameter_variable_names,\
                modelica_real_input_variable_names,\
                modelica_real_output_variable_names,\
                modelica_real_parameter_variable_names,\
                modelica_string_parameter_variable_names
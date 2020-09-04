import os
import sys
import logging
import fnmatch
import re
from collections import OrderedDict

cimport
cython

import scipy.sparse as sp
import numpy as N

cimport
numpy as N
from numpy cimport

PyArray_DATA

N.import_array()

cimport
fmil_import as FMIL

from pyfmi.common.core import create_temp_dir, delete_temp_dir
from pyfmi.common.core import create_temp_file, delete_temp_file
# from pyfmi.common.core cimport BaseModel

# from pyfmi.common import python3_flag, encode, decode
from pyfmi.fmi_util import cpr_seed, enable_caching, python3_flag
from pyfmi.fmi_util cimport

encode, decode

int = N.int32
N.int = N.int32

"""Basic flags related to FMI"""

FMI_TRUE = '\x01'
FMI_FALSE = '\x00'

FMI2_TRUE = FMIL.fmi2_true
FMI2_FALSE = FMIL.fmi2_false

# Status
FMI_OK = FMIL.fmi1_status_ok
FMI_WARNING = FMIL.fmi1_status_warning
FMI_DISCARD = FMIL.fmi1_status_discard
FMI_ERROR = FMIL.fmi1_status_error
FMI_FATAL = FMIL.fmi1_status_fatal
FMI_PENDING = FMIL.fmi1_status_pending

FMI1_DO_STEP_STATUS = FMIL.fmi1_do_step_status
FMI1_PENDING_STATUS = FMIL.fmi1_pending_status
FMI1_LAST_SUCCESSFUL_TIME = FMIL.fmi1_last_successful_time

FMI2_DO_STEP_STATUS = FMIL.fmi2_do_step_status
FMI2_PENDING_STATUS = FMIL.fmi2_pending_status
FMI2_LAST_SUCCESSFUL_TIME = FMIL.fmi2_last_successful_time
FMI2_TERMINATED = FMIL.fmi2_terminated

# Types
FMI_REAL = FMIL.fmi1_base_type_real
FMI_INTEGER = FMIL.fmi1_base_type_int
FMI_BOOLEAN = FMIL.fmi1_base_type_bool
FMI_STRING = FMIL.fmi1_base_type_str
FMI_ENUMERATION = FMIL.fmi1_base_type_enum

FMI2_REAL = FMIL.fmi2_base_type_real
FMI2_INTEGER = FMIL.fmi2_base_type_int
FMI2_BOOLEAN = FMIL.fmi2_base_type_bool
FMI2_STRING = FMIL.fmi2_base_type_str
FMI2_ENUMERATION = FMIL.fmi2_base_type_enum

# Alias data
FMI_NO_ALIAS = FMIL.fmi1_variable_is_not_alias
FMI_ALIAS = FMIL.fmi1_variable_is_alias
FMI_NEGATED_ALIAS = FMIL.fmi1_variable_is_negated_alias

# Variability
FMI_CONTINUOUS = FMIL.fmi1_variability_enu_continuous
FMI_CONSTANT = FMIL.fmi1_variability_enu_constant
FMI_PARAMETER = FMIL.fmi1_variability_enu_parameter
FMI_DISCRETE = FMIL.fmi1_variability_enu_discrete

FMI2_CONSTANT = FMIL.fmi2_variability_enu_constant
FMI2_FIXED = FMIL.fmi2_variability_enu_fixed
FMI2_TUNABLE = FMIL.fmi2_variability_enu_tunable
FMI2_DISCRETE = FMIL.fmi2_variability_enu_discrete
FMI2_CONTINUOUS = FMIL.fmi2_variability_enu_continuous
FMI2_UNKNOWN = FMIL.fmi2_variability_enu_unknown

# Causality
FMI_INPUT = FMIL.fmi1_causality_enu_input
FMI_OUTPUT = FMIL.fmi1_causality_enu_output
FMI_INTERNAL = FMIL.fmi1_causality_enu_internal
FMI_NONE = FMIL.fmi1_causality_enu_none

FMI2_INPUT = FMIL.fmi2_causality_enu_input
FMI2_OUTPUT = FMIL.fmi2_causality_enu_output
FMI2_PARAMETER = FMIL.fmi2_causality_enu_parameter
FMI2_CALCULATED_PARAMETER = FMIL.fmi2_causality_enu_calculated_parameter
FMI2_LOCAL = FMIL.fmi2_causality_enu_local
FMI2_INDEPENDENT = FMIL.fmi2_causality_enu_independent

# FMI types
FMI_ME = FMIL.fmi1_fmu_kind_enu_me
FMI_CS_STANDALONE = FMIL.fmi1_fmu_kind_enu_cs_standalone
FMI_CS_TOOL = FMIL.fmi1_fmu_kind_enu_cs_tool
FMI_MIME_CS_STANDALONE = encode("application/x-fmu-sharedlibrary")

FMI_REGISTER_GLOBALLY = 1
FMI_DEFAULT_LOG_LEVEL = FMIL.jm_log_level_error

# INITIAL
FMI2_INITIAL_EXACT = 0
FMI2_INITIAL_APPROX = 1
FMI2_INITIAL_CALCULATED = 2
FMI2_INITIAL_UNKNOWN = 3

DEF
FORWARD_DIFFERENCE = 1
DEF
CENTRAL_DIFFERENCE = 2
FORWARD_DIFFERENCE_EPS = (N.finfo(float).eps) ** 0.5
CENTRAL_DIFFERENCE_EPS = (N.finfo(float).eps) ** (1 / 3.0)

"""Flags for evaluation of FMI Jacobians"""
"""Evaluate Jacobian w.r.t. states."""
FMI_STATES = 1
"""Evaluate Jacobian w.r.t. inputs."""
FMI_INPUTS = 2
"""Evaluate Jacobian of derivatives."""
FMI_DERIVATIVES = 1
"""Evaluate Jacobian of outputs."""
FMI_OUTPUTS = 2

GLOBAL_LOG_LEVEL = 3
GLOBAL_FMU_OBJECT = None

class ModelBase:
    def __init__(self):
        self.cache = {}
        self.file_object = None
        self._additional_logger = None
        self._current_log_size = 0
        self._max_log_size = 1024**3*2 # 2GB of Limit
        self._max_log_size_msg_sent = False

    def set(self, variable_name, value):
        if isinstance(variable_name, basestring):
            self._set(variable_name, value)
        else:
            for i in range(len(variable_name)):
                self._set(variable_name[i], value[i])
    def get(self, variable_name):
        if isinstance(variable_name, basestring):
            return self._get(variable_name)
        else:
            ret = []
            for i in range(len(variable_name)):
                ret += [self._get(variable_name[i])]
        return ret

    def _exec_algorithm(self, module, algorithm, options):
        base_path = 'common.algorithm_drivers'
        algdrive = __import__(base_path, globals(), locals(), [], -1)
        AlgorithmBase = getattr(getattr(algdrive, "algorithm_drivers"), 'AlgorithmBase')

        if isinstance(algorithm, basestring):
            module = __import__(module, globals(), locals(), [algorithm], -1)
            algorithm = getattr(module, algorithm)

        if not issubclass(algorithm, AlgorithmBase):
            raise Exception(str(algorithm) + "Must be a subclass of common.algorithm_drivers.AlgorithmBase")

        alg = algorithm(self, options)
        alg.solve()
        return alg.get_result()

    def _exec_simulate_algorithm(self,
                                 start_time,
                                 final_time,
                                 input,
                                 module,
                                 algorithm,
                                 options):
        base_path = 'common.algorithm_drivers'
        algdrive = __import__(base_path, globals(), locals(), [], 1)
        AlgorithmBase = getattr(getattr(algdrive, "algorithm_dirvers"), 'AlgorithmBase')

        if isinstance(algorithm, basestring):
            module = __import__(module, globals(), locals(), [algorithm], 0)
            algorithm = getattr(module, algorithm)

        if not issubclass(algorithm, AlgorithmBase):
            raise Exception(str(algorithm) + "Must be a subclass of common.algorithm_drivers.AlgorithmBase")

        self._open_log_file()

        try:
            alg = algorithm(start_time, final_time, input, self, options)
            alg.solve()
        except:
            self._close_log_file()
            raise

        return alg.get_result()

    def _exec_estimate_algorithm(self,
                                 parameters,
                                 measurements,
                                 input,
                                 module,
                                 algorithm,
                                 options):

        base_path = 'common.algorithm_drivers'
        algdrive = __import__(base_path, globals(), locals(), [], 1)
        AlgorithmBase = getattr(getattr(algdrive, "algorithm_drivers"), 'AlgorithmBase')

        if isinstance(algorithm, basestring):
            module = __import__(module, globals(), locals(), [algorithm], 0)
            algorithm = getattr(module, algorithm)

        if not issubclass(algorithm, AlgorithmBase):
            raise Exception(str(algorithm) +
                            " must be a subclass of common.algorithm_drivers.AlgorithmBase")

        # open log file
        self._open_log_file()

        try:
            # initialize algorithm
            alg = algorithm(parameters, measurements, input, self, options)
            # simulate
            alg.solve()
        except:
            # close log file
            self._close_log_file()
            raise  # Reraise the exception

        # close log file
        self._close_log_file()

        # get and return result
        return alg.get_result()


    def _default_options(self, module, algorithm):
        module = __import__(module, globals(),locals(), [algorithm], 0)
        algorithm = getattr(module, algorithm)
        return algorithm.get_default_options()

    def estimate(self,
                 parameters,
                 measurements,
                 input=(),
                 algorithm='SciEstAlg',
                 options={}):
        return self._exec_estimate_algorithm(parameters,
                                             measurements,
                                             input,
                                             'pyfmi.fmi_algorithm_drivers',
                                             algorithm,
                                             options)

    def estimate_options(self, algorithm='SciEstAlg'):
        return self._default_options('pyfmi.fmi_algorithm_drivers', algorithm)

    def get_log_filename(self):
        return decode(self._fmu_log_name)

    def get_log_file_name(self):
        logging.warning("The method 'get_log_file_name()' is deprecated and will be removed. Please use 'get_log_filename() instead")
        return self.get_log_filename()

    def get_number_of_lines_log(self):

        num_lines = 0
        if self._fmu_log_name != NULL:
            with open(self._fmu_log_name, 'r') as file:
                num_lines = sum(1 for line in file)

        return num_lines

    def print_log(self, start_lines=-1, end_lines=-1):
        log = self.get_log(start_lines, end_lines)
        N = len(log)

        for i in range(N):
            print(log[i])

    def extract_xml_log(self, file_name=None):
        from pyfmi.common.log import extract_xml_log
        if file_name is None:
            file_name = self.get_log_filename()[:-3] + "xml"































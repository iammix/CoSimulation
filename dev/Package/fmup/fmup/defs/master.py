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
        pass




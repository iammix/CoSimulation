import os
import numpy as np
import openseespy.opensees as ops
import shutil

class Bridge(object):
    def __init__(self, elenum, vel, L, A, MassPerLength, E, Izz, )
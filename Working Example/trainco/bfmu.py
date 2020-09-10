from pythonfmu import Fmi2Causality, Fmi2Variability, Fmi2Slave, Real
import bridge
import numpy as np


class Bridge(Fmi2Slave):
    author = "iammix"
    description = "Bridge OpenSees model"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.Mb = 10
        self.Mw = 10
        self.k = 10
        self.c = 0
        self.dofs = 2
        self.m = np.array([self.Mb, self.Mw])
        self.k = np.array([0, self.k, 0])
        self.c = np.array([0, self.c, 0])
        self.IC = np.array([0, 0, 0, 0, 0, 0])

    def do_step(self):
        bridge.main()
        return true

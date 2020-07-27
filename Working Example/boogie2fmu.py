from fmup import Fmi2Causality, Fmi2Variability, Fmi2Slave, Real
import numpy as np
import boogie

class DoubleOsc(Fmi2Slave):
    author = "iammix"
    description = "A simple description of 2DOF Oscillator. For more infos take a look at bo ogie.py file"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Mass Define
        self.mw = 10.0
        self.mv = 10000.0
        self.m = np.array([self.mw, self.mv])

        # Stiffness Define
        self.k0 = 1000000.0

        # Damping Define
        self.c0 = 100
        self.Tn = 0.0
        self.DTc = 10.0
        self.f = 0.0
        self.tag = 1
        self.roughness = 1
        self.length = 100
        self.velocity = 5
        self.omega = 20
        self.irr_0 = 0.12
        self.x = np.array([0.0, 0.0, 0.0])
        self.v = np.array([0.0, 0.0, 0.0])
        self.constr = np.array([omega, irr_0])
        self.disp1 = np.arrar

        self.register_variable(Real())

    def do_step(self, current_time, cs_timestep,):
        boogie.main()
        return True

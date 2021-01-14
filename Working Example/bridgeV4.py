from fmup import Fmi2Causality, Fmi2Variability, Fmi2Slave, Real
import numpy as np
import openseespy.opensees as ops
import shutil
import os
import matplotlib.pyplot as plt


class BridgefmuV4(Fmi2Slave):
    author = "iammix"
    description = "Bridge OpenSees model."

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.nsteps = 10

        self.number_of_elements = 6
        self.node_number = self.number_of_elements + 1
        self.izz = 1
        self.young_modulus = 100000
        self.mass_per_length = 1
        self.section_area = 1
        self.length = 10
        self.velocity = 5
        self.tag = 1
        # self.Fn = 1231231
        # self.Fnplusi = 1231231
        self.u = 0
        self.analysis_duration = 100000
        self.test_force = 100
        self.time = 0.0
        self.xload = 0.0
        self.dt = 0.0001

        # Register Variables
        self.register_variable(Real("tag", causality=Fmi2Causality.input))
        # self.register_variable(Real("Fn", causality=Fmi2Causality.input))
        # self.register_variable(Real("Fnplusi", causality=Fmi2Causality.input))
        self.register_variable(Real("u", causality=Fmi2Causality.output))
        self.register_variable(Real("velocity", causality=Fmi2Causality.parameter, variability=Fmi2Variability.tunable))

        self.register_variable(
            Real("analysis_duration", causality=Fmi2Causality.parameter, variability=Fmi2Variability.tunable))
        self.register_variable(
            Real("test_force", causality=Fmi2Causality.parameter, variability=Fmi2Variability.tunable))
        self.register_variable(Real("time", causality=Fmi2Causality.output))
        self.register_variable(Real("xload", causality=Fmi2Causality.output))

    def do_step(self, current_time, step_size):
        step_size = self.dt
        # UNITS
        self.MM = 1.0  # milimeters
        self.N = 1.0  # Newton
        self.SEC = 1.0  # seconds

        # INITIALIZE OPENSEES MODEL
        ops.wipe()
        ops.wipeAnalysis()

        ops.model('basic', '-ndm', 2, '-ndf', 3)
        self.dir_of_database = "..\\OpenseesDB"
        self.access_rights = 0o777
        os.mkdir(self.dir_of_database, self.access_rights)
        ops.database('File', "{}/OpenSees_Model".format(self.dir_of_database))

        # CONSTRUCT MODEL
        element_length: float = self.length / self.number_of_elements
        temp = 0
        for i in range(1, self.node_number + 1):
            ops.node(i, temp, 0.0)
            temp += element_length
        ops.fix(1, 1, 1, 0)
        ops.fix(self.node_number, 0, 1, 1)
        ops.geomTransf('Linear', 1, 0, 0, 1)
        for i in range(1, self.node_number):
            ops.element('elasticBeamColumn', i, i, i + 1, self.section_area, self.young_modulus, self.izz, 1, '-mass',
                        self.mass_per_length)

        # INITIAL CONDITIONS
        for i in range(1, self.number_of_elements + 2):
            ops.setNodeDisp(i, 2, 0)
            ops.setNodeVel(i, 2, 0)
            ops.setNodeAccel(i, 2, 0)

        analysis_duration = self.analysis_duration
        start_time = ops.getTime() - step_size
        ops.save(1)

        for i in range(0, self.nsteps + 1):
            load_factor = self.test_force
            # load_factor = (self.Fn + (self.Fnplusi - self.Fn) / self.nsteps)
            ops.timeSeries('Path', i, '-values', 0, load_factor, 0, '-time', start_time, start_time + 2 * step_size,
                           4 * step_size,
                           '-prependZero')
            ops.pattern('Plain', i, i)
            next_id = 0
            self.xload = self.velocity * (ops.getTime() + i * step_size)
            for j in range(1, self.node_number + 1):
                if ops.nodeCoord(j, 1) > self.xload:
                    next_id = j
                    break
            ops.eleLoad('-ele', next_id - 1, '-type', '-beamPoint', 1, (self.xload - ops.nodeCoord(next_id - 1, 1)) / (
                    ops.nodeCoord(next_id, 1) - ops.nodeCoord(next_id - 1, 1)))
            start_time += step_size

            ops.wipeAnalysis()
            ops.constraints('Plain')
            ops.system('ProfileSPD')
            ops.numberer('Plain')
            ops.integrator('HHT', 0.67)
            ops.algorithm('Linear')
            ops.test('NormUnbalance', 1e-5, 100, 2)
            ops.analysis('Transient')
            current_time = 0.0

            analysis_tag = 0

            while analysis_tag == 0 and current_time < analysis_duration:
                analysis_tag = ops.analyze(1, step_size)
                current_time = ops.getTime()
                self.u = (ops.nodeDisp(3, 2))

            self.time = current_time
            print("DONE")
            return True

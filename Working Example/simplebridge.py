from fmup import Fmi2Causality, Fmi2Variability, Fmi2Slave, Real
import openseespy.opensees as ops
import matplotlib.pyplot as plt


class SimpleBridge(Fmi2Slave):
    author = "iammix"
    description = "Simple Bridge Model!"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.number_of_elements = 10
        self.number_of_nodes = self.number_of_elements + 1
        self.izz = 1
        self.E = 29e6
        self.mass_per_length = 20
        self.section_area = 10
        self.length = 100
        self.u = 0
        self.analysis_duration = 0.0
        self.step_size = 0.001
        self.force = 1
        self.nsteps = 1000
        self.start_time = 0
        self.next_node_id = 0
        self.load_position = 0
        self.velocity = 10
        self.disp = []
        self.time = []

        # self.register_variable(Real("disp", causality=Fmi2Causality.calculatedParameter, variability=Fmi2Variability.tunable))
        # self.register_variable(Real("time", causality=Fmi2Causality.calculatedParameter, variability=Fmi2Variability.tunable))
        self.register_variable(Real("force", causality=Fmi2Causality.input))

    def do_step(self, current_time, step_size):
        ops.wipe()
        ops.wipeAnalysis()
        ops.model('basic', '-ndm', 2, '-ndf', 3)

        element_length = self.length / self.number_of_elements
        temp = 0
        for i in range(self.number_of_nodes):
            ops.node(i, temp, 0.0)
            temp += element_length
        ops.fix(0, 1, 1, 1)
        ops.fix(self.number_of_nodes - 1, 1, 1, 1)
        ops.geomTransf('Linear', 1, 0, 0, 1)

        for i in range(self.number_of_nodes - 1):
            ops.element('elasticBeamColumn', i, i, i + 1, self.section_area, self.E, self.izz, 1, '-mass',
                        self.mass_per_length)

        self.start_time = ops.getTime() - self.step_size

        for i in range(self.nsteps + 1):
            ops.timeSeries('Path', i, '-values', 0, 1, 0, '-time', self.start_time,
                           self.start_time + 2 * self.step_size, 4 * self.step_size, '-prependZero')
            ops.pattern('Plain', i, i)
            self.load_position = self.velocity * (ops.getTime() + i * self.step_size)
            for j in range(self.number_of_nodes):
                if ops.nodeCoord(j, 1) > self.load_position:
                    self.next_node_id = j
                    break
            ops.eleLoad('-ele', self.next_node_id - 1, '-type', '-beamPoint', self.force,
                        (self.load_position - ops.nodeCoord(self.next_node_id - 1, 1)) / (
                                    ops.nodeCoord(self.next_node_id, 1) - ops.nodeCoord(self.next_node_id - 1, 1)))
            self.start_time += self.step_size

        ops.constraints('Penalty', 1e+10, 1e+10)
        ops.system('ProfileSPD')
        ops.numberer('Plain')
        # ops.rayleigh(0, 0, 10, 0)
        ops.integrator('HHT', 0.67)
        ops.algorithm('Linear')
        ops.test('NormDispIncr', 1e-5, 100, 2)
        ops.analysis('Transient')
        current_time = 0.0
        self.analysis_duration = self.nsteps * self.step_size
        analysis_tag = 0

        self.time = []
        self.disp = []
        while analysis_tag == 0 and current_time < self.analysis_duration:
            analysis_tag = ops.analyze(1, step_size)
            current_time = ops.getTime()
            self.time.append(current_time)
            self.disp.append(ops.nodeDisp(5, 2))

        plt.plot(self.time, self.disp)
        plt.show()


from fmup import Fmi2Causality, Fmi2Variability, Fmi2Slave, Real


class Test(Fmi2Slave):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.x = 1
        self.delta_v = 1
        self.f_time = 100


        self.register_variable((Real("delta_v", causality=Fmi2Causality.input, description="Input-output")))
        self.register_variable(Real("delta_v", causality=Fmi2Causality.output, description="Input-output"))
        self.register_variable(Real("f_time", causality=Fmi2Causality.parameter, variability=Fmi2Variability.tunable))

    def do_step(self, current_time, step_size):
        self.delta_v = step_size
        return True

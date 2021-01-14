from pythonfmu import Fmi2Causality, Fmi2Causality, Fmi2Slave, Real

class Vehicle(Fmi2Slave):
    author = "Konstantinos Mixios"
    description = "Vehicle with 2DOFS responding to vertical"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.register_variable("R", causality=Fmi2Causality.parameter, variability=)
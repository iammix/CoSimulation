from pyfmi import load_fmu
import numpy
model = load_fmu('SimpleBridge.fmu')
for i in range(0, 1000, 10):
    force = ('force', lambda force: -10 * i)
    res = model.simulate(input=force)

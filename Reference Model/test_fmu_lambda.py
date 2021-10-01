from pyfmi import load_fmu

import matplotlib.pyplot as p
import numpy

model = load_fmu('Resistor.fmu')

inputs = ('positive_pin_v', lambda t: 20 + 5. * numpy.cos(t))

res = model.simulate(final_time=30, input=inputs, options={'ncp': 300})

fig = p.figure()
ax1 = p.subplot(2, 1, 1)
ax1.plot(res['time'], res['i'])
ax1.set_ylabel('Intensity [A]')
ax2 = p.subplot(2, 1, 2)
ax2.plot(res['time'], res['delta_v'])
ax2.set_xlabel('time')
ax2.set_ylabel('Voltage [V]')
p.show()
from pyfmi import load_fmu

import matplotlib.pyplot as p

model = load_fmu('Test.fmu')

f_time_reference = model.get_model_variables()['f_time'].value_reference
model.set_real([f_time_reference, ], [100.0, ])
res = model.simulate()



fig = p.figure()
ax2 = p.subplot(1, 1, 1)
ax2.plot(res['time'], res['delta_v'])
ax2.set_xlabel('time')
ax2.set_ylabel('Voltage [V]')
p.show()

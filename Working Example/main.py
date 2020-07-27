from pyfmi import load_fmu

model = load_fmu('Debugbridgefmuv2.fmu')
model.simulate()
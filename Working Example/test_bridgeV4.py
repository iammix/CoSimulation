from pyfmi import load_fmu
import matplotlib.pyplot as plt

model = load_fmu("BridgefmuV4.fmu")

res = model.simulate()
y = res['time']
z = res['xload']
x = res['u']

plt.plot(z, y)
plt.show()


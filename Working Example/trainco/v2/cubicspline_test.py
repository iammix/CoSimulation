#import numpy as np
#import matplotlib.pyplot as plt
#from scipy import interpolate
#timestamp = (0,5,10,15,30,35,40,50,55,60)
#distance = (100,90,65,85,70,30,40,45,20,0)
#plt.plot(timestamp, distance, 'o')
#plt.show()
#data = np.array((timestamp,distance))
#tck,u = interpolate.splprep(data, s=0)
#unew = np.arange(0, 1.01, 0.01)
#out = interpolate.splev(unew, tck)
#plt.plot(out[0], out[1], color='orange')
#plt.plot(data[0,:], data[1,:], 'ob')
#plt.show()

from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt
import numpy as np
x = np.arange(10)
y = np.sin(x)
cs = CubicSpline(x, y)
xs = np.arange(-0.5, 9.6, 0.1)
plt.figure(figsize=(6.5, 4))
plt.plot(x, y, 'o', label='data')
plt.plot(xs, np.sin(xs), label='true')
plt.plot(xs, cs(xs), label="S")
plt.plot(xs, cs(xs, 1), label="S'")
plt.plot(xs, cs(xs, 2), label="S''")
plt.plot(xs, cs(xs, 3), label="S'''")
plt.xlim(-0.5, 9.5)
plt.legend(loc='lower left', ncol=2)
plt.show()
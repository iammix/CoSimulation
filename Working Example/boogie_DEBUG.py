import numpy as np
import os
from shutil import copyfile as cp
import matplotlib.pyplot as plt

# Create database
try:
    dir_of_database = "..\\BoogieDB"
    access_rights = 0o777
    os.mkdir(dir_of_database, access_rights)
except:
    pass

dofs = 2
state_current = np.zeros(3 * dofs)
M = np.zeros([dofs, dofs])
K = np.zeros([dofs, dofs])
C = np.zeros([dofs, dofs])
time = 0.0
duration = 50
force = np.zeros(dofs)
force_inter = None
interface_dof = None
nsteps = 100
dt = duration / nsteps
t = np.linspace(time, time + duration, nsteps + 1)
tag = 0
k = [1e+4, 0]  # define MATRIXES
c = [0, 0]  # define MATRIXES
m = [1, 10]  # define MATRIXES

dofs = dofs + 1
state_current = np.concatenate((state_current, np.zeros(3)))
force = np.concatenate((force, np.zeros(1)))
M = np.vstack((np.concatenate((M, np.zeros([2, 1])), axis=1), np.array([1.0, 0, 0])))
M[0, 2] = 1.0
C = np.vstack((np.concatenate((C, np.zeros([2, 1])), axis=1), np.zeros(3)))
K = np.vstack((np.concatenate((K, np.zeros([2, 1])), axis=1), np.zeros(3)))


M[0, 0] = m[0]
M[1, 1] = m[1]

K[0, 0] = k[0]
K[0, 1] = -k[0]
K[1, 0] = -k[0]
K[1, 1] = k[0]

C[0, 0] = c[0]
C[0, 1] = -c[0]
C[1, 0] = -c[0]
C[1, 1] = c[0]


h = dt
x = np.zeros([dofs, len(t)])
xdot = np.zeros([dofs, len(t)])
xddot = np.zeros([dofs, len(t)])

if tag == 1:
    cp("{}/file1.txt".format(dir_of_database), "{}/file0.txt".format(dir_of_database))

try:
    with open('file0.txt') as f:
        state_current = []
        for line in f:
            for x in line.split():
                state_current(float(x))
    x[0:dofs, 0] = state_current[0:dofs]
    xdot[dofs:2 * dofs, 0] = state_current[dofs:2 * dofs]
    xddot[2 * dofs:3 * dofs, 0] = state_current[2 * dofs:3 * dofs]
except:
    pass

xdot[1, 0] = 100
# HHT
af = 1 / 3
gamma = 1 / 2 + af
beta = 1 / 4 + 1 / 2 * af
for i in range(len(t) - 1):
    t_af = (1 - af) * t[i + 1] + af * t[i]
    t_af = t[i + 1]
    temp_1 = M + (h * gamma) * (1 - af) * C + (h ** 2 * beta) * (1 - af) * K
    temp_2 = -(np.matmul(C, (xdot[:, i] + h * (1 - gamma) * (1 - af) * xddot[:, i])))
    temp_3 = -(np.matmul(K, (
            x[:, i] + h * (1 - af) * xdot[:, i] + h ** 2 * (1 / 2 - beta) * (1 - af) * xddot[:, i])))
    # force[interface_dof - 1] = force_inter(t_af)

    xddot[:, i + 1] = np.linalg.solve(temp_1, temp_2 + temp_3)  # + force)

    xdot[:, i + 1] = xdot[:, i] + (1 - gamma) * h * xddot[:, i] + (gamma) * h * xddot[:, i + 1]
    x[:, i + 1] = x[:, i] + h * xdot[:, i] + h * h / 2 * (
            (1 - 2 * beta) * xddot[:, i] + (2 * beta) * xddot[:, i + 1])


state_current[0:dofs] = x[0:dofs, -1]
state_current[dofs:2 * dofs] = xdot[0:dofs, -1]
state_current[2 * dofs:3 * dofs] = xddot[0:dofs, -1]



with open("{}/file1.txt".format(dir_of_database), "w") as f:
    for items in state_current:
        f.write('{}\n'.format(items))


plt.plot(t, x[1])
plt.show()

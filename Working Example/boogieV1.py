from fmup import Fmi2Variability, Fmi2Causality, Fmi2Slave, Real
import numpy as np
import os
from shutil import copyfile as cp
import matplotlib.pyplot as plt


# fmup build -f boogieV1.py --no-external-tool
class BoogiefmuV1(Fmi2Slave):
    description = "Boogie Simple model"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.dofs = 2
        self.M = np.zeros([self.dofs, self.dofs])
        self.K = np.zeros([self.dofs, self.dofs])
        self.C = np.zeros([self.dofs, self.dofs])
        self.time = 0.0
        self.duration = 1.00

        self.force = np.zeros(self.dofs)
        self.force_inter = None
        self.interface_dof = None
        self.nsteps = 100

        self.tag = 0
        self.k = [1e+4, 0]  # define MATRIXES
        self.c = [100, 0]  # define MATRIXES
        self.m = [1, 10]  # define MATRIXES
        try:
            self.dir_of_database = "..\\BoogieDB"
            self.access_rights = 0o777
            os.mkdir(self.dir_of_database, self.access_rights)
        except:
            pass
        self.register_variable(Real("duration", causality=Fmi2Causality.parameter, variability=Fmi2Variability.tunable))
        self.register_variable(Real("tag", causality=Fmi2Causality.input))
        self.register_variable(Real("nsteps", causality=Fmi2Causality.input))
        self.dt = self.duration / self.nsteps
        self.t = np.linspace(self.time, self.time + self.duration, self.nsteps + 1)




    def do_step(self, current_time, step_size):

        self.state_current = np.zeros(3 * self.dofs)
        self.dofs = self.dofs + 1
        self.state_current = np.concatenate((self.state_current, np.zeros(3)))
        self.force = np.concatenate((self.force, np.zeros(1)))
        self.M = np.vstack((np.concatenate((self.M, np.zeros([2, 1])), axis=1), np.array([1.0, 0, 0])))
        self.M[0, 2] = 1.0
        self.C = np.vstack((np.concatenate((self.C, np.zeros([2, 1])), axis=1), np.zeros(3)))
        self.K = np.vstack((np.concatenate((self.K, np.zeros([2, 1])), axis=1), np.zeros(3)))

        self.M[0, 0] = self.m[0]
        self.M[1, 1] = self.m[1]

        self.K[0, 0] = self.k[0]
        self.K[0, 1] = -self.k[0]
        self.K[1, 0] = -self.k[0]
        self.K[1, 1] = self.k[0]

        self.C[0, 0] = self.c[0]
        self.C[0, 1] = -self.c[0]
        self.C[1, 0] = -self.c[0]
        self.C[1, 1] = self.c[0]

        h = self.dt
        x = np.zeros([self.dofs, len(self.t)])
        xdot = np.zeros([self.dofs, len(self.t)])
        xddot = np.zeros([self.dofs, len(self.t)])

        if self.tag == 1:
            cp("{}/file1.txt".format(self.dir_of_database), "{}/file0.txt".format(self.dir_of_database))

        try:
            with open('file0.txt') as f:
                self.state_current = []
                for line in f:
                    for x in line.split():
                        self.state_current(float(x))
            x[0:self.dofs, 0] = self.state_current[0:self.dofs]
            xdot[self.dofs:2 * self.dofs, 0] = self.state_current[self.dofs:2 * self.dofs]
            xddot[2 * self.dofs:3 * self.dofs, 0] = self.state_current[2 * self.dofs:3 * self.dofs]
        except:
            pass

        xdot[1, 0] = 100
        # HHT
        af = 1 / 3
        gamma = 1 / 2 + af
        beta = 1 / 4 + 1 / 2 * af
        for i in range(len(self.t) - 1):
            t_af = (1 - af) * self.t[i + 1] + af * self.t[i]
            t_af = self.t[i + 1]
            temp_1 = self.M + (h * gamma) * (1 - af) * self.C + (h ** 2 * beta) * (1 - af) * self.K
            temp_2 = -(np.matmul(self.C, (xdot[:, i] + h * (1 - gamma) * (1 - af) * xddot[:, i])))
            temp_3 = -(np.matmul(self.K, (
                    x[:, i] + h * (1 - af) * xdot[:, i] + h ** 2 * (1 / 2 - beta) * (1 - af) * xddot[:, i])))

            xddot[:, i + 1] = np.linalg.solve(temp_1, temp_2 + temp_3)

            xdot[:, i + 1] = xdot[:, i] + (1 - gamma) * h * xddot[:, i] + (gamma) * h * xddot[:, i + 1]
            x[:, i + 1] = x[:, i] + h * xdot[:, i] + h * h / 2 * (
                    (1 - 2 * beta) * xddot[:, i] + (2 * beta) * xddot[:, i + 1])

        self.state_current[0:self.dofs] = x[0:self.dofs, -1]
        self.state_current[self.dofs:2 * self.dofs] = xdot[0:self.dofs, -1]
        self.state_current[2 * self.dofs:3 * self.dofs] = xddot[0:self.dofs, -1]

        with open("{}/file1.txt".format(self.dir_of_database), "w") as f:
            for items in self.state_current:
                f.write('{}\n'.format(items))

        plt.plot(self.t, x[1])
        plt.show()

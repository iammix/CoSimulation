import matplotlib.pyplot as plt
import numpy as np


class Vehicle(object):

    def __init__(self, mv, mw, c, k, steps, Tn, DTc):
        self.mv = mv
        self.mw = mw
        self.c = c
        self.k = k
        self.steps = steps
        self.Tn = Tn
        self.DTc = DTc
        self.mrr = None
        self.krr = None
        self.crr = None
        self.x = None
        self.xdot = None
        self.xddot = None
        self.M = np.zeros([3, 3])
        self.K = np.zeros([3, 3])
        self.C = np.zeros([3, 3])
        self.dofs = 2
        self.fcons = np.zeros(3)
        self.createState()

    def createMassMatrix(self):
        self.mrr = self.mw
        self.M[0, 0] = self.mw
        self.M[1, 1] = self.mv
        self.M[0, 2] = self.mrr
        self.M[2, 0] = self.mrr

    def createStifnessMatrix(self, h):
        self.krr = self.mrr * (3.14159 / (1000 * h)) * (3.14159 / (1000 * h))
        self.K[0, 0] = self.k
        self.K[0, 1] = -self.k
        self.K[1, 1] = self.k
        self.K[1, 0] = -self.k
        self.K[0, 2] = self.krr
        self.K[2, 0] = self.krr

    def createDampingMatrix(self, h):
        self.crr = 2 * self.mrr * np.sqrt(self.krr / self.mrr)
        # self.crr=self.c
        self.C[0, 0] = self.c
        self.C[0, 1] = -self.c
        self.C[1, 1] = self.c
        self.C[1, 0] = -self.c
        self.C[0, 2] = self.crr
        self.C[2, 0] = self.crr

    def createState(self):
        self.t = np.linspace(self.Tn, self.Tn + self.DTc, self.steps + 1)
        self.x = np.zeros([self.dofs + 1, len(self.t)])
        self.xdot = np.zeros([self.dofs + 1, len(self.t)])
        self.xddot = np.zeros([self.dofs + 1, len(self.t)])

    def setInitialState(self, x0, v0):
        self.x[0, 0] = x0[0]
        self.x[1, 0] = x0[1]
        self.x[2, 0] = x0[2]
        self.xdot[0, 0] = v0[0]
        self.xdot[1, 0] = v0[1]
        self.xdot[2, 0] = v0[2]

    def setInterfaceInput(self, interfaces):
        self.constraint = interfaces

    def getInterfaceOutput(self):
        return self.x[0, self.steps], self.x_dot[0, self.steps], self.xddot[0, self.steps]

    def do_Step(self):
        an = 1 / 4
        bn = 1 / 2
        h = self.DTc / (self.steps)
        self.createMassMatrix()
        self.createStifnessMatrix(h)
        self.createDampingMatrix(h)

        # Initial Acceleration
        self.fcons[2] = self.crr * (self.constraint[0] * self.constraint[1])
        b = -np.matmul(self.K, self.x[:, 0]) - np.matmul(self.C, self.xdot[:, 0]) + self.fcons
        self.xddot[:, 0] = np.linalg.solve(self.M, b)

        for i in range(len(self.t) - 1):
            # Compute RHS
            temp_1 = -np.matmul(self.K, self.x[:, i])
            temp_2 = -np.matmul((self.C + h * self.K), self.xdot[:, i])
            temp_3 = -np.matmul(((1 - bn) * h * self.C + h * h / 2 * (1 - 2 * an) * self.K), self.xddot[:, i])
            self.fcons[2] = self.mrr * (
                    -self.constraint[0] * self.constraint[0] * np.sin(self.constraint[0] * self.t[i + 1])) * \
                            self.constraint[1]
            self.fcons[2] += self.crr * (self.constraint[0] * np.cos(self.constraint[0] * self.t[i + 1])) * \
                             self.constraint[1]
            self.fcons[2] += self.krr * np.sin(self.constraint[0] * self.t[i + 1]) * self.constraint[1]
            b = temp_1 + temp_2 + temp_3 + self.fcons

            # Create Jacobian
            A = (self.M + h * bn * self.C + h * h * an * self.K)

            # Compute Velocity
            self.xddot[:, i + 1] = np.linalg.solve(A, b)

            # Update State
            self.xdot[:, i + 1] = self.xdot[:, i] + (1 - bn) * h * self.xddot[:, i] + (bn) * h * self.xddot[:, i + 1]
            self.x[:, i + 1] = self.x[:, i] + h * self.xdot[:, i] + h * h / 2 * (
                    (1 - 2 * an) * self.xddot[:, i] + (2 * an) * self.xddot[:, i + 1])

        return self.x, self.xdot, self.t

    #def report(self, x, xdot, t):
    #    # for i in range(1,x.shape[0]-1):
    #    fig1 = plt.figure(0)
    #    disp1 = plt.plot(t, x[0, :])
    #    disp2 = plt.plot(t, x[1, :])
    #    plt.xlabel('time [sec]')
    #    plt.ylabel('Displacement [m]')
    #    plt.legend([disp1[0], disp2[0]], ['x1 analytical', 'x2 analytical'])
    #    fig2 = plt.figure(1)
    #    vel1 = plt.plot(t, xdot[0, :])
    #    vel2 = plt.plot(t, xdot[1, :])
    #    plt.xlabel('time [sec]')
    #    plt.ylabel('Velocity [m/sec]')
    #    plt.legend([vel1[0], vel2[0]], ['v1 analytical', 'v2 analytical'])
    #    plt.show()


def main():
    mw = 10.0
    mv = 10000.0
    k0 = 1000000.0
    c0 = 100
    Tn = 0.0
    DTc = 10.0
    steps = 10000
    f = 0.0
    omega = 20
    irr_0 = 0.12
    x = np.array([0.0, 0.0, 0.0])
    v = np.array([0.0, 0.0, 0.0])
    constr = np.array([omega, irr_0])
    oscilator = Vehicle(mv, mw, c0, k0, steps, Tn, DTc)
    oscilator.setInitialState(x, v)
    oscilator.setInterfaceInput(constr)
    xa, xadot, t = oscilator.do_Step()
    # oscilator.report(xa, xadot, t)


if __name__ == "__main__":
    main()

import math
import numpy as np
import matplotlib.pyplot as plt


VALID_TAG = {1, 2}
VALID_ROUGH1 = {0, 1, 2}
VALID_ROUGH2 = {0, 1, 2, 3, 4, 5, 6}


def irregularity(tag, roughness, L, v):
    if tag not in VALID_TAG:
        raise ValueError("tag instance must be one of {}.".format(VALID_TAG))
    if tag == 1:
        if roughness not in VALID_ROUGH1:
            raise ValueError("roughness instance for tag {} must be one of {}.".format(tag, VALID_ROUGH1))
    elif tag == 2:
        if roughness not in VALID_ROUGH2:
            raise ValueError("roughness instance for tag {} must be one of {}.".format(tag, VALID_ROUGH2))
    """
    :param tag: 1 high speed railway German spectra
        :param roughness: 0 no roughness
                          1  very good roughness
                          2 good roughness
    :param tag:2 high speed railway USA spectra
        :param roughness: 0 no roughness
                          1 level 1 roughness
                          2 level 2 roughness-very poor
                          3 level 3 roughness
                          4 level 4 roughness
                          5 level 5 roughness
                          6 level 6 roughness-very good
    :param L: Bridge Length
    :param v: vehicle Velocity
    :return: irregularity vertical displacement profile
    """
    if tag == 1:
        nl = 2 * np.pi / 80  # rad/m, 0.5m
        nh = 2 * np.pi / 0.5  # rad/m, 80m
        if roughness == 0:
            Av = 0
            wr = 0.0206
            wc = 0.8246
        elif roughness == 1:
            Av = 4.032e-7
            wr = 0.0206
            wc = 0.8246
        elif roughness == 2:
            Av = 10.80e-7
            wr = 0.0206
            wc = 0.8246

    elif tag == 2:
        nl = 2 * np.pi / 300  # rad/m, 1.5m
        nh = 2 * np.pi / 1.5  # rad/m, 300m
        if roughness == 0:
            Av = 0
            wc = 0.8245
        elif roughness == 1:
            Av = 1.2107e-4
            wc = 0.8245
        elif roughness == 2:
            Av = 1.0181e-4
            wc = 0.8245
        elif roughness == 3:
            Av = 0.6816e-4
            wc = 0.8245
        elif roughness == 4:
            Av = 0.5376e-4
            wc = 0.8245
        elif roughness == 5:
            Av = 0.2095e-4
            wc = 0.8245
        elif roughness == 6:
            Av = 0.0339e-4
            wc = 0.8245

    N = 2048
    deta_f = (nh - nl) / N
    nk = np.linspace((nl + (nh - nl) / (2 * N)), (nh - (nh - nl) / (2 * N)), num=N)
    faik = []
    for i in range(N):
        faik.append(2 * np.pi * np.random.random())
    ak2 = np.zeros(N)

    for i in range(1, N):
        wn = nk[i]
        if tag == 1:
            Sn = ((Av * wc ** 2) / (wn ** 2 + wr ** 2) / (wn ** 2 + wc ** 2))
        elif tag == 2:
            Sn = ((0.25 * Av * wc ** 2) / (wn ** 2) / (wn ** 2 + wc ** 2))
        ak2[i] = np.sqrt(2 * deta_f * Sn)

    step = 1 / (nh / 2 / np.pi) / v / 2
    number_of_spaces = int(L / v / step)
    t = []
    for i in np.linspace(0, L / v, num=number_of_spaces):
        t.append(i)
    Lt = len(t)

    qkdd = np.zeros((N, Lt))
    for i in range(N):
        for j in range(Lt):
            qkdd[i, j] = -(nk[i]) ** 2 * ak2[i] * np.cos(nk[i] * v * t[j] + faik[i])
    qtdd = np.sum(qkdd, axis=0).tolist()

    qkd = np.zeros((N, Lt))
    for i in range(N):
        for j in range(Lt):
            qkd[i, j] = -(nk[i]) * ak2[i] * np.sin(nk[i] * v * t[j] + faik[i])
    qtd = np.sum(qkd, axis=0).tolist()

    qk = np.zeros((N, Lt))
    for i in range(N):
        for j in range(Lt):
            qk[i, j] = ak2[i] * np.cos(nk[i] * v * t[j] + faik[i])
    qt = np.sum(qk, axis=0).tolist()
    v_t = [i * v for i in t] # generate discrete positioning

    ax = plt.subplot()
    if tag == 1:
        tag = "German"
    else:
        tag = "USA"
    line1= ax.plot(v_t, qt, linewidth=0.5, label='Irregularity {},roughness level {}'.format(tag, roughness))
    plt.xlabel("Length (m)")
    plt.ylabel("Vertical Irregularity (m)")
    ax.legend()
    plt.show()
    return (v_t, qt)


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

    # self.xddot[:,0]= np.array(np.linalg.solve(A,b))

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

        # initial accelaration
        self.fcons[2] = +self.crr * (self.constraint[0] * self.constraint[1])
        b = -np.matmul(self.K, self.x[:, 0]) - np.matmul(self.C, self.xdot[:, 0]) + self.fcons
        self.xddot[:, 0] = np.linalg.solve(self.M, b)

        for i in range(len(self.t) - 1):

            # compute RHS
            temp_1 = -np.matmul(self.K, self.x[:, i])
            temp_2 = -np.matmul((self.C + h * self.K), self.xdot[:, i])
            temp_3 = -np.matmul(((1 - bn) * h * self.C + h * h / 2 * (1 - 2 * an) * self.K), self.xddot[:, i])
            self.fcons[2] = self.mrr * (-self.constraint[0] * self.constraint[0] * np.sin(self.constraint[0] * self.t[i + 1])) * self.constraint[1]
            self.fcons[2] += self.crr * (self.constraint[0] * np.cos(self.constraint[0] * self.t[i + 1])) * self.constraint[1]
            self.fcons[2] += self.krr * np.sin(self.constraint[0] * self.t[i + 1]) * self.constraint[1]
            b = temp_1 + temp_2 + temp_3 + self.fcons

            # create jacobian
            A = (self.M + h * bn * self.C + h * h * an * self.K)

            # compute velocity
            self.xddot[:, i + 1] = np.linalg.solve(A, b)

            # update state
            self.xdot[:, i + 1] = self.xdot[:, i] + (1 - bn) * h * self.xddot[:, i] + (bn) * h * self.xddot[:, i + 1]
            self.x[:, i + 1] = self.x[:, i] + h * self.xdot[:, i] + h * h / 2 * (
                    (1 - 2 * an) * self.xddot[:, i] + (2 * an) * self.xddot[:, i + 1])

        return self.x, self.xdot, self.t


    def report(self, x, xdot, t):
        # for i in range(1,x.shape[0]-1):
        fig1 = plt.figure(0)
        disp1 = plt.plot(t, x[0, :])
        disp2 = plt.plot(t, x[1, :])
        plt.xlabel('time [sec]')
        plt.ylabel('Displacement [m]')
        plt.legend([disp1[0], disp2[0]], ['x1 analytical', 'x2 analytical'])

        fig2 = plt.figure(1)
        vel1 = plt.plot(t, xdot[0, :])
        vel2 = plt.plot(t, xdot[1, :])
        plt.xlabel('time [sec]')
        plt.ylabel('Velocity [m/sec]')
        plt.legend([vel1[0], vel2[0]], ['v1 analytical', 'v2 analytical'])
        plt.show()


def main():
    mw = 10.0
    mv = 10000.0
    k0 = 1000000.0
    c0 = 100
    Tn = 0.0
    DTc = 10.0
    steps = 10000
    f = 0.0
    #irregularity
    tag = 1
    roughness = 1
    length = 100
    velocity = 5
    irregularity(tag, roughness, length, velocity)
    omega = 20
    irr_0 = 0.12
    x = np.array([0.0, 0.0, 0.0])
    v = np.array([0.0, 0.0, 0.0])
    constr = np.array([omega, irr_0])
    oscilator = Vehicle(mv, mw, c0, k0, steps, Tn, DTc)
    oscilator.setInitialState(x, v)
    oscilator.setInterfaceInput(constr)
    xa, xadot, t = oscilator.do_Step()
    #oscilator.report(xa, xadot, t)


if __name__ == "__main__":
    main()
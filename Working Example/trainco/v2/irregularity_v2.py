import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
from scipy import interpolate

VALID_TAG = {1, 2}
VALID_ROUGH1 = {0, 1, 2}
VALID_ROUGH2 = {0, 1, 2, 3, 4, 5, 6}

def irregularity(tag, roughness, L, v, nofp):
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
    :param numbers: number of points to create the cubic spline for the irregularity x, v, a profile
    :return: irregularity vertical displacement profile
    """
    if tag not in VALID_TAG:
        raise ValueError("tag instance must be one of {}.".format(VALID_TAG))
    if tag == 1:
        if roughness not in VALID_ROUGH1:
            raise ValueError("roughness instance for tag {} must be one of {}.".format(tag, VALID_ROUGH1))
    elif tag == 2:
        if roughness not in VALID_ROUGH2:
            raise ValueError("roughness instance for tag {} must be one of {}.".format(tag, VALID_ROUGH2))
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

    #Cubic Spline Points on bridge deck(discrete positions)
    xc = np.arange(0, L + 1/nofp, 1/nofp)

    # Create Cubic Spline for vertical displacement irregularity profile
    disp_cs = CubicSpline(v_t, qt)

    # Create Cubic Spline for vertical Velocity irregularity profile
    vel_cs = CubicSpline(v_t, qtd)

    # Create Cubic Spline for vertical Acceleration irregularity profile
    acc_cs = CubicSpline(v_t, qtdd)

    # Generate Plots
    if tag == 1:
        tag = "German"
    else:
        tag = "USA"
    plt.figure(1)
    plt.plot(v_t, qt, 'o', label="Calculated Data, {} Irreg. Spectra, Roughness Level {}".format(tag, roughness))
    plt.plot(xc, disp_cs(xc), label="Cubic Spline, {} Irreg. Spectra, Roughness Level {}".format(tag, roughness))
    plt.xlabel("Length(m)")
    plt.ylabel("Vertical Irregularity (m)")
    plt.legend()

    plt.figure(2)
    plt.plot(v_t, qtd, 'o', label="Calculated Data, {} Irreg. Spectra, Roughness Level {}".format(tag, roughness))
    plt.plot(xc, vel_cs(xc), label="Cubic Spline, {} Irreg. Spectra, Roughness Level {}".format(tag, roughness))
    plt.xlabel("Length(m)")
    plt.ylabel("Vertical Irregularity (m/sec)")
    plt.legend()

    plt.figure(3)
    plt.plot(v_t, qtdd, 'o', label="Calculated Data, {} Irreg. Spectra, Roughness Level {}".format(tag, roughness))
    plt.plot(xc, acc_cs(xc), label="Cubic Spline, {} Irreg. Spectra, Roughness Level {}".format(tag, roughness))
    plt.xlabel("Length(m)")
    plt.ylabel("Vertical Irregularity (m/sec^2)")
    plt.legend()

    plt.show()



def main():
    irregularity(1, 1, 10000, 4, 100)

if __name__ == "__main__":
    main()
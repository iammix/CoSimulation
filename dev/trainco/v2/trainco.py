#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Kleanthi Pontiki                                               

import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
import scipy.linalg
# import two_dof_oscillator_v2 as analytical
import openseespy.opensees as ops

import coupled_simulation_v2 as cs
import Irreg_fun


# Train plain model
class bridge(object):
    def __init__(self, elenum, vel, L, A, MassPerLength, E, Izz, interface_coef):
        self.vel = vel
        self.elenum = elenum
        self.interface_coef = interface_coef
        self.nodenum = elenum + 1
        self.state_previous = np.zeros((self.nodenum, 9))  # each node has 3 dofs * 3 states ( x,v,a)
        self.state_current = np.zeros((self.nodenum, 9))
        self.time = 0.0
        self.duration = 0.0
        self.force_inter = None
        self.t = None
        self.nsteps = 0
        self.dt = 0
        self.state = 0
        self.interface_dof = None
        self.initialize_model()
        self.built(MassPerLength, L, A, E, Izz)
        self.set_initial()

    def initialize_model(self):
        ops.wipe()
        # define model
        ops.model('basic', '-ndm', 2, '-ndf', 3)
        # Create database
        ops.database("File", "Opensees_model")

    def built(self, M, L, A, E, Izz):
        # construct nodes without mass
        elelength = L / self.elenum
        temp = 0.0
        for i in range(1, self.nodenum + 1):
            ops.node(i, temp, 0.0)
            temp = temp + elelength
            # ops.fix(i,1,1,1)
        ops.fix(1, 1, 1, 0)  # f
        ops.fix(self.nodenum, 1, 1, 0)  #
        # define material
        ops.uniaxialMaterial("Elastic", 1, 1)  # E=1 ==> A=k Damping? viscoous damper material
        # Create elements
        ops.geomTransf('Linear', 1)
        for i in range(1, self.nodenum):
            ops.element('elasticBeamColumn', i, *[i, i + 1], A, E, Izz, 1, '-mass', M)
        # opsplt.plot_model()

    def set_initial(self):
        for i in range(1, self.elenum + 2):
            ops.setNodeDisp(i, 2, 0)
            ops.setNodeVel(i, 2, 0)
            ops.setNodeAccel(i, 2, 0)

    def set_interface_input(self, T, lc, nsteps):
        self.duration = T
        self.nsteps = nsteps
        self.set_timestep()
        if self.state > 0:
            ops.restore(self.state)
        ops.setTime(self.time)
        try:
            for i in range(0, self.nsteps + 1):
                ops.remove('timeSeries', i)
                ops.remove("loadPattern", i)
        except:
            pass

        tstart = self.time - self.dt
        for i in range(0, self.nsteps + 1):
            factor = self.interface_coef * lc[0] + (
                        self.interface_coef * lc[1] - self.interface_coef * lc[0]) / self.nsteps * i
            ops.timeSeries('Path', i, '-values', 0, factor, 0, '-time', tstart, tstart + 2 * self.dt, 4 * self.dt,
                           '-prependZero')
            ops.pattern("Plain", i, i)
            next_id = 0
            xload = self.vel * (self.time + i * self.dt)
            for j in range(1, self.nodenum + 1):
                if ops.nodeCoord(j, 1) > xload:
                    next_id = j
                    break
            ops.eleLoad('-ele', next_id - 1, '-type', '-beamPoint', 1, (xload - ops.nodeCoord(next_id - 1, 1)) / (
                        ops.nodeCoord(next_id, 1) - ops.nodeCoord(next_id - 1, 1)))
            tstart = tstart + self.dt

    def set_timestep(self):
        self.dt = self.duration / self.nsteps

    def solve(self):
        ops.wipeAnalysis()
        ops.constraints('Penalty', 1e+10, 1e+10)
        # ops.constraints('Lagrange',1e+10)
        ops.system('FullGeneral')
        ops.numberer("RCM")
        ops.integrator('HHT', 0.67)
        # ops.integrator('Newmark', 1/2,1/4,'-formD','A')
        ops.algorithm("Linear")
        ops.analysis("Transient")
        nPts = self.nsteps
        dt = self.dt
        tFinal = self.time + nPts * dt
        tCurrent = self.time
        ok = 0
        # Perform the transient analysis
        time = [tCurrent]
        # U= [0.0]
        while ok == 0 and tCurrent < (tFinal - dt / 100):
            ok = ops.analyze(1, dt)
            tCurrent = ops.getTime()
            # print(ops.getLoadFactor(1))
            # time.append(tCurrent)
            # U.append(ops.nodeDisp(3,2))
        # plt.plot(time,U)
        # plt.show()
        pass

    def set_update(self):
        self.state = 1
        ops.save(self.state)
        self.time = ops.getTime()

    def get_interface_output(self):
        pos = 1.0 * self.vel * ops.getTime()
        for i in range(1, self.nodenum + 1):
            if ops.nodeCoord(i, 1) > pos:
                node1 = i - 1
                node2 = i
                break
            
        disp1 = ops.nodeDisp(node1, 2)
        disp2 = ops.nodeDisp(node2, 2)
        phi1 = ops.nodeDisp(node1, 3)
        phi2 = ops.nodeDisp(node2, 3)
        x = CubicSpline([0, 1], [disp1, disp2], bc_type=((1, phi1), (1, phi2)))
        point = (pos - ops.nodeCoord(node1, 1)) / (ops.nodeCoord(node2, 1) - ops.nodeCoord(node1, 1))
        disp = x(point).item(0)

        disp1 = ops.nodeVel(node1, 2)
        disp2 = ops.nodeVel(node2, 2)
        phi1 = ops.nodeVel(node1, 3)
        phi2 = ops.nodeVel(node2, 3)
        x = CubicSpline([0, 1], [disp1, disp2], bc_type=((1, phi1), (1, phi2)))
        vel = x(point).item(0)

        disp1 = ops.nodeAccel(node1, 2)
        disp2 = ops.nodeAccel(node2, 2)
        phi1 = ops.nodeAccel(node1, 3)
        phi2 = ops.nodeAccel(node2, 3)
        x = CubicSpline([0, 1], [disp1, disp2], bc_type=((1, phi1), (1, phi2)))
        acc = x(point).item(0)

        return disp, vel, acc


class cosimulation(object):

    def __init__(self, nsteps, nsubsteps, T, model_1, model_2, modelsdict, tolerance, r, rdot, rddot, vel,
                 method='Jacobi', coupling='Force-Force'):
        self.nsteps = nsteps
        self.nsubsteps = nsubsteps
        self.T = T
        self.models = modelsdict
        self.method = method
        self.coupling = coupling
        self.converged_state = np.zeros(6)  # x1 x1dot x1ddot x2 x2dot x2ddot
        self.current_state = np.zeros(6)  # x1 x1dot x1ddot x2 x2dot x2ddot
        self.time = np.linspace(0, self.T, self.nsteps + 1)
        self.H = self.T / self.nsteps
        self.A = None
        ### Stored Variables??? ####
        self.x = np.zeros([2, len(self.time)])
        self.xdot = np.zeros([2, len(self.time)])
        self.xddot = np.zeros([2, len(self.time)])
        self.r = np.array(r)
        self.rdot = np.array(rdot)
        self.rddot = np.array(rddot)
        self.vel = vel
        self.timestep = 0
        self.sens = None
        self.converge = False
        self.tolerance = tolerance

    # def set_init(self,IIC):
    #     self.current_state=IIC
    #     self.converged_state=IIC

    # def set_solution(self):
    #     self.current_state=1*self.converged_state
    #     self.x[:,self.timestep]= np.array([self.current_state[0][0],self.current_state[1][0]])
    #     self.xdot[:,self.timestep]= np.array([self.current_state[0][1],self.current_state[1][1]])
    #     self.xddot[:,self.timestep]= np.array([self.current_state[0][2],self.current_state[1][2]])

    def get_result(self):
        return self.x, self.xdot, self.xddot

    def set_A(self):
        if self.coupling == 'Force-Force':
            self.A = np.zeros((1, len(self.time)))  # lc
        elif self.coupling == 'Force-Disp':
            pass
        else:
            print('The coupling scenario is not supported')

    def set_sens(self):
        if self.A.shape[0] == 1:
            self.sens = np.zeros([2, 3])  # [x1 xd1 xdd1] , [x2 xd2 xdd2 ]
        # else:
        # self.sens=np.zeros([self.A.shape[0],3]) # in case of dd :[ x1 xd1 xdd1], [x21 xd21 xdd21], [x22 xd22 xdd22] etc.

    def get_sens(self, model, i, temp, dA):
        if self.A.shape[0] == 1:
            model.set_interface_input(self.H, [self.A[0, i], self.A[0, i + 1] + dA], self.nsubsteps)
            model.solve()
            self.sens[temp, 0], self.sens[temp, 1], self.sens[temp, 2] = model.get_interface_output()
        # elif self.A.shape[0]==3:
        #     pass

    def check_convergence(self, i):
        if self.A.shape[0] == 1:
            res_ = self.x[1, i + 1] - self.x[0, i + 1] + self.r[i + 1]
            res_d = self.xdot[1, i + 1] - self.xdot[0, i + 1] + self.rdot[i + 1]
            res_dd = self.xddot[1, i + 1] - self.xddot[0, i + 1] + self.rddot[i + 1]
            omega = 100
            if abs(omega * omega * res_ + 2 * omega * res_d + res_dd) <= self.tolerance:  #### R ####
                self.converge = True

    def predict(self, i):
        self.A[:, i + 1] = 1.0 * self.A[:, i]

    def find_dA(self, i):
        dA = np.zeros(self.A.shape[0])
        for j in range(len(self.A)):
            if self.A.shape[0] == 1:
                dA = max(self.A[0, i + 1] / 10, 10 ** (-1))
            else:
                dA[j] = max(self.A[j, i + 1] / 10, 10 ** (-1))
        return dA

    def get_model_sol(self, model, i, temp):
        if self.A.shape[0] == 1:
            model.set_interface_input(self.H, [self.A[0, i], self.A[0, i + 1]], self.nsubsteps)
            model.solve()
            self.x[temp, i + 1], self.xdot[temp, i + 1], self.xddot[temp, i + 1] = model.get_interface_output()

    def interface_vars(self, i, dA):
        if self.A.shape[0] == 1:
            dxw = (self.sens[0, 0] - self.x[0, i + 1]) / dA
            dxb = (self.sens[1, 0] - self.x[1, i + 1]) / dA
            dxw_d = (self.sens[0, 1] - self.xdot[0, i + 1]) / dA
            dxb_d = (self.sens[1, 1] - self.xdot[1, i + 1]) / dA
            dxw_dd = (self.sens[0, 2] - self.xddot[0, i + 1]) / dA
            dxb_dd = (self.sens[1, 2] - self.xddot[1, i + 1]) / dA
            res_ = self.x[1, i + 1] - self.x[0, i + 1] + self.r[i + 1]
            res_d = self.xdot[1, i + 1] - self.xdot[0, i + 1] + self.rdot[i + 1]
            res_dd = self.xddot[1, i + 1] - self.xddot[0, i + 1] + self.rddot[i + 1]
            omega = 100
            factor = (dxw - dxb) * omega * omega + 2 * omega * (dxw_d - dxb_d) + (dxw_dd - dxb_dd)
            try:
                self.A[0, i + 1] = self.A[0, i + 1] + (omega * omega * res_ + 2 * omega * res_d + res_dd) / factor
            except:
                self.A[0, i + 1] = self.A[0, i + 1] * 1.01

    def solver(self):
        self.set_A()
        self.set_sens()
        for i in range(len(self.time) - 1):
            self.timestep = i
            self.predict(i)
            dA = self.find_dA(i)
            self.converge = False
            iter = 0
            while (self.converge == False) and (iter <= 50):
                temp = 0
                for model in self.models.values():
                    self.get_sens(model, i, temp, dA)
                    self.get_model_sol(model, i, temp)
                    if self.method == 'Gauss-Scheidel':
                        self.interface_vars(i, dA)
                    temp = temp + 1
                self.check_convergence(i)
                if self.converge == False and iter <= 20:
                    self.interface_vars(i, dA)
                iter = iter + 1

                if iter == 20:
                    print('Max iterations')

                    # update models
            for j in self.models.keys():
                self.models[j].set_update()

    def report(self):
        for i in range(0, 2):
            fig = plt.figure(0)
            plt.plot(self.time, self.x[i, :])
            plt.xlabel('time [sec]')
            plt.ylabel('Displacement [m]')

        fig = plt.figure(1)
        plt.plot(self.time, self.x[0, :] - self.x[1, :])
        plt.xlabel('time [sec]')
        plt.ylabel('Velocity [m/sec]')


def main():
    Mb = 50
    Mw = 2
    k = 1000
    c = 0
    dofs = 2
    m = np.array([Mb, Mw])
    k = np.array([0, k, 0])
    c = np.array([0, c, 0])
    IC = np.array([0, 0, 0, 0, 0, 0])  # IC1=np.array([x1,x2,u1,u2,a1,a2,....])

    element_number = 10
    train_vel = 10
    Length = 100
    A = 1
    Mass = 50
    E = 30000000
    Izz = 30
    model_2 = bridge(element_number, train_vel, Length, A, Mass, E, Izz, -1)

    model_1 = cs.Model(m, c, k, dofs, 1, 1)
    model_1.set_initial(IC)

    modelsdict = {'0': model_1,
                  '1': model_2}

    nsteps = 200  # CS steps
    nsubsteps = 10  # internal steps for each model
    T = Length / train_vel / 2
    tol = 0.0001
    r, rdot, rddot, tt = Irreg_fun.Irreg_fun(train_vel, nsteps, Length / 1.2)

    cosim = cosimulation(nsteps, nsubsteps, T, model_1, model_2, modelsdict, tol, r, rdot, rddot, train_vel)
    cosim.solver()
    cosim.report()
    # plt.plot(tt,r)
    plt.show()


if __name__ == "__main__":
    main()

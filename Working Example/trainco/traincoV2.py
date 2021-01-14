#!C:/users/iammix/Anaconda3/python
# -*- coding: utf-8 -*-
# author: Kleanthi Pontiki

import math
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
import scipy.linalg
import openseespy.opensees as ops
from openseespy.postprocessing import Get_Rendering
import mysql.connector
import sqlite3
import os
#from mpi4py.futures import MPICommExecutor
#import two_dof_oscillator as analytical
#import opdll.opensees as ops
#import coupled_simulation_v2 as cs
#ops = Py.Import("opensees.pyd")
# Create SQL database


def create_connection(db_file):
    import sqlite3
    from sqlite3 import Error
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()




class AnimateLoad(object):
    import numpy as np
    import matplotlib.patches as patches
    import matplotlib.pyplot as plt
    from matplotlib import animation
    import matplotlib.transforms as mtransforms



    def init():
        line.set_data([], [],'o-',lw=2)
        time_text.set_text('')
        return line, time_text
    
    def animate(i):
        pass


#Train plain model
class Bridge(object):
    def __init__(self, elenum, vel, L, A, MassPerLength, E, Izz):
        self.vel = vel
        self.elenum = elenum
        self.nodenum = elenum + 1
        self.state_previous = np.zeros((self.nodenum, 9)) #each node has 3 dofs * 3 states (x, v, a)
        self.state_current = np.zeros((self.nodenum, 9))
        self.time = 0.0
        self.duration = 0.0
        # self.force = np.zeros()
        self.force_inter = None
        self.t = None
        self.nsteps = 0
        self.dt = 0
        self.state = 0
        self.interface_dof = None
        # self.set_interface_dof(interface_dof)
        self.initialize_model()
        self.built(MassPerLength, L, A, E, Izz)
        self.set_initial()

    def initialize_model(self):
        ops.wipe()
        #define model
        ops.model('basic', '-ndm', 2, '-ndf', 3)
        #Create database
        #ops.database('MySQL', 'File')

    def built(self, M, L, A, E, Izz):

        #construct nodes without mass
        elelength = L / self.elenum
        temp = 0
        for i in range(1, self.nodenum + 1):
            ops.node(i, temp, 0.0)
            temp = temp + elelength
        ops.fix(1, 1, 1, 1) #fix 1st node on x,y 
        ops.fix(self.nodenum, 1, 1, 1) #fix last node on y

        #define material, for elasticBeamColumn no material definition needed
        #ops.uniaxialMaterial("Elastic", 1, 20000000000) #E=1 ==> A=k Damping? viscoous damper material

        #Create elements
        ops.geomTransf('Linear', 1, 0, 0, 1)
        for i in range(1, self.nodenum):
            ops.element('elasticBeamColumn', i, i, i + 1, A, E, Izz, 1, '-mass', M)

    def set_initial(self):

        for i in range(1, self.elenum + 2):

            ops.setNodeDisp(i, 2, 0)
            ops.setNodeVel(i, 2, 0)
            ops.setNodeAccel(i, 2, 0)

    def set_interface_input(self, T, lc, nsteps):

        self.duration = T
        self.nsteps = nsteps
        self.set_timestep()
        self.xload = 0
        #self.t = np.linspace(self.time, self.time + self.duration, self.nsteps + 1)

        if self.state > 0:
            ops.restore(self.state)
            ops.setTime(self.time)
        try:
            ops.remove('timeSeries', 1)
            ops.remove("loadPattern", 1)
        except:
            pass

        tstart = ops.getTime() - self.dt

        for i in range(1, self.nsteps + 1):

            ops.timeSeries('Triangle', i, tstart, tstart + 2 * self.dt, 4 * self.dt,\
                '-factor', lc[0] + (lc[1] - lc[0]) / self.nsteps * i)
            ops.pattern("Plain", i, i) 
            next_id = 0
            self.xload = self.vel * (ops.getTime() + i * self.dt)

            for j in range(1, self.nodenum + 1):
                if ops.nodeCoord(j, 1) >= self.xload:
                    next_id = j 
                    break

            ops.eleLoad('-ele', next_id-1, '-type', '-beamPoint', 1, (self.xload-ops.nodeCoord(next_id - 1, 1))/(ops.nodeCoord(next_id, 1) - ops.nodeCoord(next_id - 1,1)))
            tstart = tstart + self.dt

    def set_timestep(self):
        self.dt = self.duration / self.nsteps

    def solve(self): 
        ops.wipeAnalysis()
        ops.constraints('Plain')
        ops.system("ProfileSPD")
        ops.numberer("RCM")
        ops.integrator("Newmark", 1/4, 1/2, 'A')
        ops.algorithm("Newton")
        ops.test("NormDispIncr", 1e-6, 10000, 2)
        ops.analysis("Transient")
        nPts = self.nsteps ###
        dt = self.dt ###
        tFinal = self.time + nPts * dt ###
        tCurrent = ops.getTime() ###
        ok = 0 ###

        # Perform the transient analysis
        time=[tCurrent]
        U= [0.0]
        ops.database('File', 'Train-State')


        while ok == 0 and tCurrent < (tFinal - dt / 100):
            ok = ops.analyze(1, dt)
            tCurrent = ops.getTime()
            print(ops.getLoadFactor(1))
            time.append(tCurrent)
            U.append(ops.nodeDisp(3,2))

            #ops.save(1)

        plt.plot(time, U)
        Get_Rendering.plot_model()
        plt.show()

        ops.setTime(self.time+self.duration)
        # self.state_current[0]=ops.nodeDisp(self.interface_dof,1)
        # self.state_current[1]=ops.nodeVel(self.interface_dof,1)
        # self.state_current[2]=ops.nodeAccel(self.interface_dof,1)

    def set_update(self):
        self.state = self.state + 1
        ops.save(self.state)
        self.state_previous = 1.0 * self.state_current
        self.time = ops.getTime()

    def get_interface_output(self):
        return self.state_current[0], self.state_current[1], self.state_current[2]



def main():
    dir_path = os.getcwd()
    create_connection(dir_path+"/test.db")
    Mb = 10.0
    Mw = 10.0
    k = 10.0
    c = 0.0
    dofs = 2
    m = np.array([Mb, Mw])
    k = np.array([0 , k, 0])
    c = np.array([0 , c, 0])
    IC = np.array([0, 0, 0, 0, 0, 0]) #IC1=np.array([x1, x2, u1, u2, a1, a2,....])
    # Number of Elements, Velocity, Length, Section Area, Mass Per Lenght, Young Modulus, Izz
    B = Bridge(10, 5, 20, 1, 10, 10, 1)
    B.set_interface_input(3.9, np.array([-10 ,-10]), 10)
    B.solve()
    # train=cs.Model(m,c,k,dofs,1,1)
    # train.set_initial(IC)

if __name__ == "__main__":
    #with MPICommExecutor() as executor:
    main()
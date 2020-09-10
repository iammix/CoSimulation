import math
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
# import scipy.linalg
# import two_dof_oscillator as analytical
import openseespy.opensees as ops
from openseespy.postprocessing import Get_Rendering


# import coupled_simulation_v2 as cs

# Train plain model
class Bridge(object):
    def __init__(self, elenum, vel, L, A, MassPerLength, E, Izz):
        self.vel = vel
        self.elenum = elenum
        self.nodenum = elenum + 1
        self.state_previous = np.zeros((self.nodenum, 9))  # each node has 3 dofs * 3 states ( x,v,a)
        self.state_current = np.zeros((self.nodenum, 9))
        self.time = 0.0
        self.duration = 0.0
        # self.force=np.zeros()
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
        # define model
        ops.model('basic', '-ndm', 2, '-ndf', 3)
        # Create database
        ops.database("File", "C://Opensees_model")

    def built(self, M, L, A, E, Izz):
        # construct nodes without mass
        elelength = L / self.elenum
        temp = 0
        for i in range(1, self.nodenum + 1):
            ops.node(i, temp, 0.0)
            temp = temp + elelength
        ops.fix(1, 1, 1, 0)  # fix 1st node on x,y
        ops.fix(self.nodenum, 0, 1, 0)  # fix last node on y
        # define material
        #ops.uniaxialMaterial("Elastic", 1, 1)  # E=1 ==> A=k Damping? viscoous damper material
        # Create elements
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
        self.interface_coef = 1
        # self.t=np.linspace(self.time,self.time+self.duration,self.nsteps+1)
        if self.state > 0:
            ops.restore(self.state)
            ops.setTime(self.time)
        try:
            for i in range(0, self.nsteps + 1):
                ops.remove('timeSeries', i)
                ops.remove("loadPattern", i)
        except:
            pass
        tstart = ops.getTime() - self.dt
        for i in range(0, self.nsteps + 1):
            factor = (lc[0] + (lc[1] - lc[0]) / self.nsteps * i)
            ops.timeSeries('Path', i, '-values', 0, factor, 0, '-time', tstart, tstart + 2 * self.dt, 4 * self.dt, "-prependZero")
            ops.pattern("Plain", i, i)
            next_id = 0
            xload = self.vel * (ops.getTime() + i * self.dt)
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
        ops.constraints('Plain')
        ops.system('ProfileSPD')
        ops.numberer('Plain')
        ops.integrator('Newmark', 1 / 4, 1 / 2, "A")
        ops.algorithm('Linear')
        ops.test('NormUnbalance', 1e-5, 100, 2)
        ops.analysis('VariableTransient')
        nPts = self.nsteps
        dt = self.dt
        tFinal = self.time + nPts * dt
        tCurrent = self.time
        ok = 0
        # Perform the transient analysis
        time = [tCurrent]
        U = [0.0]
        while ok == 0 and tCurrent < tFinal - dt / 100:
            ok = ops.analyze(1, dt)
            tCurrent = ops.getTime()
            print(ops.getLoadFactor(1))
            time.append(tCurrent)
            U.append(ops.nodeDisp(3, 2))
        plt.plot(time, U)
        plt.show()

        ops.setTime(self.time + self.duration)
        # self.state_current[0]=ops.nodeDisp(self.interface_dof,1)
        # self.state_current[1]=ops.nodeVel(self.interface_dof,1)
        # self.state_current[2]=ops.nodeAccel(self.interface_dof,1)

    def set_update(self):
        self.state = 1
        ops.save(self.state)
        self.state_previous = 1.0 * self.state_current
        self.time = ops.getTime()

    def get_interface_output(self):
        return self.state_current[0], self.state_current[1], self.state_current[2]


def main():
    Mb = 10
    Mw = 10
    k = 10
    c = 0
    dofs = 2
    m = np.array([Mb, Mw])
    k = np.array([0, k, 0])
    c = np.array([0, c, 0])
    IC = np.array([0, 0, 0, 0, 0, 0])  # IC1=np.array([x1,x2,u1,u2,a1,a2,....])

    B = Bridge(4, 5, 20, 1, 1, 10000, 1)
    lc = np.array([-10, -10])
    B.set_interface_input(3.9, lc, 10)
    B.solve()
    # train=cs.Model(m,c,k,dofs,1,1)
    # train.set_initial(IC)


if __name__ == "__main__":
    main()

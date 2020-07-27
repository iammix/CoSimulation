class openseesmodel(object):
    def __init__(self,m,c,k,dofs,interface_dof,IC):
        self.dofs =dofs 
        self.state_previous=np.zeros(3)
        self.state_current=np.zeros(3)
        self.time=0.0
        self.duration=0.0
        self.force=np.zeros(dofs)
        self.force_inter=None
        self.t =None
        self.nsteps=0
        self.dt=0
        self.state=0
        self.interface_dof=None
        self.set_interface_dof(interface_dof)
        self.initialize_model()
        self.built(m,k,c,self.dofs)
        self.set_initial(IC)
    
    def set_interface_dof(self,interface_dof):
        self.interface_dof=interface_dof+1

    def initialize_model(self):
        ops.wipe()
        #define model
        ops.model('basic', '-ndm', 2, '-ndf', 2)
        #Create database
        ops.database("File", "Opensees_model")
        


    def built(self,m,k,c,dofs):
        m=np.append(m,[0])
        k=np.append(k,[0])
        #construct nodes without mass
        for i in range(2,self.dofs+2,1):
            ops.node(i,i-1,0.0)
            ops.fix(i,0,1) #fix every node on y direction
        ops.node(1,0.0,0.0)
        ops.fix(1,1,1) #fix the first node on every direction (universal)    
        #create mass on nodes
        for i in range(2,self.dofs+2,1):
            mnode=1.0*m[i-2]
            ops.mass(i,mnode)
        #define material
        ops.uniaxialMaterial("Elastic", 1, 1)#E=1 ==> A=k Damping? viscoous damper material
        #Create elements
        for i in range(1,self.dofs+1,1):
            knode=1.0*k[i-1]
            ops.element('Truss',i,i,i+1,knode,1)
       # ops.timeSeries("Constant", 1)
       # ops.pattern("Plain", 1, 1) #plain, pattern id=1, on time series with id=1 ???
        
        

    def set_initial(self,IC):
        for i in range(1,self.dofs+1):
            ops.setNodeDisp(i+1,1,1.0*IC[0+(i-1)])
            ops.setNodeVel(i+1,1,1.0*IC[1+(i-1)])
            ops.setNodeAccel(i+1,1,1.0*IC[2+(i-1)])
    
    def set_interface_input(self,T,lc,nsteps):
        self.duration=T
        self.nsteps=nsteps
        self.set_timestep()
        #self.t=np.linspace(self.time,self.time+self.duration,self.nsteps+1)
        if self.state>0:
            ops.restore(self.state)
            ops.setTime(self.time)
        try:
            ops.remove('timeSeries',1)
            ops.remove("loadPattern", 1)
        except:
            pass
        ops.timeSeries('Path',1, '-dt',self.duration, '-values',lc[0],lc[-1], '-time',self.time,self.time+self.duration,'-useLast')
        ops.pattern("Plain", 1, 1) #plain, pattern id=1, on time series with id=1 ???
        ops.load(self.interface_dof, 1, 0)
        
    def set_timestep(self):
        self.dt=self.duration/self.nsteps


    def solve(self): 
        ops.wipeAnalysis()
        ops.constraints('Plain') 
        ops.system("BandSPD") 
        ops.numberer("RCM")
        ops.integrator("Newmark", 1/4, 1/2,"A")
        ops.algorithm("Linear")
        ops.analysis("Transient")
        nPts=self.nsteps
        dt=self.dt
        tFinal = self.time+nPts*dt
        tCurrent = ops.getTime()
        ok = 0
        # Perform the transient analysis
        while ok == 0 and   tCurrent < tFinal-dt/100:
            ok = ops.analyze(1, dt)
            tCurrent = ops.getTime()
        ops.setTime(self.time+self.duration)
        self.state_current[0]=ops.nodeDisp(self.interface_dof,1)
        self.state_current[1]=ops.nodeVel(self.interface_dof,1)
        self.state_current[2]=ops.nodeAccel(self.interface_dof,1)

        
    def set_update(self):
        self.state=self.state+1
        ops.save(self.state)
        self.state_previous=1.0*self.state_current
        self.time=ops.getTime()
    
    def get_interface_output(self):
        return self.state_current[0],self.state_current[1],self.state_current[2]
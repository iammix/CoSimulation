import math
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
import scipy.linalg


#Model Class: Objects of each individual model defined by their basic attributes and solving methods

class Model(object):
    def __init__(self,m,c,k,dofs,interface_dof,interface_coef,intergrator='Newmark',lagrange=False):
        self.dofs =dofs 
        self.M=np.zeros([dofs,dofs])
        self.K=np.zeros([dofs,dofs])
        self.C=np.zeros([dofs,dofs])
        self.state_previous=np.zeros(3*dofs) #last state at timestep Tn np.array([x xdot xddot])
        self.state_current =np.zeros(3*dofs) #new state at timestep Tn+1 np.array([x xdot xddot])
        self.time=0.0 
        self.duration=0.0
        self.force=np.zeros(dofs)
        self.force_inter=None
        self.t =None
        self.nsteps=0
        self.dt=0
        self.coef=interface_coef
        self.intergrator=intergrator
        #set system
        self.set_system(m,c,k)
        self.interface_dof=None
        self.set_interface_dof(interface_dof)
        if lagrange==True:
            self.reform()
            self.lagrange=lagrange

    def  reform(self):
        self.dofs=self.dofs+1
        self.state_previous=np.concatenate((self.state_previous,np.zeros(3)))
        self.state_current=np.concatenate((self.state_current,np.zeros(3)))
        self.force=np.concatenate((self.force,np.zeros(1)))
        self.M=np.vstack((np.concatenate((self.M,np.zeros([2,1])),axis=1),np.array([1.0,0,0])))
        self.M[0,2]=1.0
        self.C=np.vstack((np.concatenate((self.C,np.zeros([2,1])),axis=1),np.zeros(3)))
        self.K=np.vstack((np.concatenate((self.K,np.zeros([2,1])),axis=1),np.zeros(3)))


    def set_interface_dof(self,interface_dof): #dof on which the orchistrator will derive results
        self.interface_dof=interface_dof

    def set_system(self,m,c,k): 
        k=np.append(k,[0])
        c=np.append(c,[0])
        for i in range(self.dofs):
                self.M[i,i]= m[i]
                self.K[i,i]= k[i]+k[i+1]
                self.C[i,i]= c[i]+c[i+1]
        for i in range(self.dofs-1):
                self.K[i,i+1]=-k[i+1]
                self.K[i+1,i]=-k[i+1]
                self.C[i,i+1]=-c[i+1]
                self.C[i+1,i]=-c[i+1]

    def set_initial(self,IC): #sets initial conditions
        self.state_previous=IC
    
    def set_update(self):  
        self.state_previous=1*self.state_current
        self.time=1*self.time+1*self.duration
    
    def set_timestep(self):
        self.dt=self.duration/self.nsteps
    
    def get_interface_output(self):
        return self.state_current[self.interface_dof-1],self.state_current[self.dofs+self.interface_dof-1],self.state_current[2*self.dofs+self.interface_dof-1]

    def set_interface_input(self,T,lc,nsteps):
        self.duration=T
        self.nsteps=nsteps
        self.set_timestep()
        self.t=np.linspace(self.time,self.time+self.duration,self.nsteps+1)
        self.force_inter= interpolate.interp1d([self.t[0], self.t[-1]],[self.coef*lc[0], self.coef*lc[-1]])

    def get_lagrange_mul(self):
        return self.state_current[-1]

    def solve(self): 
        h=self.dt
        x=np.zeros([self.dofs,len(self.t)])
        xdot=np.zeros([self.dofs,len(self.t)])
        xddot=np.zeros([self.dofs,len(self.t)])
        x[0:self.dofs,0] =self.state_previous[0:self.dofs]
        xdot[0:self.dofs,0] =self.state_previous[self.dofs:2*self.dofs]
        xddot[0:self.dofs,0] =self.state_previous[2*self.dofs:3*self.dofs]
        if  self.intergrator=='HHT':
            af=1/3
            gamma=1/2+af
            beta=1/4+1/2*af
            for i in  range(len(self.t)-1):

                t_af=(1-af)*self.t[i+1]+af*self.t[i]
                t_af=self.t[i+1]
                temp_1= self.M + (h * gamma)*(1- af) * self.C + (h**2 * beta)*(1- af) * self.K
                temp_2= -(np.matmul(self.C,(xdot[:,i]+h*(1-gamma)*(1- af)*xddot[:,i])))
                temp_3= -(np.matmul(self.K,(x[:,i]+h*(1- af)*xdot[:,i]+h**2 * (1/2-beta) *(1- af)* xddot[:,i])))
                
                self.force[self.interface_dof-1]=self.force_inter(t_af)
                
                xddot[:,i+1]= np.linalg.solve(temp_1,temp_2+temp_3+self.force)

                xdot[:,i+1] = xdot[:,i] + (1 - gamma) * h * xddot[:,i] + (gamma) * h * xddot[:,i+1]                  
                x[:,i+1] = x[:,i] + h * xdot[:,i] + h * h / 2 * ((1 - 2 * beta) * xddot[:,i] + (2 * beta) * xddot[:,i+1])

        else:  
            an=1/4
            bn=1/2
            for i in range(len(self.t)-1):
                temp_1 = - np.matmul(self.K,x[:,i])
                temp_2 = - np.matmul((bn * self.C + h * self.K), xdot[:,i])
                temp_3 = - np.matmul(((1 - bn) * self.C + h * h / 2 * (1 - 2 * an) * self.K), xddot[:,i])
                self.force[self.interface_dof-1]=self.force_inter(self.t[i+1])  
                b = temp_1 + temp_2 + temp_3 + self.force
                #create jacobian
                A = (self.M + h * bn * self.C + h * h * an * self.K)
                #compute velocity
                xddot[:,i+1] = np.linalg.solve(A, b)
                #update state
                xdot[:,i+1] = xdot[:,i] + (1 - bn) * h * xddot[:,i] + (bn) * h * xddot[:,i+1]                  
                x[:,i+1] = x[:,i] + h * xdot[:,i] + h * h / 2 * ((1 - 2 * bn) * xddot[:,i] + (2 * bn) * xddot[:,i+1])

        self.state_current[0:self.dofs]=x[0:self.dofs,-1]
        self.state_current[self.dofs:2*self.dofs]=xdot[0:self.dofs,-1] 
        self.state_current[2*self.dofs:3*self.dofs]=xddot[0:self.dofs,-1]
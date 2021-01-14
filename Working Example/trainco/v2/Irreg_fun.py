import math
import numpy as np 
import matplotlib.pyplot as plt 

def Irreg_fun(V,nsteps,bridge_length,IrrType=1,IrrLevel=2,Trig_method=3):
    if IrrType==1:
        nl=2*math.pi/80
        nh=2*math.pi/0.5
        N=2048
        if IrrLevel==0:
            Av=0
            wr=0.0206
            wc=0.8246
        elif IrrLevel==1:
            Av=4.032*10**(-7)
            wr=0.0206
            wc=0.8246
        elif IrrLevel==2:
            Av=10.80*10**(-7)
            wr=0.0206
            wc=0.8246
    elif IrrType==2:
        nl=2*math.pi/300
        nh=2*math.pi/1.5
        N=2048
        if IrrLevel==0:
            Av=0
            wc=0.8245
        elif IrrLevel==1:
            Av=1.2107*10**(-4)
            wc=0.8245
        elif IrrLevel==2:
            Av=1.0181*10**(-4)
            wc=0.8245
        elif IrrLevel==3:
            Av=0.6816*10**(-4)
            wc=0.8245
        elif IrrLevel==4:
            Av=0.5376*10**(-4)
            wc=0.8245
        elif IrrLevel==5:
            Av=0.2095*10**(-4)
            wc=0.8245
        elif IrrLevel==6:
            Av=0.0339*10**(-4)
            wc=0.8245
    
    delta_f=(nh-nl)/N
    start=nl+(nh-nl)/(2*N)
    stop=nh-(nh-nl)/(2*N)+(nh-nl)/N
    step=(nh-nl)/N
    nk=np.linspace(start,stop,math.floor(stop/step))
    
    np.random.seed()
    faik=2*math.pi*np.random.rand(1,N)
    ak2=np.zeros([1,N])

    for i in range(0,N):
        wn=nk[i]
        if IrrType==1:
            Sn=(Av*wc**2/(wn**2+wr**2)/(wn**2+wc**2))
        elif IrrType==2:
            Sn=(0.25*Av*wc**2/(wn**2)/(wn**2+wc**2))
        ak2[0,i]=1*np.sqrt(2*delta_f*Sn)

    t=np.linspace(0,bridge_length/V,nsteps+1)
    Lt=len(t)

    #Trigonometric method (1)
   
    qtdd=np.zeros(Lt)
    qkdd=np.zeros([N,Lt])
    for i in range(0,N):
        for j in range(0,Lt):
            qkdd[i,j]=-(nk[i])**2*ak2[0,i]*math.cos(nk[i]*V*t[j]+faik[0,i])
            qtdd[j]=qtdd[j]+qkdd[i,j]
    Irr_vec_dd=-qtdd 
    qkd=np.zeros([N,Lt])
    qtd=np.zeros(Lt)
    for i in range(0,N):
        for j in range(0,Lt):
            qkd[i,j]=-(nk[i])*ak2[0,i]*math.sin(nk[i]*V*t[j]+faik[0,i])
            qtd[j]=qtd[j]+qkd[i,j]
    Irr_vec_d=-qtd
    qk=np.zeros([N,Lt])
    qt=np.zeros(Lt)
    for i in range(0,N):
        for j in range(0,Lt):
            qk[i,j]=ak2[0,i]*math.cos(nk[i]*V*t[j]+faik[0,i])
            qt[j]=qk[i,j]+qt[j]
    Irr_vec=-qt
    
    
    return Irr_vec, Irr_vec_d, Irr_vec_dd,t


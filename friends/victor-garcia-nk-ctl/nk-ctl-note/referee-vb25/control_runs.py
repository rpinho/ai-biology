"""Diagnostic controls for the printed ODE; these do not prove convergence."""
import concurrent.futures
import json
import math
import os
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

a,b=0.514,1.02e-9
def rates(t):
    return 1-1.5*t/(10000+t)+t/(1000+t),2-t/(500+t)+2*t/(25000+t)
def scalar(t,u,v):
    n,e=rates(t)
    return a*(1-b*t)-u/n-v*t/(n*e)
def equilibria(u,v):
    grid=np.r_[0.0,np.geomspace(1e-10,1/b,3000)]
    return [brentq(scalar,l,r,args=(u,v),xtol=1e-10) for l,r in zip(grid[:-1],grid[1:]) if scalar(l,u,v)*scalar(r,u,v)<0]
def jac(t,u,v):
    n,e=rates(t)
    np_= -15000/(t+10000)**2+1000/(t+1000)**2
    ep_= -500/(t+500)**2+50000/(t+25000)**2
    y=1/n;z=t/(n*e)
    return np.array([[-a*b*t,-u*t,-v*t],[-np_*y,-n,0],[y-ep_*z,t,-e]])
def run(case, max_step=float('inf')):
    name,u,v,t0,y0,q0,horizon=case
    def rhs(time,vec):
        logt,y,q=vec
        t=math.exp(logt) if logt>-745 else 0.0
        n,e=rates(t)
        return [a*(1-b*t)-u*y-q,1-n*y,v*t*y-e*q]
    sol=solve_ivp(rhs,(0,horizon),[math.log(t0),y0,q0],method='Radau',rtol=2e-9,atol=2e-11,max_step=max_step)
    logt,y,q=sol.y[:,-1]
    t=math.exp(logt) if logt>-745 else 0.0
    return {'name':name,'U':u,'V':v,'initial_T':t0,'initial_y':y0,'initial_Vz':q0,
            'horizon':horizon,'success':bool(sol.success),'steps':len(sol.t),
            'final_T':t,'final_logT':logt,'final_y':y,'final_Vz':q,
            'final_derivative':list(map(float,rhs(horizon,sol.y[:,-1])))}

if __name__=='__main__':
    cases=[
        ('bistability-low',0.6,2e-9,100,1,0,2000),
        ('bistability-high',0.6,2e-9,100000,1,0,2000),
        ('U=a-low-V',a,1e-5,100,1,0,5000),
        ('U=a-high-V',a,0.002,100,1,0,5000),
        ('U=3a/2',1.5*a,1e-9,1e9,0,0,2000),
        ('above-3a/2',10,100,1e9,0,0,100),
        ('U<a-small-V',0.2,1e-9,1,0,0,2000),
        ('U<a-large-V',0.2,1,1e9,2,10,500),
        ('initial-immune-overshoot',0.6,2e-9,100000,100,1,3000),
        ('very-small-couplings',1e-8,1e-15,1e9,0,0,500),
    ]
    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as pool:
        results=list(pool.map(run,cases))
    baseline_roots=equilibria(0.6,2e-9)
    baseline={'U':0.6,'V':2e-9,'roots':baseline_roots,
              'eigenvalues':[[str(e) for e in np.linalg.eigvals(jac(t,0.6,2e-9))] for t in baseline_roots]}
    discrepancies=[]
    for t in (1000,10000,100000):
        n,_=rates(t)
        legacy_n=1-1.5*t/(10000+t*t)+t/(1000+t)
        discrepancies.append({'T':t,'printed_n':n,'official_R_n':legacy_n})
    Path('control_results.json').write_text(json.dumps({'baseline':baseline,'runs':results,'source_R_denominator_control':discrepancies},indent=2))
    print(json.dumps(baseline))
    for r in results:print(json.dumps(r),flush=True)
    print('NUMERICAL CONTROLS DONE; finite diagnostics, not a proof')

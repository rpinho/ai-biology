"""PeerJ 8913 eqs 1--6 and Table 2; no claimant/referee code imports."""
import csv,itertools,json,os,subprocess
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import minimize
from scipy.special import expit

source=Path('friends_note_victor_1104')
t=np.array([2007.5,2008.5,2009.5,2010.5])
n=np.array([11,226,378,454]); k=np.array([3,81,135,191])
dates=np.array([2021.5,2022.5,2023.5,2024.5])
def predict(tau,intro,dates):
    def rhs(t,y):
        s,w,a,r=y; beta=.8/.98; gamma=.8; mu=.12
        infected=w+a+r
        return [-beta*s*infected+gamma*infected+(1-mu)*tau*w,
                beta*s*w-(gamma+tau)*w,mu*tau*w-gamma*a,
                beta*s*(a+r)-gamma*r]
    sol=solve_ivp(rhs,(intro,max(dates)),[.98,.02,0,0],t_eval=dates,
                  method='LSODA',rtol=1e-10,atol=1e-13)
    if not sol.success: raise RuntimeError(sol.message)
    return (sol.y[2]+sol.y[3])/sol.y[1:].sum(axis=0)
def loss(raw):
    p=predict(np.exp(raw[0]),1990+17.5*expit(raw[1]),t)
    return -np.sum(k*np.log(p)+(n-k)*np.log1p(-p))
fit=minimize(loss,[np.log(.4),0],method='Nelder-Mead',
             options={'maxiter':500,'xatol':1e-9,'fatol':1e-10})
tau_fit=np.exp(fit.x[0]); intro_fit=1990+17.5*expit(fit.x[1])
with (source/'results/standard/parameters.csv').open() as f:
    frozen=next(row for row in csv.DictReader(f) if row['country']=='Denmark')
tau=float(frozen['tau']); intro=float(frozen['intro'])
method=predict(tau,intro,dates)
# Derive r=(I_A+I_T)/I_S from equations: r'=tau*(r+mu), r(T)=0.
ratio=.12*np.expm1(tau*(dates-intro)); scalar=ratio/(1+ratio)
# Ordinary binomial logistic Newton/IRLS, four historical rows only.
X=np.column_stack([np.ones(4),t-2009.5]); coef=np.zeros(2)
for _ in range(30):
    p=expit(X@coef)
    step=np.linalg.solve(X.T@((n*p*(1-p))[:,None]*X),X.T@(k-n*p))
    coef+=step
    if max(abs(step))<1e-12: break
simple=expit(np.column_stack([np.ones(4),dates-2009.5])@coef)
trivial=np.full(4,k[-1]/n[-1])
ssi=np.array([274/438,311/436]); miba=np.array([.606,.632,.636,.65])
out={'training':{'time':t.tolist(),'n':n.tolist(),'k':k.tolist()},
     'frozen_parameters':{'tau':tau,'intro':intro},
     'independent_fit':{'tau':float(tau_fit),'intro':float(intro_fit),'success':bool(fit.success)},
     'max_ode_scalar_difference':float(max(abs(method-scalar))),
     'logistic_coefficients':coef.tolist(),
     'predictions':{'date':dates.tolist(),'method':method.tolist(),
                    'simple':simple.tolist(),'trivial':trivial.tolist(),
                    'refit':predict(tau_fit,intro_fit,dates).tolist()},'scores':{}}
baselines={}
for name,obs in [('SSI',ssi),('MiBa',miba)]:
    errors=[float(np.mean(abs(pred[:len(obs)]-obs))) for pred in [trivial,simple,method]]
    cmd=['python3',os.path.expanduser('~/dev/ai-research-tools/tools/sbs/sbs.py'),
         '--trivial',str(errors[0]),'--simple',str(errors[1]),'--method',str(errors[2]),
         '--lower-is-better','--metric','MAE']
    result=subprocess.run(cmd,capture_output=True,text=True,check=True)
    baselines[name]=json.loads(result.stdout)
    out['scores'][name]={'observed':obs.tolist(),
        'MAE_percentage_points':dict(zip(['trivial','simple','method'],[100*x for x in errors])),
        'SBS':(errors[0]-errors[1])/(errors[0]-errors[2])}
corners=[]
for signs in itertools.product([-1,1],repeat=4):
    obs=miba+np.array(signs)*np.array([.0005,.0005,.0005,.005])
    err=[float(np.mean(abs(pred-obs))) for pred in [trivial,simple,method]]
    corners.append([*err,(err[0]-err[1])/(err[0]-err[2])])
out['rounding_bounds']={'min':np.min(corners,axis=0).tolist(),'max':np.max(corners,axis=0).tolist()}
out['ssi_2021_integer_denominators']=[d for d in range(274,1000) if .6255<=274/d<.6265]
out['same_year_source_contrasts_points']=((ssi-miba[:2])*100).tolist()
Path('fresh_recomputation.json').write_text(json.dumps(out,indent=2)+'\n')
Path('BASELINES.json').write_text(json.dumps(baselines,indent=2)+'\n')
print(json.dumps(out,indent=2))

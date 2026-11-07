"""Independent implementation from Cadosch et al. eqs (1)-(6), Table 2.
Does not import the worker's code, outputs, or prior referee.
"""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'): os.environ[key]='1'
import json, itertools, subprocess, time
import numpy as np
from scipy.integrate import odeint
from scipy.optimize import minimize
from scipy.special import expit, gammaln
import statsmodels.api as sm

started=time.monotonic()
years=np.arange(2007,2011)+.5
n=np.array([11,226,378,454]); k=np.array([3,81,135,191])
external_years=np.arange(2021,2025)+.5
beta=.8/.98; gamma=.8; mu=.12
initial=[.98,.02,0.,0.]

def derivatives(x,t,tau):
 s,w,a,r=x
 allinfected=w+a+r
 return [-beta*s*allinfected+gamma*allinfected+(1-mu)*tau*w,
         beta*s*w-gamma*w-tau*w,
         mu*tau*w-gamma*a,
         beta*s*(a+r)-gamma*r]

def resistance(t,tau,introduction,precise=False):
 t=np.asarray(t)
 opts={'rtol':1e-10,'atol':1e-13} if precise else {'rtol':1e-6,'atol':1e-6}
 x=odeint(derivatives,initial,np.r_[introduction,t],args=(tau,),**opts)[1:]
 return (x[:,2]+x[:,3])/x[:,1:].sum(axis=1)

def transform(v): return np.exp(v[0]),1990+expit(v[1])*(years[0]-1990)
def objective(v):
 tau,introduction=transform(v)
 p=resistance(years,tau,introduction)
 if np.any(p<=0) or np.any(p>=1):return float('inf')
 return -float(np.sum(gammaln(n+1)-gammaln(k+1)-gammaln(n-k+1)+k*np.log(p)+(n-k)*np.log1p(-p)))

# First run: the paper's standard Nelder-Mead procedure and transformed start.
fit=minimize(objective,[np.log(.4),0.],method='Nelder-Mead')
assert fit.success,fit
own_tau,own_intro=transform(fit.x)
# Also evaluate frozen source parameter values as literal data, rather than substituting our refit.
frozen_tau=.129069567169382; frozen_intro=1995.5803585762
source=resistance(external_years,frozen_tau,frozen_intro,precise=True)
refitted=resistance(external_years,own_tau,own_intro,precise=True)
# Independent analytic identity derived by dividing (3)+(4) by (2):
# r'=tau*(r+mu), r(T)=0; p=r/(1+r). This is a cross-check, not the fitter.
r=mu*np.expm1(frozen_tau*(external_years-frozen_intro)); analytic=r/(1+r)
assert np.max(abs(source-analytic))<1e-8
assert np.max(abs(source-refitted))<.002

# Standard grouped-binomial GLM; only the four printed historical training rows.
x=sm.add_constant(years-2010)
glm=sm.GLM(np.column_stack([k,n-k]),x,family=sm.families.Binomial()).fit()
simple=glm.predict(sm.add_constant(external_years-2010))
trivial=np.repeat(k[-1]/n[-1],4)
# Exact SSI numerator/denominator, and printed MiBa centers, transcribed from primary sources.
ssi=np.array([274/438,311/436]); miba=np.array([.606,.632,.636,.65])
# Integer denominator audit for the 2021 overall and sex-specific counts/rounding.
possible=lambda positive,pct:[den for den in range(positive,2000) if pct-.05<=100*positive/den<pct+.05]
assert possible(274,62.6)==[438]
assert possible(142,61.2)==[232]
assert possible(132,64.1)==[206]

def score(obs,p):return float(np.mean(abs(obs-p[:len(obs)])))
results={}; raw={}
for label,obs in [('SSI',ssi),('MiBa',miba)]:
 scores={name:score(obs,p) for name,p in [('trivial',trivial),('simple',simple),('method',source)]}
 command=['python3',os.path.expanduser('~/dev/ai-research-tools/tools/sbs/sbs.py')]
 for name,value in scores.items(): command.extend(['--'+name,repr(value)])
 command.extend(['--lower-is-better','--metric','MAE'])
 run=subprocess.run(command,capture_output=True,text=True,check=True)
 raw[label]={'command':command,'stdout':run.stdout,'stderr':run.stderr,'scores_fraction':scores}
 results[label]={'MAE_percentage_points':{a:100*b for a,b in scores.items()},'SBS':json.loads(run.stdout)}

halfwidth=np.array([.0005,.0005,.0005,.005])
corners=[]
for signs in itertools.product([-1,1],repeat=4):
 obs=miba+halfwidth*np.array(signs)
 t,s,m=[score(obs,p) for p in (trivial,simple,source)]
 corners.append([t,s,m,(t-s)/(t-m)])
corners=np.array(corners)

# Standard unconstrained linear trend as an extra, training-only baseline check.
linear=sm.OLS(k/n,x).fit().predict(sm.add_constant(external_years-2010))
weighted_linear=sm.WLS(k/n,x,weights=n).fit().predict(sm.add_constant(external_years-2010))
results['extra_linear_checks']={name:{'predictions':p.tolist(),'SSI_MAE_pp':score(ssi,p)*100,'MiBa_MAE_pp':score(miba,p)*100} for name,p in [('linear',linear),('weighted_linear',weighted_linear)]}
results['rounding_MiBa']={'columns':['trivial_MAE','simple_MAE','method_MAE','SBS'],'min':corners.min(axis=0).tolist(),'max':corners.max(axis=0).tolist()}
results['fit']={'tau':own_tau,'intro':own_intro,'nll':fit.fun,'parameters_transformed':fit.x.tolist(),'optimizer':str(fit.message),'evaluations':fit.nfev}
results['frozen_parameters']={'tau':frozen_tau,'intro':frozen_intro}
results['glm']={'coefficients_center2010':glm.params.tolist(),'converged':glm.converged}
results['predictions']={'years':external_years.tolist(),'frozen_model':source.tolist(),'own_refit':refitted.tolist(),'analytic':analytic.tolist(),'simple':simple.tolist(),'trivial':trivial.tolist()}
results['observations']={'SSI':ssi.tolist(),'MiBa':miba.tolist()}
results['source_contrasts_pp']=(100*(ssi-miba[:2])).tolist()
results['elapsed_seconds']=time.monotonic()-started
with open('BASELINES.json','w') as f:json.dump(raw,f,indent=2)
with open('recomputation.json','w') as f:json.dump(results,f,indent=2)
print(json.dumps(results,indent=2))

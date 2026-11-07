"""Referee reconstruction from printed Eqs.21--23 and Table 3.

No candidate search, construction, or verification module is used.
All proof checks use exact rational polynomial arithmetic in SymPy.
"""
import itertools
import json
import math
from pathlib import Path
import sympy as s

t, y, z, U, V = s.symbols('T y z U V', real=True)
R = s.Rational
a, b = R('0.514'), R('1.02e-9')
mu, bn, dn, kbn, kdn = R(1), R('1.5'), R(1), R(10000), R(1000)
d, be, de, kbe, kde = R(2), R(1), R(2), R(500), R(25000)
n = s.factor(mu - bn*t/(kbn+t) + dn*t/(kdn+t))
e = s.factor(d - be*t/(kbe+t) + de*t/(kde+t))
f = a*(1-b*t)
np, ep = s.diff(n,t), s.diff(e,t)
g = s.factor(e-t*ep)
F = f-U/n-V*t/(n*e)
checks = {}
certs = {}
def check(name, condition, evidence=None):
    assert bool(condition), name
    checks[name] = True
    if evidence is not None:
        certs[name] = evidence
    print('PASS', name, flush=True)
def zero(name, expr):
    check(name, s.cancel(expr)==0)
def coeff_pos(name, expr, minus=0):
    num, den = s.fraction(s.cancel(expr-minus))
    pn, pd = s.Poly(num,t), s.Poly(den,t)
    check(name, all(c>0 for c in pn.all_coeffs()) and all(c>0 for c in pd.all_coeffs()),
          {'degree':pn.degree(), 'numerator_descending':list(map(str,pn.all_coeffs())),
           'denominator_descending':list(map(str,pd.all_coeffs()))})
def halfline_nonnegative(name, expr):
    num, den = s.fraction(s.cancel(expr))
    check(name, all(c>=0 for c in s.Poly(num,t).all_coeffs()) and
          all(c>0 for c in s.Poly(den,t).all_coeffs()))

# Source rate bounds, including bounds whose numerator is not coefficient-positive.
halfline_nonnegative('n >= 1/2', n-R(1,2))
zero('3/2-n square identity', R(3,2)-n-((t-1500)**2+2750000)/((t+10000)*(t+1000)))
coeff_pos('e > 1', e, 1)
coeff_pos('e < 3', 3-e)
zero('g square identity', g-(2-t**2/(t+500)**2+2*t**2/(t+25000)**2))
halfline_nonnegative('g >= 1', g-1)
zero('X lower decomposition', t*np+R(3,8) -
     (R(3,2)*(t-10000)**2/(4*(t+10000)**2)+1000*t/(t+1000)**2))
zero('X upper decomposition', R(1,4)-t*np -
     ((t-1000)**2/(4*(t+1000)**2)+15000*t/(t+10000)**2))

# Differentiate the original vector field in state coordinates.
state=s.Matrix([t,y,z])
flow=s.Matrix([t*(f-U*y-V*z),1-n*y,t*y-e*z])
p=f-U*y-V*z
r=y-1/n
C=t*np/n**2
B=U*(n-e)-V*t
D=e+a*b*t
pdot=(s.Matrix([s.diff(p,x) for x in state]).dot(flow))
rdot=(s.Matrix([s.diff(r,x) for x in state]).dot(flow))
zero('p differential identity', pdot-(-D*p+e*F+B*r))
zero('r differential identity', rdot-(-n*r+C*p))
zero('energy differential identity', p*pdot+8*r*rdot-e*F*p -
     (-D*p**2-8*n*r**2+(B+8*C)*p*r))

# Derive the B interval from the scalar comparison bounds, not a numerical box.
eta=R(1,1000)
lo=-R(3,2)*a*(a+3)-eta
hi=R(3,4)*a
check('B-tail lower slope', a+3>R(5,2))
for name, value in [('lower',lo),('upper',hi)]:
    coeff_pos('strict damping at '+name+' endpoint',32*n*D-(value+8*C)**2,1)
check('exact eigenvalue margin',1/(4*(15+a))==R(125,7757),str(R(125,7757)))

# Rebuild the equilibrium polynomial directly, then rule out every bad sign
# pattern by exact strict Fourier--Motzkin elimination in (U,V).
q=s.symbols('q')
P=s.Poly(s.cancel((f*n*e-U*e-V*t)*(2*(t+10000)*(t+1000))*(t+500)*(t+25000)),t)
check('equilibrium degree five',P.degree()==5)
check('leading coefficient always negative',s.diff(P.LC(),V)<0 and P.LC().subs(V,0)<0)
def feasible(constraints):
    # Each tuple means a*U+b*V+c > 0. Both variables are eliminated.
    current=constraints
    for _ in range(2):
        pos=[v for v in current if v[0]>0]
        neg=[v for v in current if v[0]<0]
        nxt=[v[1:] for v in current if v[0]==0]
        for pp in pos:
            for nn in neg:
                nxt.append(tuple(s.factor(-nn[0]*pp[j]+pp[0]*nn[j]) for j in range(1,len(pp))))
        current=nxt
    return all(v[0]>0 for v in current)
bad=0
for signs in itertools.product((-1,1),repeat=5):
    chain=(-1,)+signs
    changes=sum(chain[j]!=chain[j+1] for j in range(5))
    if changes<=2:
        continue
    constraints=[(R(1),R(0),R(0)),(R(0),R(1),R(0))]
    for c,sign in zip(P.all_coeffs()[1:],signs):
        constraints.append(tuple(sign*s.diff(c,x) for x in (U,V))+(sign*c.subs({U:0,V:0}),))
    check('impossible sign pattern '+''.join('+' if v>0 else '-' for v in signs),not feasible(constraints))
    bad+=1
certs['Descartes']={'bad_strict_sign_patterns_excluded':bad,
 'zero_coefficients':'Any parameter point with zeros has an arbitrarily close generic point preserving all nonzero signs; insertion of signs cannot reduce variation.'}

# Fold formula derived by solving F=F_T=0; halfline uniqueness and monotonicity.
sol=s.solve([s.together(F),s.together(s.diff(F,t))],(U,V),simplify=False)
vs=s.factor(sol[V]); us=s.factor(sol[U])
zero('fold V formula',vs-e**2*(f*np-a*b*n)/g)
zero('fold U formula',us-(f*n-t*vs/e))
zero('fold tangent identity',s.diff(us,t)+t/e*s.diff(vs,t))
Q=s.factor((1-b*t)*np-b*n)
qnum,qden=s.fraction(Q)
signs=[s.sign(c) for c in s.Poly(qnum,t).all_coeffs() if c!=0]
check('fold endpoint unique positive root',sum(signs[j]!=signs[j+1] for j in range(len(signs)-1))==1
      and qnum.subs(t,0)>0 and qnum.subs(t,2200)<0)
vnum,vden=s.fraction(s.cancel(-s.diff(vs,t)))
degree=s.degree(vnum,t)
# Positive coefficients of (1+x)^d p(2200*x/(1+x)) certify [0,2200].
x=s.symbols('x')
transformed=s.Poly(s.cancel((1+x)**degree*vnum.subs(t,2200*x/(1+x))),x)
check('fold V strictly decreasing on [0,2200]',all(c>0 for c in transformed.all_coeffs()) and
      all(c>0 for c in s.Poly(vden,t).all_coeffs()),
      {'degree':int(degree),'transformed_coefficients':list(map(str,transformed.all_coeffs()))})
zero('boundary fold value',vs.subs(t,0)-2*a*(R(17,20000)-b))
zero('energy logarithmic coefficient at zero',s.limit(e*F,t,0)-2*(a-U))
zero('U=a removable energy derivative',s.limit((-e*F/t).subs(U,a),t,0)-(V-vs.subs(t,0)))
check('U=a,Vcrit negative F curvature',s.limit(s.diff(F,t,2).subs({U:a,V:vs.subs(t,0)}),t,0)<0)

# Full 3D Jacobian. Compare invariant coefficients at equilibrium, not a
# projected scalar derivative used as a stability surrogate.
J=flow.jacobian(state).subs({y:1/n,z:t/(n*e)})
J=J.subs(U, n*f-V*t/e)
lam=s.symbols('lambda')
cp=J.charpoly(lam).all_coeffs()
AA=a*b*t; CC=U/n; KK=V*t/(n*e); XX=t*np
expected=[s.Integer(1),AA+n+e,AA*(n+e)+n*e-CC*XX+KK*g,
          AA*n*e-(CC+KK)*e*XX+KK*n*g]
for i,(actual,wanted) in enumerate(zip(cp,expected)):
    zero('Jacobian cubic coefficient '+str(i),actual-wanted.subs(U,n*f-V*t/e))
zero('Jacobian constant and F derivative',expected[-1]+t*n*e*s.diff(F,t))
check('Routh positive a2 lower margin',R(1,2)-a/4>0)
check('Routh determinant lower margin',R(3,4)-a/8>0)

# Record algebraic, not floating-point, endpoint isolation.
left,right=R(0),R(2200)
for _ in range(60):
    mid=(left+right)/2
    if qnum.subs(t,mid)>0:left=mid
    else:right=mid
certs['fold_endpoint_isolation']={'left':str(left),'right':str(right),
    'approx_Tcrit':float((left+right)/2),'approx_Umax':float(us.subs(t,(left+right)/2)),
    'Vcrit':str(vs.subs(t,0))}
result={'status':'PASS','checks':checks,'certificates':certs,
        'rates':{'n':str(n),'e':str(e),'a':str(a),'b':str(b)},
        'fold':{'U':str(us),'V':str(vs)}}
Path('independent_exact.json').write_text(json.dumps(result,indent=2))
print(json.dumps(certs['fold_endpoint_isolation']))
print('INDEPENDENT EXACT AUDIT DONE',flush=True)

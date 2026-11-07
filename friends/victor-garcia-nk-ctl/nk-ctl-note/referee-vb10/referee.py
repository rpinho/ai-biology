"""Independent algebra and exact interval audit of printed Eqs. 21--23.

No claimant module, coefficient, root interval or verifier is imported.
Parameters below transcribe primary Table 3 and the submitted witness.
Run on authorized pod, streamed through stdin; emits JSON to stdout.
"""
import sympy as s
import json
import time
from itertools import combinations

started = time.time()
T, N, E = s.symbols('T N E', real=True)
names = 'a b c k sigma mu bn dn Kbn Kdn d be de Kbe Kde omega'.split()
syms = s.symbols(' '.join(names), positive=True)
p = dict(zip(names, syms))
a,b,c,k,sigma,mu,bn,dn,Kbn,Kdn,d,be,de,Kbe,Kde,omega = syms
# Direct transcription of primary Eqs. 21, 22, 23.
field = s.Matrix([
    a*T*(1-b*T)-c*N*T-k*T*E,
    sigma-mu*N+bn*T*N/(Kbn+T)-dn*T*N/(Kdn+T),
    -d*E+be*T*E/(Kbe+T)-de*T*E/(Kde+T)+omega*N*T,
])
Jraw = field.jacobian([T,N,E])
n = mu-bn*T/(Kbn+T)+dn*T/(Kdn+T)
e = d-be*T/(Kbe+T)+de*T/(Kde+T)
B = (Kbn+T)*(Kdn+T)
D = (Kbe+T)*(Kde+T)
A = s.cancel(n*B)
C = s.cancel(e*D)
P = s.Poly(s.expand(a*(1-b*T)*A*C-c*sigma*B*C-k*omega*sigma*T*B*D),T)
assert P.degree() == 5
assert s.expand(P.eval(0)-(a*mu-c*sigma)*d*Kbn*Kdn*Kbe*Kde)==0
assert s.expand(P.LC()-(-a*b*(be-de-d)*(bn-mu-dn)-k*sigma*omega))==0
# Schur identity with arbitrary loss rates/derivatives. This avoids
# presupposing the stability of a projected one-dimensional equation.
nv, ev, np, ep = s.symbols('nv ev np ep', nonzero=True)
Ne = sigma/nv
Ee = omega*Ne*T/ev
Jg = s.Matrix([[-a*b*T,-c*T,-k*T],[-np*Ne,-nv,0],
               [-ep*Ee+omega*Ne,omega*T,-ev]])
Hp = -a*b+c*sigma*np/nv**2-k*omega*sigma*(nv*ev-T*(np*ev+nv*ep))/(nv*ev)**2
assert s.cancel((-Jg).det()+T*nv*ev*Hp)==0
# With n=A/B, e=C/D and P=A*C*H, at a root of H:
# det(-J)=-T*n*e*H'=-T*P'/(B*D).
result = {'algebra': {'degree':5, 'boundary_identity':True,
    'paper_eq81_leading_coefficient':True, 'schur_identity':True}}

# Basic exact rational interval arithmetic; sympy is used only for rational
# polynomial algebra and Sturm isolation, not floating-point stability.
def point(q):
    q=s.Rational(q)
    return (q,q)
def add(x,y): return (x[0]+y[0],x[1]+y[1])
def mul(x,y):
    vals=[i*j for i in x for j in y]
    return (min(vals),max(vals))
def div(x,y):
    assert y[0]*y[1]>0, ('division crosses zero',y)
    return mul(x,(1/y[1],1/y[0]))
def ipoly(poly,x):
    ans=point(0)
    for q in poly.all_coeffs(): ans=add(mul(ans,x),point(q))
    return ans
def irat(expr,x):
    num,den=s.fraction(s.cancel(expr))
    return div(ipoly(s.Poly(num,T),x),ipoly(s.Poly(den,T),x))
def encode(x):
    return {'exact':[str(x[0]),str(x[1])],
            'decimal':[float(x[0]),float(x[1])]}

compact = dict(a=1,b='1/100000',c='11/10',k='29/100',sigma=1,
    mu=1,bn=1,dn=1,Kbn=100,Kdn='1/10',d=1,be=2,de=50,
    Kbe=1,Kde=100,omega=1)
table = dict(a='0.514',b='0.00000000102',mu=1,bn='1.5',dn=1,
    Kbn=10000,Kdn=1000,d=2,be=1,de=2,Kbe=500,Kde=25000,
    omega='0.00000011',sigma=1000,c='3/5000',k='1/55000')

def witness(label, values, expect):
    sub={p[key]:s.Rational(val) for key,val in values.items()}
    nf=s.cancel(n.subs(sub)); ef=s.cancel(e.subs(sub))
    for f in [nf,ef]:
        num,den=s.fraction(f)
        assert all(q>0 for q in s.Poly(den,T).all_coeffs())
        poly=s.Poly(num,T)
        assert (all(q>=0 for q in poly.all_coeffs()) and poly.eval(0)>0
                or poly.degree()==2 and poly.LC()>0 and s.discriminant(poly)<0)
    Ns=s.cancel(values['sigma']/nf)
    Es=s.cancel(sub[omega]*Ns*T/ef)
    # Use differentiated original field, with no scalar-slope stability test.
    J=Jraw.subs(sub).subs({N:Ns,E:Es}).applyfunc(s.cancel)
    coeff1=s.cancel(-s.trace(J))
    coeff2=s.cancel(sum(J.extract(inds,inds).det() for inds in combinations(range(3),2)))
    coeff3=s.cancel(-J.det())
    delta=s.cancel(coeff1*coeff2-coeff3)
    poly=s.Poly(P.as_expr().subs(sub),T)
    intervals=poly.intervals(eps=s.Rational(1,10**25))
    positive=[(bounds,m) for bounds,m in intervals if bounds[0]>0]
    assert len(positive)==poly.count_roots(0,s.oo)
    roots=[]
    stable=0
    for bounds,m in positive:
        assert m==1
        checks=[irat(f,bounds) for f in [coeff1,coeff2,coeff3,delta]]
        is_stable=all(x[0]>0 for x in checks)
        assert is_stable or checks[2][1]<0
        assert checks[0][0]>0 and checks[1][0]>0 and checks[3][0]>0
        # Nonzero constant term and delta>0 exclude zero and imaginary pair.
        stable+=is_stable
        roots.append({'T':encode(bounds),'N':encode(irat(Ns,bounds)),
            'E':encode(irat(Es,bounds)), 'routh':[encode(x) for x in checks],
            'stable':is_stable, 'hyperbolic':True})
    boundary=[sub[a]-sub[c]*sub[sigma]/sub[mu],-sub[mu],-sub[d]]
    stable+=all(x<0 for x in boundary)
    assert stable==expect,(label,stable)
    return {'parameters':values,'polynomial':str(poly.as_expr()),
            'positive_loss_rates_on_nonnegative_axis':True,
            'positive_roots_sturm_count':len(positive),'roots':roots,
            'boundary_eigenvalues':[str(x) for x in boundary],
            'total_stable':int(stable)}

result['compact']=witness('compact',compact,3)
print('COMPACT_DONE',flush=True)
result['table3']=witness('table3',table,2)
print('TABLE3_DONE',flush=True)

# Independent fixed-Table-3 coefficient proof. Choose scale T=1000*x,
# distinct from the claimant's, and use v=k*sigma*omega without rescaling.
x,u,v=s.symbols('x u v',real=True)
fixed={p[key]:s.Rational(val) for key,val in table.items()
       if key not in ['c','k','sigma']}
nn=s.cancel(n.subs(fixed).subs(T,1000*x))
ee=s.cancel(e.subs(fixed).subs(T,1000*x))
an,bn_=s.fraction(nn); ae,be_=s.fraction(ee)
pp=s.Poly(s.expand(fixed[a]*(1-fixed[b]*1000*x)*an*ae
                  -u*bn_*ae-v*1000*x*bn_*be_),x)
assert pp.degree()==5
lc=pp.LC()
assert lc.subs(v,0)<0 and s.diff(lc,v)<0 and s.diff(lc,u)==0
thresholds=[]
for power in range(4,-1,-1):
    co=pp.nth(power)
    weight=-s.diff(co,u)
    assert weight>0
    tau=s.cancel(co.subs(u,0)/weight)
    assert s.expand(co-weight*(tau-u))==0
    thresholds.append(tau)
diffs=[s.expand(thresholds[i+1]-thresholds[i]) for i in range(4)]
assert all(q.subs(v,0)>0 and s.diff(q,v)>0 for q in diffs[:2])
assert all(q.subs(v,0)<0 and s.diff(q,v)>0 for q in diffs[2:])
turns=[s.solve(q,v)[0] for q in diffs[2:]]
assert 0<turns[0]<turns[1]
# Ascending adjacent differences prove descending-power tau sequence is
# unimodal for all v>=0. Positive coefficients form one block at any u.
# Thus the negative-leading polynomial has <=2 Descartes sign changes.
result['table3_global']={'scale':'T=1000*x','v':'k*sigma*omega',
    'thresholds':[str(q) for q in thresholds],
    'successive_differences':[str(q) for q in diffs],
    'turns':[str(q) for q in turns],
    'unimodal_all_v_nonnegative':True,'descartes_positive_root_bound':2}
result['elapsed_seconds']=time.time()-started
result['status']='PASS'
print('BEGIN_REFEREE_JSON')
print(json.dumps(result,indent=2))
print('END_REFEREE_JSON')

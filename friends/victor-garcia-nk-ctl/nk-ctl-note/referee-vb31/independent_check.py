"""Independent exact referee. No claimant search/verifier code is used.

The energy ansatz is a submitted witness, transcribed from GLOBAL_PROOF.md.
Source equations/rates are checked against fresh primary XML by source_audit.py.
All scientific execution is on the authorized pod.
"""
import hashlib, itertools, json, pathlib, time
import sympy as S

OUT=pathlib.Path('/workspace/ref_victor_VB31')
started=time.time()
T,y,z,a,b,U,V,p,r,xx,ww,s=S.symbols('T y z a b U V p r x w s')
R=S.Rational
n=1-R(3,2)*T/(10000+T)+T/(1000+T)
e=2-T/(500+T)+2*T/(25000+T)
k=(T+3420000)/(30*(T+200000))
q=S.Integer(32)
can=lambda expr:S.cancel(expr)
n,e,k=map(can,(n,e,k))
C=can(T*S.diff(n,T)/n**2)
G=can(-e*(a*(1-b*T)-U/n-V*T/(n*e)))
H=can(k*G/n)
pv=a*(1-b*T)-U*y-V*z
rv=y-1/n
vv=pv-k*rv
field=(T*pv,1-n*y,T*y-e*z)
kin=vv**2/2+q*rv**2/2+H*rv
# Chain rule in original coordinates; the primitives contribute (G-H*C)*p.
edot=can(sum(S.diff(kin,state)*f for state,f in zip((T,y,z),field))+(G-H*C)*pv)
print('full-source derivative built',time.time()-started,flush=True)
edot_pr=can(edot.subs(z,(a*(1-b*T)-U*y-p)/V).subs(y,r+1/n))
# v=p-k*r: derive quadratic in v,r, without inserting claimed A,K,Q formulas.
v=S.Symbol('v')
edot_vr=S.Poly(can(edot_pr.subs(p,v+k*r)),v,r)
# Because k varies with T, coefficients of v^2 and vr depend on r.
Ac=can(-edot_vr.coeff_monomial(v**2)-edot_vr.coeff_monomial(v**2*r)*r)
Kc=can(edot_vr.coeff_monomial(v*r)+edot_vr.coeff_monomial(v*r**2)*r)
Qc=can(-edot_vr.coeff_monomial(r**2))
assert can(edot_pr.subs(p,v+k*r)-(-Ac*v**2+Kc*v*r-Qc*r**2))==0
expected_A=e+a*b*T+k*C+T*S.diff(k,T)*r
expected_K=U*(n-e)-V*T-k*(e+a*b*T-n)+(q-k**2)*C+T*S.diff(H,T)-k*T*S.diff(k,T)*r
expected_Q=q*(n-k*C)-k*T*S.diff(H,T)
assert all(can(aa-bb)==0 for aa,bb in [(Ac,expected_A),(Kc,expected_K),(Qc,expected_Q)])
print('PASS direct full-field energy identity (all shift derivatives included)',flush=True)

def replace_controls(expr):
    return can(expr.subs(r,y-1/n).subs({b:xx/(a*T),V:ww/T}))
matrix=S.Matrix([[replace_controls(Ac),-replace_controls(Kc)/2],[-replace_controls(Kc)/2,replace_controls(Qc)]])
controls=(a,xx,U,ww,y)
# Each variable separately affine; inspect mixed terms below as well.
for entry in matrix:
    assert all(can(S.diff(entry,c,2))==0 for c in controls)
    # Matrix must be jointly affine in a,x,U,w, and may have affine y terms.
    assert all(can(S.diff(entry,c,d))==0 for c,d in itertools.combinations((a,xx,U,ww),2))
print('PASS control affinity',flush=True)

receipts=[]; unique={}
def certify_positive(expr,label):
    numerator,denominator=map(lambda h:S.Poly(h,T,domain=S.QQ),S.fraction(can(expr)))
    # Rational cancellation can choose either overall sign.
    if denominator.eval(0)<0:
        numerator,denominator=-numerator,-denominator
    assert denominator.eval(0)>0 and all(c>=0 for c in denominator.all_coeffs()),(label,'denominator')
    assert numerator.eval(0)>0,(label,'nonpositive at origin')
    primitive=numerator.clear_denoms()[1].primitive()[1]
    key=tuple(map(int,primitive.all_coeffs()))
    digest=hashlib.sha256(json.dumps(key).encode()).hexdigest()
    if key not in unique:
        root_count=int(primitive.count_roots(0,S.oo))
        assert root_count==0,(label,'positive real roots',root_count)
        unique[key]={'sha256':digest,'degree':primitive.degree(),'positive_roots':root_count,'coefficients':list(key)}
    record={'label':label,'sha256':digest,'degree':primitive.degree(),'positive_roots':0}
    receipts.append(record)
    print('PASS',label,'degree',primitive.degree(),digest[:12],flush=True)

# Rate, lag, and proof-weight bounds used by the analytic argument.
for label,expr in [('n>1/2',n-R(1,2)),('n<3/2',R(3,2)-n),('e>1',e-1),('e<3',3-e),
                   ('C<1/2',R(1,2)-C),('C>-1/2',R(1,2)+C),
                   ('k>0',k),('k<=57/100',R(57,100)-k+0*T)]:
    # The last two nonstrict bounds may have zeros, so certify after removing
    # exact T factors; T>=0 and the remaining factor is strictly positive.
    ex=can(expr)
    num,den=S.fraction(ex)
    factors=0
    while S.Poly(num,T).eval(0)==0:
        num=can(num/T); factors+=1
    certify_positive(num/den,label+f' (T factors={factors})')
assert can(R(161,1200)+T*S.diff(k,T)-R(161,1200)*(T-200000)**2/(T+200000)**2)==0
assert S.Poly(S.fraction(can(-S.diff(k,T)))[0],T).LC()>0
assert R(1)-R(57,100)*R(1,2)-R(161,1200)*R(4,3)==R(193,360)

# Derive Bernstein matrices from power coefficients of s=a/2, rather than
# treating the three claimed stages as samples of the parameter interval.
vertices=[]
for yend,theta,corner in itertools.product((R(2,3),R(2)),(0,1),((0,0),(0,1),(1,0))):
    u,eta=corner
    ms=matrix.subs({y:yend,a:2*s,xx:2*s*theta,U:3*s*u,ww:3*s*(2*s+3)*(1-u)*eta})
    powers=[]
    for entry in ms:
        poly=S.Poly(entry,s)
        assert poly.degree()<=2
        powers.append([poly.nth(i) for i in range(3)])
    coeff_matrices=[]
    for stage in range(3):
        entries=[c[0] if stage==0 else c[0]+c[1]/2 if stage==1 else sum(c) for c in powers]
        coeff_matrices.append(S.Matrix(2,2,entries))
    reconstruction=(1-s)**2*coeff_matrices[0]+2*s*(1-s)*coeff_matrices[1]+s**2*coeff_matrices[2]
    assert all(can(ex)==0 for ex in reconstruction-ms)
    for stage,mat in enumerate(coeff_matrices):
        label=f'y={yend},x/a={theta},corner={corner},Bernstein={stage}'
        certify_positive(mat[0,0],label+': A')
        certify_positive(4*mat.det(),label+': 4det')
        vertices.append(label)
print('PASS exact Bernstein convex coverage',len(vertices),'matrices',flush=True)

# Sceptic control: this is not merely uniqueness or automatic extinction.
control={a:2,b:R(51,50000000000),U:R(11,5),V:R(11,100000000000)}
force=can(a*(1-b*T)-U/n-V*T/(n*e))
control_num=S.Poly(S.fraction(can(force.subs(control)))[0],T)
positive_roots=int(control_num.count_roots(0,S.oo))
assert positive_roots==2
assert S.gcd(control_num,control_num.diff()).degree()==0
intervals=control_num.intervals(eps=R(1,10))
print('PASS multiequilibrium control: exactly two simple positive equilibria',str(intervals),flush=True)

# Critical a=U boundary expansion used to extend the energy to T=0.
g0=can(G.subs(T,0)); assert can(g0+2*(a-U))==0
gcrit=can(G.subs(U,a))
assert can(gcrit.subs(T,0))==0
assert S.limit(gcrit/T,T,0).is_finite is not False
assert can(H.subs(U,a).subs(T,0))==0
assert can(C.subs(T,0))==0
result={'status':'PASS','sympy':S.__version__,'elapsed_s':time.time()-started,
        'energy_identity':'exact original-coordinate chain rule',
        'control_matrices':len(vertices),'unique_positive_polynomials':len(unique),
        'positivity_checks':receipts,'polynomials':list(unique.values()),
        'control_positive_equilibria':positive_roots,'control_isolating_intervals':str(intervals),
        'origin_G':str(g0),'critical_boundary':'G(0)=H(0)=C(0)=0 when a=U'}
(OUT/'independent_result.json').write_text(json.dumps(result,indent=2))
print('ALL INDEPENDENT EXACT CHECKS PASS',time.time()-started,flush=True)

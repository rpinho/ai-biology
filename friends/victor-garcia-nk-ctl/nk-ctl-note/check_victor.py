#!/usr/bin/env python3
"""Exact checks for the convergence note. Python 3.9+, standard library only.
No input files, network, floating arithmetic, or external modules are used.
Polynomial coefficients are stored in ascending order. Rational functions are
reduced exactly. Positive polynomials are proved by Bernstein subdivision.
The energy and invariant-set arguments in the note remain analytic arguments.
Rational arithmetic routines are adapted from the supplied proof materials.
"""
from fractions import Fraction as F
from math import comb, lcm

def trim(p):
 p=list(map(F,p))
 while len(p)>1 and not p[-1]:p.pop()
 return p
def add(p,q):return trim([(p[i]if i<len(p)else 0)+(q[i]if i<len(q)else 0)for i in range(max(len(p),len(q)))])
def neg(p):return [-v for v in p]
def sub(p,q):return add(p,neg(q))
def mul(p,q):
 z=[F(0)]*(len(p)+len(q)-1)
 for i,a in enumerate(p):
  for j,b in enumerate(q):z[i+j]+=a*b
 return trim(z)
def div(p,q):
 p=trim(p);q=trim(q);a=[F(0)]*max(1,len(p)-len(q)+1)
 while p!=[0]and len(p)>=len(q):
  j=len(p)-len(q);b=p[-1]/q[-1];a[j]=b;p=sub(p,[0]*j+[b*x for x in q])
 return trim(a),p
def gcd(p,q):
 while q!=[0]:p,q=q,div(p,q)[1]
 return [v/p[-1]for v in p]
def der(p):return trim([i*p[i]for i in range(1,len(p))]or[0])
def ev(p,x):
 s=F(0)
 for a in reversed(p):s=s*x+a
 return s
class Rat:
 def __init__(self,p,q=[1]):
  if not isinstance(p,list):p=[p]
  p,q=trim(p),trim(q);g=gcd(p,q);p,r=div(p,g);assert r==[0];q,r=div(q,g);assert r==[0]
  fac=q[-1];self.p=[v/fac for v in p];self.q=[v/fac for v in q]
 def __add__(self,o):o=rr(o);return Rat(add(mul(self.p,o.q),mul(o.p,self.q)),mul(self.q,o.q))
 __radd__=__add__
 def __neg__(self):return Rat(neg(self.p),self.q)
 def __sub__(self,o):return self+-rr(o)
 def __rsub__(self,o):return rr(o)+-self
 def __mul__(self,o):o=rr(o);return Rat(mul(self.p,o.p),mul(self.q,o.q))
 __rmul__=__mul__
 def __truediv__(self,o):o=rr(o);return Rat(mul(self.p,o.q),mul(self.q,o.p))
 def __rtruediv__(self,o):return rr(o)/self
 def d(self):return Rat(sub(mul(der(self.p),self.q),mul(self.p,der(self.q))),mul(self.q,self.q))
 def at(self,x):return ev(self.p,x)/ev(self.q,x)
def rr(x):return x if isinstance(x,Rat)else Rat(x)

def scale(p,c): return trim([v*c for v in p])
def power(p,k):
    out=[F(1)]
    for _ in range(k): out=mul(out,p)
    return out

def bern_interval(p,hi):
    d=len(p)-1
    return [sum(p[i]*hi**i*F(comb(j,i),comb(d,i))
                for i in range(j+1)) for j in range(d+1)]

def split(b):
    n=len(b)-1; row=b
    left=[b[0]*(1<<n)]; right=[b[-1]*(1<<n)]
    for i in range(1,n+1):
        row=[row[j]+row[j+1] for j in range(len(row)-1)]
        left.append(row[0]*(1<<(n-i)))
        right.append(row[-1]*(1<<(n-i)))
    return left,right[::-1]

seen=set()
def positive(name,r):
    assert r.q[0]>0 and all(v>=0 for v in r.q), (name,'denominator')
    p=r.p
    key=tuple(p)
    if key in seen: return
    assert p[0]>0 and p[-1]>0, (name,'endpoints')
    d=len(p)-1
    common=lcm(*(v.denominator for v in p))
    integers=[int(v*common) for v in p]
    den=lcm(*(comb(d,j) for j in range(d+1)))
    # Homogenize p at T=10000*s/(1-s). These are scaled Bernstein
    # coefficients of (1-s)^d p(10000*s/(1-s)) on [0,1].
    b=[integers[j]*10000**j*(den//comb(d,j)) for j in range(d+1)]
    stack=[(b,0)]
    while stack:
        v,depth=stack.pop()
        assert depth<=12,(name,'subdivision limit')
        assert v[0]>0 and v[-1]>0,(name,'nonpositive endpoint')
        if min(v)>=0: continue
        lo,hi=split(v);stack.extend([(lo,depth+1),(hi,depth+1)])
    seen.add(key)

T=Rat([0,1])
n=1-F(3,2)*T/(10000+T)+T/(1000+T)
e=2-T/(500+T)+2*T/(25000+T)
C=T*n.d()/n/n
k=(T+3420000)/(30*(T+200000));kx=T*k.d()
for name,r in [('n>1/2',n-F(1,2)),('n<3/2',F(3,2)-n),
               ('e>1',e-1),('e<3',3-e),('C+',F(1,2)+C),
               ('C-',F(1,2)-C),('ne>7/5',n*e-F(7,5)),
               ('g>=1',e-T*e.d()-1),('k<=57/100',F(57,100)-k)]:
    # A bound with equality at zero is checked after removing its T factors.
    if r.p[0]==0:
        pp=r.p[:]
        while pp[0]==0: pp=pp[1:]
        positive(name,Rat(pp,r.q))
    else: positive(name,r)
assert k.at(0)==F(57,100)
# k decreases to 1/30. |T k'| <= (57/100-1/30)/4.
assert F(57,100)-F(1,30)==F(161,300)
assert F(161,300)/4==F(161,1200)
assert 1-F(57,100)/2-F(161,1200)*F(4,3)==F(193,360)
print('PASS source bounds and leading damping bound 193/360',flush=True)

# Derive H_logT by differentiating each actual source-potential coefficient.
inv=1/n
gA=-e*inv;gX=e*inv;gU=e*inv*inv;gW=inv*inv
HA=kx*gA+k*T*gA.d()
HX=kx*gX+k*(T*gX.d()+gX)
HU=kx*gU+k*T*gU.d()
HW=kx*gW+k*(T*gW.d()+gW)
controls=0
checked_matrices=set()
for stage in (0,1,2):
    a=F(stage);wm=(F(0),F(9,2),F(15))[stage]
    for u,eta in ((0,0),(0,1),(1,0)):
        U=F(3,2)*a*u;w=wm*(1-u)*eta
        for theta in (0,1):
            x=a*theta;D=e+x;B=U*(n-e)-w
            Hx=a*HA+x*HX+U*HU+w*HW
            for y in (F(2,3),F(2)):
                key=(a,x,U,w,y)
                controls+=1
                if key in checked_matrices: continue
                checked_matrices.add(key)
                r=y-inv;A=D+k*C+kx*r
                K=B-k*(D-n)+(32-k*k)*C+Hx-k*kx*r
                Q=32*(n-k*C)-k*Hx
                positive('growth control',4*A*Q-K*K)
    print('PASS growth Bernstein stage',stage,flush=True)
assert controls==36
assert len(checked_matrices)==26
# Verify degree-two Bernstein geometry exactly, rather than sample positivity.
for u,eta in ((0,0),(0,1),(1,0)):
    for theta in (0,1):
        # Construct the actual vertex curves with a=2s, independently
        # of the displayed control table; compare power coefficients.
        ap=[F(0),F(2)]
        curves=[ap,scale(ap,theta),scale(ap,F(3,2)*u),
                scale(mul(ap,add(ap,[3])),F(3,2)*(1-u)*eta)]
        table=[(0,0,0,0),(1,theta,F(3,2)*u,F(9,2)*(1-u)*eta),
               (2,2*theta,3*u,15*(1-u)*eta)]
        basis=[[1,-2,1],[0,2,-2],[0,0,1]]
        for j,curve in enumerate(curves):
            expanded=[F(0)]
            for stage in range(3):
                expanded=add(expanded,scale(basis[stage],table[stage][j]))
            assert expanded==trim(curve),('Bernstein geometry',u,eta,theta,j)
print('PASS 36 growth control choices, 26 distinct tuples, and Bernstein geometry',flush=True)

# Limitation of this particular energy outside the certified interval.
# This is a triangle vertex at a=5/2, x=w=0, U=3a/2 and y=2.
a=F(5,2);x=F(0);U=F(3,2)*a;w=F(0);r=2-inv
D=e+x;B=U*(n-e)-w;Hx=a*HA+x*HX+U*HU+w*HW
A=D+k*C+kx*r
K=B-k*(D-n)+(32-k*k)*C+Hx-k*kx*r
Q=32*(n-k*C)-k*Hx
assert (4*A*Q-K*K).at(100000)<0
print('PASS energy limitation at a=5/2',flush=True)

# Printed-rate coefficient conditions and both envelope endpoints.
D=mul([10000,1],[1000,1]);De=mul([500,1],[25000,1])
t=[F(0),F(1)]
N=add(sub(D,scale(mul(t,[1000,1]),F(3,2))),mul(t,[10000,1]))
E=add(sub(scale(De,2),mul(t,[25000,1])),scale(mul(t,[500,1]),2))
W=sub(mul(der(N),D),mul(N,der(D)));Cn=mul(t,W)
assert all(v>0 for v in sub(mul(N,E),scale(mul(D,De),F(7,5))))
for sign in (-1,1):
    pp=add(scale(mul(N,N),F(1,2)),scale(Cn,sign))
    assert len(pp)==5 and all(pp[j]>0 for j in (0,1,2,4))
    assert pp[3]>=0 or pp[3]**2<4*pp[2]*pp[4]
assert F(8500)-F(9,16)>0
assert F(1,4)+F(3,2)/200==F(103,400)
for a,Mn,c,m,target in [(F(13,25),F(3,2),F(1,2),F(7,5),F(858,625)),
                        (F(27,50),F(2),F(103,400),F(1),F(492237,500000))]:
    L=max(a*Mn*(a+3),a*Mn*(Mn-1))
    assert c*L==target<m
    delta=m-c*L;q=L/c;eps=min(L,delta/(5*c))
    assert 4*q*m-(2*L+eps)**2>=3*L*delta/c>0
print('PASS envelope endpoint products 858/625<7/5; 492237/500000<1',flush=True)

# Fixed-growth energy certificate, fold geometry and multiplicity bound.
a=F(257,500);b=F(51,50000000000)
Bs=[-3*a*(a+3)/2-F(1,1000),3*a/4]
assert Bs==[F(-1355147,500000),F(771,2000)]
for B in Bs:
    left=scale(mul(power(N,5),add(E,scale(mul(t,De),a*b))),32)
    right=mul(mul(D,De),add(power(add(scale(power(N,2),B),scale(Cn,8)),2),power(N,4)))
    pp=sub(left,right)
    assert len(pp)==14 and all(v>0 for v in pp)
assert F(1,4)/(15+a)==F(125,7757)
G=sub(mul(E,De),mul(t,sub(mul(der(E),De),mul(E,der(De)))))
assert all(v>0 for v in G)
Q0=sub(mul([1,-b],W),scale(mul(N,D),b))
def changes(p):
    signs=[1 if v>0 else -1 for v in p if v]
    return sum(x!=y for x,y in zip(signs,signs[1:]))
assert changes(Q0)==1 and ev(Q0,0)>0 and ev(Q0,2200)<0
VN=scale(mul(power(E,2),Q0),a);VD=mul(power(D,2),G)
minusvp=sub(mul(VN,der(VD)),mul(der(VN),VD))
assert all(v>0 for v in bern_interval(minusvp,F(2200)))
Vfold=Rat(VN,VD);Ufold=a*(1-b*T)*n-T*Vfold/e
assert (Ufold.d()+T*Vfold.d()/e).p==[0]
assert Vfold.at(0)==F(10922486893,12500000000000)
assert Ufold.at(0)==a
# Exact brackets for the approximate fold endpoint coordinates in the text.
lo,hi=F(213260,100),F(213261,100)
assert ev(Q0,lo)>0>ev(Q0,hi)
assert F(72839,100000)<a*(1-b*lo)*n.at(lo)
# N and D have positive coefficients. Thus throughout [lo,hi],
# n(T)<=N(hi)/D(lo), irrespective of whether n is monotone.
assert all(v>0 for v in N+D)
assert a*(1-b*lo)*ev(N,hi)/ev(D,lo)<F(72840,100000)
Pbase=mul(mul(scale([1,-b],a),N),E);PU=mul(D,E);PV=mul(t,mul(D,De))
tau=[(Pbase[j]/PU[j],-PV[j]/PU[j]) for j in range(5)]
for hi,lo in ((4,3),(3,2)):
    assert tau[hi][0]-tau[lo][0]<0 and tau[hi][1]-tau[lo][1]<=0
cross=[]
for hi,lo in ((2,1),(1,0)):
    c0=tau[hi][0]-tau[lo][0];c1=tau[hi][1]-tau[lo][1]
    assert c0>0 and c1<0;cross.append(-c0/c1)
assert 0<cross[0]<cross[1] and Pbase[5]<0 and PV[5]>0
# The threshold sequence is unimodal; its positive coefficients form a block.
# Together with the negative leading coefficient this proves <=2 variations.
assert F(1,2)-a/4==F(743,2000)
assert F(3,4)-a/8==F(2743,4000)
print('PASS two degree-13 certificates; margin 125/7757; fold and root bound',flush=True)

# Exact Laurent-polynomial calculus for the generic energy identities.
# Negative powers occur only for the positive variable n. Jets are independent.
names='T y z a b U V n nt e et k kt p r G Gt'.split()
size=len(names);index={s:i for i,s in enumerate(names)}
class Poly:
    def __init__(self,terms=None):self.terms={m:F(v) for m,v in (terms or {}).items() if v}
    def __add__(self,o):
        o=poly(o);d=self.terms.copy()
        for m,v in o.terms.items():d[m]=d.get(m,0)+v
        return Poly(d)
    __radd__=__add__
    def __neg__(self):return Poly({m:-v for m,v in self.terms.items()})
    def __sub__(self,o):return self+-poly(o)
    def __rsub__(self,o):return poly(o)+-self
    def __mul__(self,o):
        o=poly(o);d={}
        for m,v in self.terms.items():
            for mm,w in o.terms.items():
                key=tuple(a+b for a,b in zip(m,mm));d[key]=d.get(key,0)+v*w
        return Poly(d)
    __rmul__=__mul__
    def diff(self,s):
        i=index[s];d={}
        for m,v in self.terms.items():
            if m[i]:
                mm=list(m);mm[i]-=1;d[tuple(mm)]=v*m[i]
        return Poly(d)
def poly(v):return v if isinstance(v,Poly) else Poly({(0,)*size:F(v)})
def var(s,power=1):
    m=[0]*size;m[index[s]]=power;return Poly({tuple(m):1})
def zero(v):assert not v.terms
TT,yy,zz,aa,bb,UU,VV,nn,nt,ee,et,kk,kt,pp,rrr,gg,gt=map(var,names)
ni=var('n',-1);Ci=TT*nt*ni*ni
pi=aa*(1-bb*TT)-UU*yy-VV*zz;ri=yy-ni
Fi=aa*(1-bb*TT)-UU*ni-VV*TT*ni*var('e',-1)
Td=TT*pi;yd=1-nn*yy;zd=TT*yy-ee*zz
pd=pi.diff('T')*Td+pi.diff('y')*yd+pi.diff('z')*zd
rd=ri.diff('T')*Td+ri.diff('n')*nt*Td+yd
zero(rd-(-nn*ri+Ci*pi))
zero(pd-(-(aa*bb*TT+ee)*pi+ee*Fi+(UU*(nn-ee)-VV*TT)*ri))
# Differentiate the whole shifted expression with P_T=G/T, R_T=-HC/T.
H=kk*gg*ni;v=pp-kk*rrr
energy=v*v*F(1,2)+32*rrr*rrr*F(1,2)+H*rrr
pr=-(aa*bb*TT+ee)*pp-gg+(UU*(nn-ee)-VV*TT)*rrr
rrd=-nn*rrr+Ci*pp
Ed=energy.diff('p')*pr+energy.diff('r')*rrd
Ed+=(energy.diff('n')*nt+energy.diff('k')*kt+energy.diff('G')*gt)*TT*pp
Ed+=gg*pp-H*Ci*pp
Hx=TT*(kt*gg*ni+kk*gt*ni-kk*gg*nt*ni*ni)
Ai=aa*bb*TT+ee+kk*Ci+TT*kt*rrr
Ki=UU*(nn-ee)-VV*TT-kk*(aa*bb*TT+ee-nn)+(32-kk*kk)*Ci+Hx-kk*TT*kt*rrr
Qi=32*(nn-kk*Ci)-kk*Hx
zero(Ed-(-Ai*v*v+Ki*v*rrr-Qi*rrr*rrr))
print('PASS exact differential identities, including variable shift derivative')
# Full equilibrium Jacobian, in relative population coordinates.
A0=aa*bb*TT;C0=UU*ni;K0=VV*TT*ni*var('e',-1)
X=TT*nt;g=ee-TT*et
J=[[-A0,-C0,-K0],[-X,-nn,poly(0)],[g,ee,-ee]]
def det3(M):
    return M[0][0]*(M[1][1]*M[2][2]-M[1][2]*M[2][1])-M[0][1]*(M[1][0]*M[2][2]-M[1][2]*M[2][0])+M[0][2]*(M[1][0]*M[2][1]-M[1][1]*M[2][0])
a1=-(J[0][0]+J[1][1]+J[2][2])
a2=poly(0)
for i,j in ((0,1),(0,2),(1,2)):
    a2+=J[i][i]*J[j][j]-J[i][j]*J[j][i]
a3=-det3(J)
zero(a1-(A0+nn+ee))
zero(a2-(A0*(nn+ee)+nn*ee-C0*X+K0*g))
zero(a3-(A0*nn*ee-(C0+K0)*ee*X+K0*nn*g))
Fp=-aa*bb+UU*nt*ni*ni-VV*ni*var('e',-1)+VV*TT*nt*ni*ni*var('e',-1)+VV*TT*et*ni*var('e',-2)
zero(a3+TT*nn*ee*Fp)
zero(a1*a2-a3-(A0*A0*(nn+ee)+A0*(nn+ee)*(nn+ee)+nn*ee*(nn+ee)-C0*X*(A0+nn)+K0*g*(A0+ee)+K0*ee*X))
positive('X<=1/4',F(1,4)-T*n.d())
positive('X>=-3/8',F(3,8)+T*n.d())
print('PASS full Jacobian characteristic polynomial and Routh rate bounds')
print('ALL CHECKS PASS')

"""Second exact positivity route: subdivision, with no Sturm/root library.

Input is the referee's own polynomial output. Map T=10000*t/(1-t),
then prove positivity of the homogeneous polynomial on [0,1] by the
Bernstein convex-hull property and exact integer de Casteljau subdivision.
"""
import hashlib,json,math,pathlib,time
root=pathlib.Path('/workspace/ref_victor_VB31')
start=time.time()
obj=json.loads((root/'independent_result.json').read_text())
results=[]
def split(b):
    n=len(b)-1
    row=b
    left=[b[0]*(1<<n)]; right=[b[-1]*(1<<n)]
    for i in range(1,n+1):
        row=[row[j]+row[j+1] for j in range(len(row)-1)]
        left.append(row[0]*(1<<(n-i)))
        right.append(row[-1]*(1<<(n-i)))
    return left,right[::-1]
for pol in obj['polynomials']:
    coeff=pol['coefficients'][::-1]; degree=pol['degree']
    assert coeff[0]>0 and coeff[-1]>0
    denom=math.lcm(*(math.comb(degree,j) for j in range(degree+1)))
    bern=[coeff[j]*10000**j*(denom//math.comb(degree,j)) for j in range(degree+1)]
    stack=[(bern,0)]; leaves=0; deepest=0
    while stack:
        b,depth=stack.pop(); deepest=max(deepest,depth)
        assert depth<=50,('subdivision limit',pol['sha256'])
        # Strict positivity follows even with an interior zero coefficient
        # when endpoints are positive and every coefficient is nonnegative.
        if min(b)>=0 and b[0]>0 and b[-1]>0:
            leaves+=1
        else:
            assert b[0]>0 and b[-1]>0,('nonpositive endpoint',pol['sha256'],depth)
            left,right=split(b)
            stack.extend([(left,depth+1),(right,depth+1)])
    rec={'sha256':pol['sha256'],'degree':degree,'leaves':leaves,'max_depth':deepest}
    results.append(rec); print('PASS',rec,flush=True)
result={'status':'PASS','method':'exact integer Bernstein subdivision; T=10000*t/(1-t)',
        'polynomials':len(results),'checks':results,'elapsed_s':time.time()-start}
(root/'bernstein_result.json').write_text(json.dumps(result,indent=2))
print('ALL SECOND-ROUTE POSITIVITY CHECKS PASS',len(results),time.time()-start,flush=True)

"""Only train and validation experimental targets enter this worker."""
import copy
import json
import sys
import time
from pathlib import Path

import numpy as np
import torch
from torch.nn import functional as F
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'synfactor'))
from model import SynFactor

class NeuralAdditive(SynFactor):
    def __init__(self):
        super().__init__(2058, tasks=1, rank=1, hidden=64)

    def forward(self, components, present):
        total=self.factor(components[:,0],0)+self.factor(components[:,1],1)
        return (total.squeeze(-1)*self.output_scale+self.output_bias)*self.y_scale+self.y_mean

def run(key,name,mode,kind,seed):
    prefix='audit/'+key+'-'+name
    dest=Path(f'{prefix}-{kind}_{mode}-{seed}.npz')
    if dest.exists():
        with np.load(dest) as prev:
            assert np.isfinite(prev['pred']).all()
        return
    start=time.monotonic()
    torch.set_num_threads(4)
    torch.manual_seed(seed)
    d=np.load(prefix+'-inputs.npz')
    ids=torch.from_numpy(d['ids'])
    tr,va,te=map(torch.from_numpy,(d['tr'],d['va'],d['te']))
    n=len(tr)+len(va)+len(te)
    if mode=='C':
        tr=torch.cat([tr,torch.arange(n,len(ids))])
    if mode=='D':
        y=torch.zeros(n)
        y[tr]=torch.from_numpy(d['yfit']).float()
        y[va]=torch.from_numpy(d['yval']).float()
    else:
        y=torch.from_numpy(d['teacher']).float()
    bce=mode=='D' and bool(d['binary'])
    x=torch.from_numpy(np.load('audit/'+key+'-features.npy'))
    net=SynFactor(2058,tasks=1,rank=16,hidden=64) if kind=='CP' else NeuralAdditive()
    # Third slot is absent; upstream train.py indexes embedding zero there.
    ids=torch.cat([ids,torch.zeros(len(ids),1,dtype=torch.long)],dim=1)
    present=torch.tensor([True,True,False])
    with torch.no_grad():
        # Bound the memory used by repeated Cartesian synthon occurrences.
        occurrences=ids[tr,:2].flatten()
        hist=torch.bincount(occurrences,minlength=len(x)).double()
        weights=hist/hist.sum()
        xd=x.double()
        mean=weights@xd
        sd=torch.sqrt(weights@(xd-mean).square())
        net.x_mean.copy_(mean)
        net.x_scale.copy_(torch.where(sd>1e-5,sd,1.))
        del xd
        if not bce:
            net.y_mean.copy_(y[tr].mean())
            net.y_scale.copy_(y[tr].std().clamp_min(1e-6))
    def infer(batch):
        return net(x[ids[batch]],present.expand(len(batch),3)).flatten()
    def evaluate(indices):
        return torch.cat([infer(b) for b in indices.split(256)])
    optimizer=torch.optim.AdamW(net.parameters(),lr=.002,weight_decay=.002)
    best,stale,state=float('inf'),0,None
    for epoch in range(1,301):
        net.train()
        for batch in tr[torch.randperm(len(tr))].split(256):
            p=infer(batch)
            if bce:
                loss=F.binary_cross_entropy_with_logits(p,y[batch])
            else:
                loss=F.huber_loss((p-net.y_mean)/net.y_scale,(y[batch]-net.y_mean)/net.y_scale)
            optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(net.parameters(),5.)
            optimizer.step()
        net.eval()
        with torch.no_grad():
            p=evaluate(va)
            cost=(F.binary_cross_entropy_with_logits(p,y[va]) if bce else ((p-y[va])/net.y_scale).square().mean()).item()
        if cost<best-1e-5:
            best,stale,state,at=cost,0,copy.deepcopy(net.state_dict()),epoch
        else:
            stale+=1
        if stale>=35:
            break
    net.load_state_dict(state)
    net.eval()
    with torch.inference_mode():
        pred=evaluate(te).numpy()
    assert np.isfinite(pred).all()
    tmp=dest.with_suffix('.part.npz')
    np.savez(tmp,pred=pred,best_epoch=at,epochs=epoch,seconds=time.monotonic()-start)
    tmp.replace(dest)
    print(key,name,mode,kind,seed,epoch,round(time.monotonic()-start,1),flush=True)

if __name__=='__main__':
    key,name=sys.argv[1:]
    for mode in ('D','C','T'):
        for seed in (42,43,44):
            for kind in ('A','CP'):
                run(key,name,mode,kind,seed)

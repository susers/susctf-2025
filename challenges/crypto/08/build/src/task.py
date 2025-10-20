import random as random2
import os
from datetime import *
from sage.all import *

rng=random2.Random()
rng.seed(os.urandom(48))

class LFSR:
    def __init__(self,n,p,seed,mask):
        self.n=n
        self.p=p
        self.mask=mask[:n]
        self.state=seed[:n]

    def getstate(self):
        ret=sum([u*v%self.p for u,v in zip(self.state,self.mask)])%self.p
        self.state.append(ret)
        self.state.pop(0)
        return ret

q=251
R=PolynomialRing(Zmod(q),'X')
X=R.gen(0)

QR=R.quo(X**256+X+6)
ERR=list(range(q))
shuffle(ERR)


ESEED=[rng.randint(0,6) for _ in range(5)]
ESEED[rng.randint(0,4)]=rng.randint(1,6)
EMASK=[rng.randint(0,6) for _ in range(5)]
EMASK[rng.randint(0,4)]=rng.randint(1,6)
rng.seed(os.urandom(33))
rng.shuffle(ESEED)
rng.shuffle(EMASK)
lfsr57=LFSR(5,7,ESEED,EMASK)

token=''.join([random2.choice('0123456789ABCDEFGHJK')for _ in range(256)])
s=[ord(ch) for ch in token]
s=QR(s)
seedA=os.urandom(48).hex()
print('seedA= ',seedA)

rngA=random2.Random()
rngA.seed(seedA)
for i in range(548):
    op=int(input('Give me your option>'))
    if(op==1):
        A=QR([rngA.randint(0,q-1) for _ in range(256)])
        e=QR([ERR[lfsr57.getstate()] for _ in range(256)])
        print('Your Cipher=',list(A*s+e))
    elif(op==2):
        token1=input('GIVE ME MY TOKEN>').strip()
        if(token1==token):
            print('Congraduations! Here is your flag:',os.getenv('GZCTF_FLAG'))
        else:
            print('Sorry, Wrong Token')

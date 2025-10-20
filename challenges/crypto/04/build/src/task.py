import random as random2
import os
from sage.all import *
from sage.stats.distributions.discrete_gaussian_integer import DiscreteGaussianDistributionIntegerSampler as DGDIS
n=128
p=31337
D=DGDIS(sigma=1) #Generate the discrete gaussian distribution with sigma = 1

flag=os.getenv('GZCTF_FLAG')+''.join([random2.choice('0123456789ABCDEGHJK')for _ in range(n)])
seedA=''.join([random2.choice('0123456789ABCDEFGHJK') for _ in range(24)])
print('Public Seed:'+seedA)
rng=random2.Random()
rng.seed(seedA.encode())
while(1):
    A=matrix(Zmod(p),[[rng.randint(0,99) for _ in range(n)]for __ in range(n)])
    if(A.rank()==n):
        break

rng.seed(os.urandom(48))

s=vector(Zmod(p),[rng.randrange(200,p-200,200)+ord(flag[i]) for i in range(n)])

for i in range(548*2):
    op=int(input('Give me your choice>'))
    if(op==1):
        e=vector(Zmod(p),[D() for _ in range(n)])
        print(list(A*s+e))
    else:
        break

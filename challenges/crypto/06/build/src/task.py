from Crypto.Util.number import *
from random import *
from os import urandom,getenv


token=''.join([choice('ABCDEFGHJK0123456789')for _ in range(90)])

class LFSR:
    def __init__(self,n,p,seed):
        self.n=n
        self.p=p
        self.mask=[1]+[randint(0,p-1) for _ in range(n-1)]
        self.state=seed[:n]
        while(len(self.state)<n):
            self.state.append(len(self.state))
    def getstate(self):
        ret=sum([u*v%self.p for u,v in zip(self.state,self.mask)])%self.p
        self.state.append(ret)
        self.state.pop(0)
        return ret

p=getPrime(208)
h=32328345448461253988278351927
lfsr1=LFSR(45,p,[randrange(200,p-200,200)+ord(i) for i in token[:45]])
lfsr2=LFSR(45,h,[randrange(200,h-200,200)+ord(i) for i in token[45:]])
print(f'p={p}')
print(f'mask={lfsr1.mask}')
MONEY = 97
isHint=False
cHint=800
for i in range(500):
    MENU=f"""
++++++MENU+++++++++
+1.Guess      $  1+
+2.BuyHint    $350+
+3.SubmitTkn $2000+
+0.Exit           +
++++++NFSR+3+++++++
DOLLAR:{str(MONEY).zfill(4)}
CHANCE:{str(500-i).zfill(4)}
"""
    print(MENU)
    op=int(input('Choice>'))
    if(op==1):
        MONEY-=1
        x=int(input('Your Guess>'))
        u=lfsr1.getstate()^((lfsr2.getstate()))
        if(u==x):
            print(f'AC, Your answer:{x} Right answer:{u}')
            MONEY+=7
        elif(abs(u-x)<=h):
            print(f'PC, Your answer:{x} Right answer:{u}')
            MONEY+=2
        else:
            print(f'WA, Your answer:{x} Right answer:{u}')
        if(MONEY==0):
            exit(0)
    elif(op==2):
        if(MONEY<350):
            print(f'Sorry, The hint cost $350, You only have ${MONEY}')
            continue
        else:
            MONEY-=350
            print(f'lfsr2.mask={lfsr2.mask}')
            print(f'lfsr2.state={lfsr2.state}')
            isHint=True
    elif(op==3):
        if(MONEY<2000):
            print(f'Sorry, token submission cost $2000, You only have ${MONEY}')
        else:
            MONEY-=2000
            token1=input('NOW! GIVE ME MY TOKEN!>').strip()
            if(token1.upper()==token):
                FLAG=getenv('GZCTF_FLAG')
                print(f'Congraduations! here is your flag!!!:{FLAG}')
            else:
                print('Sorry, but I think you could have your flag...')
    else:
        exit(0)
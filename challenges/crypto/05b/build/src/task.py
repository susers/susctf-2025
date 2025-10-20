from Crypto.Util.number import *
from random import *
from os import *

p=int(input('Please give me a 32~50 bit prime modulus>'))

if(not isPrime(p) or p.bit_length()<=32 or p.bit_length()>=50):
    print('Invalid parameter!')
    exit(0)

RODICT=dict()
USED=set()

def RandomOracle(x):
    global USED,RODICT
    if(RODICT.get(x,None) is not None):
        return RODICT[x]
    while(1):
        r=bytes_to_long(urandom(48))%p
        if(r not in USED):
            USED|={r}
            RODICT[x]=r
            return r

state=[randint(1,p-1) for _ in range(randint(256,512))]
visited=False
for i in range(200):
    op=int(input('Give me your option>'))
    if(op==1):
        msg=input("Input your message array(Decimal Format)>")
        #input example: 1 2 3 4 5 6 7 8 9 10 100 999 10000
        msg=msg.split()
        msg=msg[:512]
        ciph=[]
        for ch in msg:
            cur=state.pop(0)
            ciph.append(cur+RandomOracle(int(ch)))
            state.append(pow(cur,2*(getrandbits(2)+1)+1,p))
        print(ciph)

    elif(op==2):
        if(visited):
            print('Only one chance!')
            continue
        else:
            visited=True
            ret=[]
            flag=getenv('GZCTF_FLAG')
            for ch in flag:
                chi=ord(ch)
                cur=state.pop(0)
                ret.append(RandomOracle(chi)+cur)
                state.append(pow(cur,2*(getrandbits(2)+1)+1,p))
            print('Cipher of flag=',ret)

    else:
        break

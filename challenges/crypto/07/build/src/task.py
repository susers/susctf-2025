from Crypto.Util.number import *
import os
from sage.all import *
import random as random2
BANNER="""
 ######  ##     ##  ######   ######  ######## ########     #######    #####    #######  ######## 
##    ## ##     ## ##    ## ##    ##    ##    ##          ##     ##  ##   ##  ##     ## ##       
##       ##     ## ##       ##          ##    ##                 ## ##     ##        ## ##       
 ######  ##     ##  ######  ##          ##    ######       #######  ##     ##  #######  #######  
      ## ##     ##       ## ##          ##    ##          ##        ##     ## ##              ## 
##    ## ##     ## ##    ## ##    ##    ##    ##          ##         ##   ##  ##        ##    ## 
 ######   #######   ######   ######     ##    ##          #########   #####   #########  ###### 

 ######  ########  ##    ## ########  ########  #######     ######## 
##    ## ##     ##  ##  ##  ##     ##    ##    ##     ##    ##    ## 
##       ##     ##   ####   ##     ##    ##    ##     ##        ##   
##       ########     ##    ########     ##    ##     ##       ##    
##       ##   ##      ##    ##           ##    ##     ##      ##     
##    ## ##    ##     ##    ##           ##    ##     ##      ##     
 ######  ##     ##    ##    ##           ##     #######       ##     
"""
print(BANNER)

globalPrime=26959946667150639794667015087019630673637144422540572481103610249153
def GetFlag():
    flag=os.getenv('GZCTF_FLAG').encode()
    upperBoundPrime=2**1280-2**512+2**128-2**40-2**16-8+1
    p=previous_prime(random2.randint(0,upperBoundPrime))
    q=next_prime(random2.randint(0,upperBoundPrime))
    e=1435756429
    n=p*q
    c=pow(bytes_to_long(flag),e,n)
    print(f'N={n}')
    print(f'e={e}')
    print(f'c={c}')
    print(f'hint={q>>960}')

def Chall():
    p=int(input('Give me your prime>'))
    if(p.bit_length()<226 or p.bit_length()>333 or not isPrime(p)):
        print('Invaid prime!')
        exit(1)
    a,b=[int(i)%p for i in input('Give me your parameters>').split()]
    assert a**2+b**2
    v=2
    while(pow(v,p>>1,p)==1):
        v+=1
    Fq2=GF((p,2),modulus=[-v,0,1],name='sqv')
    E=EllipticCurve(Fq2,[a,b])
    x1,x2=[Zmod(p)(i) for i in input('Give me 2 base points(x_coordinate)>').split()]
    G1=E.lift_x(x1)
    G2=E.lift_x(x2)
    assert G1.order()==G2.order()
    orderG=G1.order()

    def ListG(Gx):
        Gxy=Gx.xy()
        r=[]
        r=list(Gxy[0])+list(Gxy[1])
        return tuple(r)
    print(f'Your Point G1: {ListG(G1)}')
    print(f'Your Point G2: {ListG(G2)}')

    for i in range(44):
        u,v=random2.randint(0,globalPrime),random2.randint(0,globalPrime)
        print(f'Your Point:{ListG(u*G1+v*G2)}')
        u1,v1=[int(i) for i in input('Give me your answer Result>').split()]
        assert u1==u and v1==v

for _ in range(2):
    op=int(input('Give me your option>'))
    if(op==1):
        GetFlag()
    elif(op==2):
        Chall()
    else:
        exit(0)

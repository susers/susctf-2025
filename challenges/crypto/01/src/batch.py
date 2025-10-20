import subprocess
import sys
from gmpy2 import *
from random import *
from Crypto.Util.number import *
# from sage.all import *

FLAGID=40000000
BATCH=200
# BATCH=3
def encrypt(m):
    def keyGen():
        sp,sq=f'{1+2*randint(1000000,4999999)}',f'{1+2*randint(1000000,4999999)}'
        for _ in range(32):
            sp=sp+'0'*25+f'{1+2*randint(1000000,4999999)}'
        for _ in range(32):
            sq=sq+'0'*25+f'{1+2*randint(1000000,4999999)}'
        p,q=int(sp),int(sq)
        p,q=int(next_prime(p)),int(next_prime(q))
        return p,q
    p,q=keyGen()
    n=p*q
    e=getPrime(1024)*getPrime(1024)*getPrime(1024)
    m=bytes_to_long(m.strip().encode())
    c=pow(m,e,n)
    return f"{n=}\n{e=}\n{c=}\n"

D = {
    'a':'aA4@',
    'b':'bB83',
    'c':'cC',
    'd':'dD<',
    'e':'eE3&',
    'f':'fF',
    'g':'gG9&',
    'h':'hH#',
    'i':'iI1!|',
    'j':'jJ;',
    'k':'kK',
    'l':'lL1|',
    'm':'mM',
    'n':'nN',
    'o':'oO0',
    'p':'pP',
    'q':'qQ9',
    'r':'rR',
    's':'sS5$',
    't':'tT7',
    'u':'uU',
    'v':'vV',
    'w':'wW',
    'x':'xX',
    'y':'yY',
    'z':'zZ2',
}
def L33T(s):
    s=s.lower()
    ret=''
    for ch in s:
        if ord(ch) not in range(97,97+26):
            ret+=ch
        else:
            ret+=choice(D[ch])
    return ret

def getFlag():
    global FLAGID
    flagorg='attention_is_all_you_need_hahaha_'
    flag=L33T(flagorg)
    FLAGID+=getrandbits(10)
    flag+=f'{FLAGID}!'
    return 'susctf{'+flag+'}'
def run():
    s = getFlag()
    res=encrypt(s)
    with open(s,'w') as f:
        f.write(res)

i=0
while(i<BATCH):
    try:
        run()
        i+=1
    except Exception as e:
        print(e)

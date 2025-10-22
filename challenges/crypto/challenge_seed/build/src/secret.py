import os
from Crypto.Util.number import bytes_to_long
import random

#SEEDS = [bytes_to_long(os.urandom(32)) for i in range(2)]
#print(SEEDS)

SEED = random.choice([114438242418500378879743348760306365125002337895160466519161057447289480013785, 105990105334969385266002827131889388579428813846831487901535629356257879538989])

with open('/flag', 'r') as f:
    flag = f.read()

import os
from Crypto.Util.number import bytes_to_long
import random

SEEDS = [bytes_to_long(os.urandom(32)) for i in range(2)]
print(SEEDS)

with open('/flag', 'r') as f:
    flag = f.read()

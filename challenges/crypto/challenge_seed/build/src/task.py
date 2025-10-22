import random
from secret import SEED, flag

random.seed(SEED)
print('Hello, ctfer!')

correct = 0
while True:
    secret = random.randint(0,2**10)
    res = int(input('Input your guess:'))
    if res != secret:
        print(f'Wrong! The secret is: {secret}')
        break
    else:
        correct += 1
    if correct == 10:
        print('Congratulations!')
        print(flag)
        break

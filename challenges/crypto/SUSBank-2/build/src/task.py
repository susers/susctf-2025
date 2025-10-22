import random
import secrets
from functools import reduce

from Crypto.Util.number import *
from gmpy2 import next_prime, iroot


def generate(pl):
    while True:
        l = list(random.sample(pl[:-1], 4))
        scaled_l = [next_prime(iroot(x, 3)[0]) for x in l]
        candidate = 2 * pl[-1] * reduce(lambda x, y: x * y, scaled_l) + 1
        if isPrime(candidate):
            print(f"big_prime = {candidate}")
            break
    return candidate


print("-----SUS Bank Service 2-----")
prime_bag = [getPrime(64) for _ in "SUS Bank Service 2"]
assert len(set(prime_bag)) == len(prime_bag)
n = reduce(lambda x, y: x * y, prime_bag[:-2])
e = 65537
balance = 0
token = 1
print(f"your account number: {n}\npassword: {e}\nbalance: {balance}")

while True:
    i = input(
        "please input your choice:\n1.Get a token\n2.Deposit\n3.Validate your balance\n4.Exit\n"
    )
    if i == "1":
        print("Your token is:", prime_bag[-2])
        try:
            if r1 > 1:
                r1 = secrets.randbelow(r1)
        except NameError:
            r1 = secrets.randbelow(n >> 4)
        c = pow(r1, e, n)
        print(f"Encrypted current token: {c}")
        try:
            res = int(input("Now please give me your token to verify:"))
            if res == r1:
                print("You can get in now!")
                r1 = secrets.randbelow(n >> 4)
                token = 2
            else:
                raise ValueError
        except ValueError:
            token = 1
            print("Nope. Please wait for your turn.")
    if i == "2":
        print("Hello, ctfer!")
        if token != 2:
            print("You are not allowed to get in now! Please wait for your turn.")
            continue
        big_prime = generate(prime_bag)
        try:
            deposit = int(input("How much will you deposit?\n"))
            if deposit < 0 or deposit > big_prime >> 2:
                raise ValueError("Invalid deposit")
            deposit = next_prime(deposit)
        except ValueError:
            deposit = 0
        r2 = secrets.randbelow(prime_bag[-1])
        c = pow(deposit, r2, big_prime)
        print(f"Here is a proof of your deposit: {c}")
        try:
            sign = int(input("Please sign here   "))
            if pow(deposit, sign, big_prime) == c:
                balance += deposit
                token = 3
            else:
                raise ValueError
        except ValueError:
            print("Invalid sign")
            token = 2
    if i == "3":
        if token < 2:
            print("You are not allowed to get in now! Please wait for your turn.")
            continue
        print("Ready to get your flag?")
        if balance == bytes_to_long(b"SUS2025"):
            print("Welcome, SUSer!")
            with open("/flag", "r") as f:
                print(f.read())
        else:
            print("Try again!")
            print(f"You have {balance} yuan now")
    if i == "4":
        print("Bye!")
        break

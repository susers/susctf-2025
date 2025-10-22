from Crypto.Util.number import *
from gmpy2 import gcd


def work():
    import string, hashlib, random

    alphabet = string.ascii_letters + string.digits
    proof = "".join(random.choices(alphabet, k=10))
    digest = hashlib.sha256(proof.encode()).hexdigest()

    print(f"sha256(XXX+{proof[3:]})=={digest}")
    x = input("Give me XXX:")
    h = hashlib.sha256((x + proof[3:]).encode()).hexdigest()
    return h == digest


"""How you work （你可以直接复制以下代码，爆破sha256不在考察范围内）
import hashlib <-如果提示没有这些库，请安装一下
import itertools
import string

def find_xxx(proof_suffix, target_digest):
    alphabet = string.ascii_letters + string.digits  # a-z, A-Z, 0-9
    for candidate in itertools.product(alphabet, repeat=3):
        xxx = ''.join(candidate)
        test_proof = xxx + proof_suffix
        test_digest = hashlib.sha256(test_proof.encode()).hexdigest()
        if test_digest == target_digest:
            return xxx  # Found the correct XXX
    return None  # If no match is found

proof_suffix = "6AwuiE5" <-这里填入后缀
target_digest = "594bd9791b89c27fa9cc84e48cb68a30eae21b5c92bccca21d3ee59c8c2e002f" <-这里填入哈希值

xxx = find_xxx(proof_suffix, target_digest)
if xxx:
    print(f"Found XXX: {xxx}") <-在这个示例中，会输出"Found XXX: N0t"
else:
    print("No matching XXX found.")
"""

print("-----SUS Bank Service-----")
p, q = [getPrime(1024) for i in range(2)]
n = p * q
e = getPrime(128)
assert gcd(e, (p - 1) * (q - 1)) == 1
balance = 0
rand = 0
d = inverse(e, (p - 1) * (q - 1))
print(
    f"your account number: {n}\npassword: {e}\nencrypted balance: {pow(balance, d, n)}"
)

while True:
    i = input(
        "please input your choice:\n1.Earn money\n2.check balance\n3.Validate your balance\n4.Exit\n"
    )
    if i == "1":
        if work():
            balance += 1
            print("You earn 1 yuan!")
    if i == "2":
        rand = getPrime(16)
        print(f"Your balance is: {pow(balance, d, n) + rand}.")
    if i == "3":
        deposit = int(input("please input your deposit(before decryption):"))
        check_deposit = pow(deposit - rand, e, n)
        if (
            check_deposit.bit_length() >= 1024
        ):  # if you input a random number as the balance, it will probably be detected and banned
            print("How can you have so much money? You must be cheating!!")
            continue
        if check_deposit > bytes_to_long(b"SUS"):
            print("Wow! You are a SUSer! Here is your flag")
            with open("./flag", "r") as f:
                flag = f.read()
                print(flag)
                break
        else:
            print("Nice try! But you should get richer to have flag!")
            print(f"Your balance is: {check_deposit}.")
    if i == "4":
        print("Bye!")
        break

from gmpy2 import next_prime
from pwn import *
import hashlib
import itertools
import string


def find_xxx(suffix, target_digest):
    alphabet = string.ascii_letters + string.digits  # a-z, A-Z, 0-9
    for candidate in itertools.product(alphabet, repeat=3):
        xxx = "".join(candidate)
        test_proof = xxx + suffix
        test_digest = hashlib.sha256(test_proof.encode()).hexdigest()
        if test_digest == target_digest:
            return xxx
    return None


conn = remote("106.14.191.23", 56302)
context.log_level = "debug"
conn.recvuntil(b"number: ")
n = int(conn.recvline())
conn.recvuntil(b"password: ")
password = int(conn.recvline())
print("接收到所有数据！")
for i in "01":
    conn.recvuntil(b"Exit\n")
    conn.sendline(b"1")
    conn.recvuntil(b"sha256(XXX+")
    suffix = conn.recvuntil(b")==", drop=True).decode()
    target_hash = conn.recvline().strip().decode()
    conn.recvuntil(b"XXX:")

    xxx = find_xxx(suffix, target_hash)
    if xxx:
        print(f"Found XXX: {xxx}")
        conn.sendline(xxx.encode())
    else:
        print("No matching XXX found.")
        conn.close()

# 此时应该已经有2元
conn.recvuntil(b"Exit\n")
conn.sendline(b"2")
conn.recvuntil(b"is: ")
balance = int(conn.recvline())
pure_balance = 0
prime = 1
while prime < 0x10000:  # 暴力破解16位以下的prime
    prime = next_prime(prime)
    pure_balance = balance - prime
    ans = pow(pure_balance, password, n)
    if ans.bit_length() < 1024:
        print(ans, "\n", prime, "\n", pure_balance)
        assert ans == 2
        break
result = pow(pure_balance, 25, n) + prime  # 2的25次方已经大于bytes_to_long(b"SUS")
conn.sendline(b"3")
conn.recvuntil(b"decryption):")
conn.sendline(str(result).encode())
conn.recvline()
conn.interactive()

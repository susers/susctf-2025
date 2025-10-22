from pwn import *

guess = [
    "136",
    "960",
]  # 你们改了那两个种子吗？改了就得换成第一个数，本地实测是136和432，随便选的136
context.log_level = "debug"
while True:
    conn = remote("106.14.191.23", 58942)
    conn.recvuntil(b"guess:")
    for i in range(11):
        conn.sendline(guess[i].encode())
        result = conn.recvuntil(
            ":"
        )  # 这一行兼具读取正确后的Input your guess:与错误后的Wrong! The secret is:两种功能
        if b"Wrong" in result:
            guess[i] = result.decode().split(": ")[-1].strip()
            guess.append("0")
        elif b"Congratulations!" in result:
            conn.interactive()
        else:
            continue

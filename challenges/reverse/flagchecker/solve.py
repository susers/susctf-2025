# secret = [ord(i) for i in "susctf{C6eck3r_Revers3d}"]
secret = [
    0x7E,
    0x61,
    0x68,
    0x41,
    0x5D,
    0x56,
    0x4C,
    0x7D,
    0x73,
    0x29,
    0x30,
    0x31,
    0x52,
    0x1A,
    0x30,
    0x24,
    0x18,
    0xF2,
    0xEE,
    0xE0,
    0xEA,
    0x93,
    0xC3,
    0xD3,
]

password_chars = []
for i in range(len(secret)):
    original_char = secret[i] ^ ((i * 7 + 13) & 0xFF)
    password_chars.append(chr(original_char))

password = "".join(password_chars)
print("Recovered password:", password)
# print("Recovered password:", ", ".join([hex(ord(i)) for i in password_chars]))

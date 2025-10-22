from Crypto.Util.number import *


class ModularMagic:
    def __init__(self, core: list[int], mod: int) -> None:
        assert isinstance(core, list) and len(core) == 4
        self.mod = mod
        self.C = core

    def magic(self, v: list[int]) -> list[int]:
        for i in range(2):
            v[i] = (v[i // 2] * self.C[i] + v[(i + 2) // 2] * self.C[i + 2]) % self.mod
        return v


flag = b"###"
assert len(flag) == 30 and flag.startswith(b"susctf{") and flag.endswith(b"}")
pure_flag = flag[7:-1]

flag1 = bytes_to_long(pure_flag[:11])
flag2 = bytes_to_long(pure_flag[11:])
flag_list = [flag1, flag2]

p = getPrime(128)
modular = ModularMagic([1349874547, 26990, 285337416819, 2], p)  # four 'magic' numbers

for i in range(10):
    flag_list = modular.magic(flag_list)

print(f"p = {p}")
print(flag_list)

"""
p = 269362074288207307542642012900174543199
[50930964716312266177839139457723607648, 201050527555147895574798415306904201600]
"""

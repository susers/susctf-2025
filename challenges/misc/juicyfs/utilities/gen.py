#!/usr/bin/env python3
import os, sys, random, textwrap

FNV_OFFSET = 1469598103934665603
FNV_PRIME  = 1099511628211
MASK = (1<<64) - 1

def fnv1a_mix_u8(h, v):
    h ^= v
    h = (h * FNV_PRIME) & MASK
    return h

def xs64s_next(x):
    x ^= (x >> 12) & MASK
    x ^= (x << 25) & MASK
    x ^= (x >> 27) & MASK
    x = (x * 2685821657736338717) & MASK
    return x

def emit_array_uint32(name, vals):
    lines = []
    row = []
    for i, v in enumerate(vals):
        row.append(str(v) + "U")
        if len(row) >= 16:
            lines.append(", ".join(row))
            row = []
    if row: lines.append(", ".join(row))
    return f"static const uint32_t {name}[{len(vals)}] = {{\n  " + ",\n  ".join(lines) + "\n};\n"

def emit_array_uint8(name, vals):
    lines = []
    row = []
    for i, v in enumerate(vals):
        row.append(str(v))
        if len(row) >= 32:
            lines.append(", ".join(row))
            row = []
    if row: lines.append(", ".join(row))
    return f"static const uint8_t {name}[{len(vals)}] = {{\n  " + ",\n  ".join(lines) + "\n};\n"

def main():
    if len(sys.argv) < 4:
        print("Usage: make_chall.py 'CTF{flag}' <blob_size_mb> <num_indices>")
        sys.exit(1)
    flag = sys.argv[1].encode("utf-8")
    size_mb = int(sys.argv[2])
    num_idx = int(sys.argv[3])

    size = size_mb * 1024 * 1024
    print(f"[+] Generating {size_mb} MB blob.bin ...")
    blob = os.urandom(size)
    with open("blob.bin", "wb") as f:
        f.write(blob)

    print(f"[+] Picking {num_idx} random indices ...")
    # Unique indices across the blob
    idxs = random.sample(range(size), k=num_idx)

    print("[+] Deriving seed from blob bytes (FNV-1a 64-bit) ...")
    h = FNV_OFFSET
    for idx in idxs:
        b = blob[idx]
        t = idx
        for _ in range(8):  # mix index bytes
            h = fnv1a_mix_u8(h, t & 0xff)
            t >>= 8
        h = fnv1a_mix_u8(h, b)

    if h == 0:
        h = 0x9E3779B97F4A7C15  # avoid zero state

    print("[+] Encrypting flag with xorshift64* keystream ...")
    s = h
    ct = bytearray(len(flag))
    for i in range(len(flag)):
        s = xs64s_next(s)
        ks = (s >> 56) & 0xff  # top byte
        ct[i] = flag[i] ^ ks

    print("[+] Writing gen_data.h ...")
    with open("gen_data.h", "w") as out:
        out.write("#pragma once\n#include <stdint.h>\n\n")
        out.write(f"#define NUM_IDXS {len(idxs)}\n")
        out.write(f"#define CT_LEN {len(ct)}\n")
        out.write(f"static const uint64_t blob_expected_size = {size}ULL;\n\n")
        out.write(emit_array_uint32("idxs", idxs))
        out.write("\n")
        out.write(emit_array_uint8("ct", ct))
        out.write("\n")

    print("[+] Done. Next steps:")
    print("  objcopy -I binary -O elf64-x86-64 -B i386:x86-64 blob.bin blob.o")
    print("  gcc -O2 -s main.c blob.o -o chall   # add -static if you want it even bigger")

if __name__ == "__main__":
    main()

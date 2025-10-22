import pickle

flag = [
    115,
    117,
    115,
    99,
    116,
    102,
    123,
    49,
    109,
    95,
    80,
    49,
    99,
    107,
    108,
    51,
    100,
    95,
    117,
    87,
    117,
    125,
]
# susctf{1m_P1ckl3d_uWu}


def encode_flag(flag):
    # Pickle the flag string using the highest protocol
    return pickle.dumps(flag, protocol=-1)


def main():
    encoded_flag = encode_flag(flag)
    print(encoded_flag)


if __name__ == "__main__":
    main()


"""
b'\x80\x05\x951\x00\x00\x00\x00\x00\x00\x00]\x94(KsKuKsKcKtKfK{K1KmK_KPK1KcKkKlK3KdK_KuKWKuK}e.'
"""
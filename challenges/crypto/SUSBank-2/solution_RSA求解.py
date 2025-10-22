import math


def product(numbers):
    """
    计算一个列表中所有数字的乘积。

    Args:
        numbers (list[int]): 包含整数的列表。

    Returns:
        int: 列表中所有数字的乘积。
    """
    result = 1
    for number in numbers:
        result *= number
    return result


def calculate_phi(primes):
    """
    根据给定的不重复质数列表计算欧拉函数 φ(n)。
    n 是所有这些质数的乘积。
    φ(n) = (p1-1) * (p2-1) * ... * (pk-1)

    Args:
        primes (list[int]): 不重复的质数列表。

    Returns:
        int: 欧拉函数 φ(n) 的值。
    """
    if not primes:
        return 0

    phi_factors = [(p - 1) for p in primes]
    return product(phi_factors)


def extended_gcd(a, b):
    """
    扩展欧几里得算法。
    返回 (gcd, x, y) 使得 a*x + b*y = gcd。
    我们将用它来计算模逆元。
    """
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = extended_gcd(b % a, a)
        return (g, x - (b // a) * y, y)


def modInverse(e, phi_n):
    """
    计算 e 关于 phi_n 的模逆元 d。
    d * e ≡ 1 (mod phi_n)

    Args:
        e (int): 公钥指数。
        phi_n (int): 欧拉函数 φ(n) 的值。

    Returns:
        int: 私钥指数 d。
    """
    # 在 Python 3.8+ 中，可以直接使用 pow(e, -1, phi_n)
    try:
        # 这是更现代、更高效的方法
        return pow(e, -1, phi_n)
    except (ValueError, TypeError):
        # 如果 pow 函数失败或版本过低，则回退到手动实现
        g, x, y = extended_gcd(e, phi_n)
        if g != 1:
            raise Exception('模逆元不存在 (e 和 φ(n) 不互质)')
        return x % phi_n


def decrypt_variant_rsa(primes, c, e=65537):
    """
    对变种 RSA 进行解密。

    Args:
        primes (list[int]): 用于构成 n 的所有不重复的质数列表。
        c (int): 待解密的密文。
        e (int, optional): 公钥指数。默认为 65537。

    Returns:
        int: 解密后的明文。
    """
    # 步骤 1: 计算模数 n
    n = product(primes)
    print(f"计算得到的模数 n = {n}\n")

    # 步骤 2: 计算欧拉函数 φ(n)
    phi_n = calculate_phi(primes)
    print(f"计算得到的欧拉函数 φ(n) = {phi_n}\n")

    # 步骤 3: 计算私钥 d
    print(f"正在计算公钥 e = {e} 关于 φ(n) 的模逆元 d...")
    d = modInverse(e, phi_n)
    print(f"计算得到的私钥 d = {d}\n")

    # 步骤 4: 解密消息 m = c^d mod n
    print(f"正在执行解密: m = c^d mod n...")
    print(f"c = {c}")
    print(f"d = {d}")
    print(f"n = {n}")

    m = pow(c, d, n)
    print("\n解密完成！")

    return m


# --- 示例 ---
if __name__ == '__main__':
    # 假设我们已知以下信息

    # 1. 构成 n 的质数列表 (这里使用一些较小的质数作为示例)
    known_primes = [10127759509377869369 , 10727180704304539213 , 10884797493293174131 , 11206472106812234543 , 12024642194926540757 , 12143590433465821751 , 12186908573309000957 , 12230380628802569243 , 12600307272648602333 , 12922047619780672777 , 13983391223160594623 , 14068828809764454053 , 15862322796247191713 , 16807383370975935173 , 17680583573560994507 , 18263603119276970027]

    # 2. 公钥指数 e
    e = 65537

    # 3. 原始消息 m (用于加密生成密文 c)
    #    注意：m 必须小于 n
    original_message = 42

    # --- 首先，我们模拟加密过程以获得密文 c ---
    n_example = product(known_primes)
    # c = m^e mod n
    c_example = 299161035261023219665454436563130250285479881392744347903247995597836042974469310193850074993642661153538571895965996883505299010409535525661040795878190454011285887750705940487325762211449715518262707470686064016395080569432509749911115710222633019468023834381670905566504172265826891389412710074266767823

    print("-------------------- 模拟场景 --------------------")
    print(f"已知质数列表: {known_primes}")
    print(f"公钥指数 e: {e}")
    print(f"原始消息 m (用于验证): {original_message}")
    print(f"由 m 加密得到的密文 c: {c_example}")
    print("--------------------------------------------------\n")

    # --- 现在，使用我们的解密函数 ---
    # 假设我们只知道 known_primes, c_example 和 e

    try:
        decrypted_message = decrypt_variant_rsa(known_primes, c_example, e)

        print("\n-------------------- 结果 --------------------")
        print(f"解密后的消息: {decrypted_message}")
        print("--------------------------------------------------")


    except Exception as ex:
        print(f"\n发生错误: {ex}")
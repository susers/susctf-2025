# -*- coding: utf-8 -*-

def solve_dlp_small_range(p1, p2, p3, p4, p5, g, h):
    """
    利用 Pohlig-Hellman 算法和 SageMath 的内置离散对数求解器，
    找到 x mod (2*p1*p2*p3) 的解。
    """
    # 1. 计算完整的模数 p 和 p-1
    p = 2 * p1 * p2 * p3 * p4 * p5 + 1
    if not is_prime(p):
        print(f"错误：计算出的 p = {p} 不是一个素数，请更换p1-p4的值。")
        return None
    
    order = p - 1
    print(f"成功构造素数 p = {p}")
    print(f"群的阶 p-1 = {order}")
    print("-" * 50)
    
    # 2. 定义有限域 GF(p) 并转换 g 和 h
    F = GF(p)
    g_field = F(g)
    h_field = F(h)
    
    # 3. Pohlig-Hellman 核心部分
    small_factors = [p1, p2, p3, p4]
    congruences = [] # 用于存储 (x_i, p_i) 对
    
    print("开始执行 Pohlig-Hellman 算法分解问题...")
    for pf in small_factors:
        print(f"\n--- 正在处理小因子 p_i = {pf} ---")
        
        # 3a. 降阶 (Order Reduction)
        N = order // pf
        g_sub = g_field ^ N
        h_sub = h_field ^ N
        
        print(f"子问题的生成元 g' = g^((p-1)/{pf}) = {g_sub}")
        print(f"子问题的目标 h' = h^((p-1)/{pf}) = {h_sub}")
        
        # 3b. 利用 Sage 内置功能解决子问题
        # h_sub.log(g_sub) 等价于求解 g_sub^x_sub = h_sub
        try:
            x_sub = discrete_log(h_sub, g_sub, ord=pf)
            print(f"成功解出子问题：x ≡ {x_sub} (mod {pf})")
            congruences.append((x_sub, pf))
        except ValueError:
            print(f"错误：无法在子群（阶为{pf}）中求解离散对数。可能 h' 不在 g' 生成的子群中。")
            return None

    print("\n" + "-" * 50)
    print("所有子问题已解决，得到以下同余方程组：")
    for res, mod in congruences:
        print(f"x ≡ {res} (mod {mod})")
        
    # 4. 使用中国剩余定理 (CRT) 合并解
    results = [c[0] for c in congruences]
    moduli = [c[1] for c in congruences]
    
    x_small = crt(results, moduli)
    M = 2 * p1 * p2 * p3 * p4
    
    print("\n使用中国剩余定理合并解...")
    print(f"最终解出：x ≡ {x_small} (mod {M})")
    
    return x_small, M

# ===================================================================
# ---                  在这里填充你的参数                      ---
# ===================================================================

p1 = 2237813   
p2 = 2298577   
p3 = 2605159   
p4 = 2561549  
p5 = 12355561016553105419
g = 23456238879650023
h = 840880366854626313647503019657877701889792766 


# ===================================================================
# ---                      运行求解器                        ---
# ===================================================================

# 调用主函数求解
solution = solve_dlp_small_range(p1, p2, p3, p4, p5, g, h)

if solution:
    x_small_solution, M_solution = solution
    
    # ===================================================================
    # ---                         验证结果                        ---
    # ===================================================================
    print("\n" + "="*50)
    print("开始验证结果...")
    print(f"我们求出的解是: x ≡ {x_small_solution} (mod {M_solution})")
    print(f"pow(g,x,p) = {pow(g,x_small_solution,2 * p1 * p2 * p3 * p4 * p5 + 1)}")
    print(f"h = {h}")

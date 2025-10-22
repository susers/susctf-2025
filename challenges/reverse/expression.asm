section .data
    menu_msg: 
        times 30 db "-", 
        db 0xA, 
        db "|         Calculator         |", 0xA, 
        db "| 1. Input flag to calculate |", 0xA, 
        db "| 2. WIP!                    |", 0xA, 
        db "| 3. Exit                    |", 0xA, 
        times 30 db "-", 
        db 0xA, 
        db "Please enter a command (1-3): ", 0

    menu_msg_len equ $ - menu_msg

    calculate_msg db "Please enter a mathematical expression: ", 0
    calculate_msg_len equ $ - calculate_msg

    result_msg db "The expression evaluates to ", 0
    result_msg_len equ $ - result_msg

    success_msg db "Correct!", 0
    success_msg_len equ $ - success_msg

    wrong_msg db "Wrong!", 0
    wrong_msg_len equ $ - wrong_msg
    
    wrong_type_msg db "How can you get a float result?", 0
    wrong_type_msg_len equ $ - wrong_type_msg

    flag_msg db "fakeflag{Happy_ASM}", 0
    flag_msg_len equ $ - flag_msg

    ; 错误信息字符串
    error0 db "Error: Unknown command", 0x0A
    error0_len equ $ - error0

    error1 db "Error: Division by zero", 0x0A
    error1_len equ $ - error1

    error2 db "Error: Unknown operator", 0x0A
    error2_len equ $ - error2

    error3 db "Error: Expression syntax error", 0x0A
    error3_len equ $ - error3

    error4 db "Error: Invalid number", 0x0A
    error4_len equ $ - error4

    float_zero db "0.0", 0x0A
    float_zero_len equ $ - float_zero

    float_nan db "NaN", 0x0A
    float_nan_len equ $ - float_nan

    float_inf db "Infinity", 0x0A
    float_inf_len equ $ - float_inf

    command db 0                ; 定义一个 1 字节的变量存储命令
    input_length db 0           ; 定义一个 1 字节的变量存储输入长度
    digit_buffer_length db 0    ; 定义一个 1 字节的变量存储数字缓冲区长度

    operator1 db 0              ; 定义一个 1 字节的变量存储运算符，用于比较优先级
    operator2 db 0              ; 定义一个 1 字节的变量存储运算符，用于比较优先级
    priority1 db 0              ; 定义一个 1 字节的变量存储优先级
    priority2 db 0              ; 定义一个 1 字节的变量存储优先级

    constant_one dd 1.0         ; 定义常量 1.0
    constant_ten dd 10          ; 定义常量 10
    power_result dd 0           ; 定义一个 4 字节的变量存储 power_of_ten 的结果
    temp_converting_result dd 0 ; 定义一个 4 字节的变量存储 临时结果
    temp_converting_ascii dd 0  ; 定义一个 4 字节的变量存储 转换的 ASCII 数字

    converted_num dd 0          ; 定义一个 4 字节的变量存储转换的数字
    converted_num_type db 0     ; 定义一个 1 字节的变量存储结果类型

    operator db 0               ; 定义一个 1 字节的变量存储操作符
    operand1 dd 0               ; 定义一个 4 字节的变量存储操作数1
    operand1_type db 0          ; 定义一个 1 字节的变量存储操作数1类型
    operand2 dd 0               ; 定义一个 4 字节的变量存储操作数2
    operand2_type db 0          ; 定义一个 1 字节的变量存储操作数2类型
    operator_count db 0         ; 定义一个 1 字节的变量存储操作符数目

    too_many_ops_msg db "Error: Too many operators", 0x0A
    too_many_ops_msg_len equ $ - too_many_ops_msg

    spare_operator db 0         ; 定义一个 1 字节的变量存储运算符，用于保存临时运算符

    operator_stack_top dd 1     ; 定义 4 字节的 operator 栈顶指针索引
    operand_type_stack_top dd 1 ; 定义 4 字节的 operand_type 栈顶指针索引
    operand_stack_top dd 1      ; 定义 4 字节的 operand 栈顶指针索引
    
    result dd 0                 ; 定义一个 4 字节的变量存储结果
    result_type db 0            ; 定义一个 1 字节的变量存储结果类型
    result_length db 0          ; 定义一个 1 字节的变量存储结果长度
    result_sign db 0            ; 定义一个 1 字节的变量存储结果符号

    ; 定义控制字操作变量
    old_cw dw 0
    new_cw dw 0

    log10_2 dd 0.30102999566    ; log10(2)
    result_exp_2 dd 0           ; 定义一个 4 字节的变量存储结果指数，以 2 为底数（浮点数用）
    result_exp_10 dd 0          ; 定义一个 4 字节的变量存储结果指数，以 10 为底数（浮点数用）

    result_binary_mantissa dd 0 ; 定义一个 4 字节的变量存储结果尾数，进制为 2（浮点数用）
    result_decimal_mantissa dd 0; 定义一个 4 字节的变量存储结果尾数，进制为 10（浮点数用）

    int_part dd 0               ; 浮点数：整数部分
    int_part_length dd 0        ; 整数部分长度
    fraction_part dd 0.0        ; 浮点数：小数部分
    fraction_part_length dd 0   ; 小数部分长度

    temp_int dd 0               ; 转换整数时的临时变量
    temp_digit dd 0             ; 转换小数时的临时变量

    equals_sign db " = "
    equals_sign_len equ $ - equals_sign

    page_command db 0           

section .bss
    command_buffer resb 2       ; 定义 2 字节缓冲区（含 null）
    input_buffer resb 256       ; 定义 256 字节缓冲区
    digit_buffer resb 10        ; 定义 10 字节的数字缓冲区

    operator_stack resb 256     ; 定义 256 字节的操作符栈
    operand_type_stack resb 256 ; 定义 256 字节的操作数类型栈
    operand_stack resd 256      ; 定义 256 个 4 字节的操作数栈

    result_buffer resb 20       ; 定义 12 字节的结果缓冲区：负号 + 最大 18 位数字 + 换行符

    int_part_buffer resb 10     ; 定义 10 字节的整数结果缓冲区：倒序输入
    fraction_part_buffer resb 6 ; 定义 6 字节的小数结果缓冲区：正序输入（精度为6）

    mantissa_buffer resb 10
    exp_buffer resb 10

    page_command_buffer resb 2



section .text
    global _start

; ----------------------------------- calculate 函数调用函数 ----------------------------------- ;
;-------------------------------------
; 函数：错误处理
; 参数：
;   eax = 错误码（0/1/2/3/4）
;-------------------------------------
error_handler:
    push ebx
    push ecx
    push edx

    ; switch(eax)
    cmp eax, 0
    je handle_error0
    cmp eax, 1
    je handle_error1
    cmp eax, 2
    je handle_error2
    cmp eax, 3
    je handle_error3
    cmp eax, 4
    je handle_error4

    ; 如果 eax 不是 0/1/2/3/4，默认处理为未知错误
    jmp handle_error0

    end_error_handler:
        pop edx
        pop ecx
        pop ebx
        ret

    handle_error0:
        ; 输出 "Error: Unknown command"
        mov eax, 4          ; sys_write
        mov ebx, 1          ; 标准输出
        mov ecx, error0     ; 错误信息地址
        mov edx, error0_len ; 错误信息长度
        int 0x80
        jmp end_error_handler

    handle_error1:
        ; 输出 "Error: Division by zero"
        mov eax, 4
        mov ebx, 1
        mov ecx, error1
        mov edx, error1_len
        int 0x80
        jmp end_error_handler   

    handle_error2:
        ; 输出 "Error: Unknown operator"
        mov eax, 4
        mov ebx, 1
        mov ecx, error2
        mov edx, error2_len
        int 0x80
        jmp end_error_handler

    handle_error3:
        ; 输出 "Error: Expression syntax error"
        mov eax, 4
        mov ebx, 1
        mov ecx, error3
        mov edx, error3_len
        int 0x80
        jmp end_error_handler

    handle_error4:
        ; 输出 "Error: Invalid number"
        mov eax, 4
        mov ebx, 1
        mov ecx, error4
        mov edx, error4_len
        int 0x80
        jmp end_error_handler


;-------------------------------------
; 函数：获取操作符的优先级
; 参数：
;   eax = 操作符
; 返回：
;   ebx = 优先级
;-------------------------------------
get_priority:
    push ecx
    push edx

    cmp al, '+'            ; '+' 的优先级
    je _plus_priority
    cmp al, '-'            ; '-' 的优先级
    je _minus_priority
    cmp al, '*'            ; '*' 的优先级
    je _multiply_priority
    cmp al, '/'            ; '/' 的优先级
    je _divide_priority

    xor ebx, ebx           ; 默认优先级为 0

    end_get_priority:
        pop edx
        pop ecx
        ret

    _plus_priority:
        mov ebx, 1         ; '+' 的优先级为 1
        jmp end_get_priority

    _minus_priority:
        mov ebx, 1         ; '-' 的优先级为 1
        jmp end_get_priority

    _multiply_priority:
        mov ebx, 2         ; '*' 的优先级为 2
        jmp end_get_priority

    _divide_priority:
        mov ebx, 2         ; '/' 的优先级为 2
        jmp end_get_priority


;-------------------------------------
; 函数：检查字符是否为数字
; 参数：
;   al = 要检查的字符
; 返回：
;   ebx = 1（是数字），0（不是数字）
;-------------------------------------
is_digit:
    push ecx
    push edx

    ; al <= '2' && al >= '1'
    cmp al, '1'
    jb not_digit
    cmp al, '2'
    ja not_digit

    comfirm_digit:
        mov ebx, 1             ; 是数字
        jmp end_is_digit

    not_digit:
        xor ebx, ebx       ; 不是数字

    end_is_digit:
        pop edx
        pop ecx
        ret 


;-------------------------------------
; 函数：计算 10^edx
; 参数：
;   edx = 负数幂次
; 返回：
;   [power_result] = 结果
;-------------------------------------
power_of_ten:
    push eax
    push ebx
    push ecx

    fld dword [constant_one]

    calculate_power_loop:
        cmp edx, 0
        je end_calculate_power_loop

        fidiv dword [constant_ten]
        inc edx
        jmp calculate_power_loop

    end_calculate_power_loop:
        fstp dword [power_result]
        pop ecx
        pop ebx
        pop eax
        ret


;-------------------------------------
; 函数：字符串转换为 32 位数字
; 参数：
;   [digit_buffer] = 数字字符串（最大长度为 10 位）
;   [digit_buffer_length] = 数字字符串长度
; 返回：
;   digit_buffer 被清空
;   [converted_num] = 转换后的 32 位数字
;   [converted_num_type] = 转换后的数字类型
;-------------------------------------
string_to_number:
    push eax
    push ebx
    push ecx
    push edx
    push esi
    push edi
    finit

    ; 初始化截断模式
    ; 1. 保存原始控制字
    fnstcw [old_cw]         ; 将当前控制字保存到 old_cw

    ; 2. 设置新控制字（向零舍入）
    mov ax, [old_cw]
    and ax, 0xF3FF          ; 清除 RC 字段（第10-11位）
    or ax, 0x0C00           ; 设置 RC=0b11（向零舍入）
    mov [new_cw], ax
    fldcw [new_cw]          ; 加载新控制字到 FPU

    ; 查找小数点位置
    mov esi, digit_buffer           ; esi 指向字符串
    mov ecx, [digit_buffer_length]
    xor edx, edx                    ; edx 记录小数点位置（无小数点则为 -1）
    mov edi, 0                      ; edi 记录小数点位置

    find_dot_loop:
        lodsb                       ; al = [esi], esi++
        cmp al, '.'
        je found_dot

        inc edi
        loop find_dot_loop

    ; 循环结束，未找到小数点
    not_dot:
        mov byte [converted_num_type], 0
        jmp integer_convert_process

    ; 中途找到小数点
    ; edi = 小数点 '.' 的索引
    found_dot:
        mov byte [converted_num_type], 1
        jmp float_convert_process


    integer_convert_process:
        ; 字符串转整数 
        mov esi, digit_buffer           ; esi 指向数字字符串
        mov ecx, [digit_buffer_length]  ; ecx = 字符串长度，即循环次数
        xor ebx, ebx                    ; ebx 存储最终结果
        xor eax, eax                    ; al 存储当前字符

        integer_convert_loop:
            ; 算法：result = result * 10 + (current_char - '0')
            lodsb                       ; al = [esi], esi++
            sub al, '0'                 ; 将ASCII字符转为数字（'3' → 3）

            imul ebx, ebx, 10           ; result *= 10
            add ebx, eax                ; result += current_char

            loop integer_convert_loop

        mov [converted_num], ebx        ; 保存结果
        jmp clear_digit_buffer

    float_convert_process:
        ; 算法：
        ;   [0, dot_index): result = result * 10 + (str[i] - '0')
        ;   [dot_index + 1, len): result += (str[i] - '0') * pow(10, dot_index - i)
        
        ; 字符串转浮点数
        mov esi, digit_buffer           ; esi 指向数字字符串
        xor ebx, ebx                    ; ebx 存储最终结果
        xor eax, eax                    ; al 存储当前字符

        mov ecx, edi                    ; ecx = 小数点索引，即循环次数
        ; 整数部分转换
        float_convert_integer_part_loop:
            lodsb                       ; al = [esi], esi++
            sub al, '0'                 ; 将ASCII字符转为数字（'3' → 3）

            imul ebx, ebx, 10           ; result *= 10
            add ebx, eax                ; result += current_char
            loop float_convert_integer_part_loop


        ; 当前 ebx = 整数部分，需要转换为浮点数
        ; 定义：
        ;   esi = i
        ;   edi = dot_index
        ;   ebx = result 
        mov esi, edi
        xor eax, eax
        inc esi                         ; 跳过小数点

        ; 转换为浮点数
        mov dword [temp_converting_result], ebx
        fild dword [temp_converting_result]
        fstp dword [temp_converting_result]

        ; 小数部分转换
        float_convert_float_part_loop:
            ; 循环结束条件
            cmp esi, [digit_buffer_length]
            je end_float_convert_float_loop

            ; 计算 (str[i] - '0')
            xor eax, eax
            mov al, [digit_buffer + esi]
            sub al, '0'
            mov dword [temp_converting_ascii], eax
            fild dword [temp_converting_ascii]

            ; 计算 dot_index - i
            mov edx, edi
            sub edx, esi
            call power_of_ten

            ; 计算 result
            fmul dword [power_result]
            fadd dword [temp_converting_result]
            fstp dword [temp_converting_result]

            inc esi
            jmp float_convert_float_part_loop


        end_float_convert_float_loop:
            ; 将[temp_converting_result] -> [converted_num]
            ; 定义 converted_num_type 为 1
            mov eax, dword [temp_converting_result]
            mov dword [converted_num], eax


            jmp clear_digit_buffer



    clear_digit_buffer:
        ; 清空缓冲区
        mov edi, digit_buffer           ; edi 指向缓冲区
        mov ecx, [digit_buffer_length]  ; 需要清空的字节数
        xor eax, eax                    ; al = 0（填充值）
        rep stosb                       ; 循环填充 0：[edi] <- al, edi++, ecx--

        ; 清空长度
        mov byte [digit_buffer_length], 0 ; 清空长度

    pop edi
    pop esi
    pop edx
    pop ecx
    pop ebx
    pop eax
    ret


;-------------------------------------
; 函数：将 input_buffer 字符串中的数字存入 digit_buffer
; 参数：
;   input_buffer = 输入字符串的地址
;   esi = 当前数字字符的第一个索引
; 返回：
;   esi = 连续数字字符的最后一个索引
;   调用 string_to_number 函数
;-------------------------------------
save_number:
    push eax
    push ebx
    push ecx
    push edx
    push edi

    ; 初始化目标缓冲区指针和长度计数器
    mov edi, 0                          ; edi 指向数字缓冲区初始位置
    mov byte [digit_buffer_length], 0   ; 初始化长度为0

    save_number_loop:
        ; 检查是否到达字符串末尾
        cmp esi, [input_length]
        jge end_save_number_loop                    ; 如果到达末尾，跳出循环

        ; 检查当前字符是否为数字
        movzx eax, byte [input_buffer + esi]        ; 无符号拓展：eax = 当前数字字符
        call is_digit
        cmp ebx, 1
        jne end_save_number_loop

        cmp edi, 3
        jae number_too_long                         ; 如果已经 >=3，则报错/退出

        ; 如果是数字，存入缓冲区
        mov byte [digit_buffer + edi], al           ; 存储当前数字字符
        inc edi                                     ; 目标指针 + 1
        inc esi                                     ; 源指针 + 1
        jmp save_number_loop                 

    number_too_long:
        mov eax, 3
        call error_handler
        jmp menu

    end_save_number_loop:  
        ; 结束循环，保存长度
        mov [digit_buffer_length], edi              ; 保存长度
        dec esi                                     ; 回退多读的字符
        call string_to_number

    
    end_save_number:
        pop edi
        pop edx
        pop ecx
        pop ebx
        pop eax
        ret


;-------------------------------------
; 函数：计算值
; 参数：
;   [operand1] = 操作符1 -> 先弹出来的操作数，实际上是加、减、乘、除数
;   [operand1_type] = 操作数1类型，0 代表整数，1 代表浮点数
;   [operand2] = 操作符2 -> 后弹出来的操作数，实际上是被加、减、乘、除数
;   [operand2_type] = 操作数2类型，0 代表整数，1 代表浮点数
;   [operator] = 操作符
; 返回：
;   [result] = 计算结果
;   [result_type] = 结果类型
;-------------------------------------
computation:
    push eax
    push ebx
    push ecx
    push edx
    finit                           ; 初始化 st 寄存器

    ; 初始化截断模式
    ; 1. 保存原始控制字
    fnstcw [old_cw]         ; 将当前控制字保存到 old_cw

    ; 2. 设置新控制字（向零舍入）
    mov ax, [old_cw]
    and ax, 0xF3FF          ; 清除 RC 字段（第10-11位）
    or ax, 0x0C00           ; 设置 RC=0b11（向零舍入）
    mov [new_cw], ax
    fldcw [new_cw]          ; 加载新控制字到 FPU

    ; 判断数据类型
    mov al, byte [operand1_type]
    or al, byte [operand2_type]     ; al = operand1_type | operand2_type
    jz integer_computation          ; 如果 al == 0，都是整数，跳转到整数计算
    jnz float_computation           ; 如果 al != 0，至少有一个是浮点数，跳转到浮点计算

    integer_computation:
        ; 读取 operand1 和 operand2
        mov ebx, [operand1]     ; 读取操作数1
        mov eax, [operand2]     ; 读取操作数2
        mov cl, [operator]      ; 读取操作符

        ; switch(cl)
        cmp cl, '+'             ; '+' 操作
        je integer_add
        cmp cl, '-'             ; '-' 操作
        je integer_sub
        cmp cl, '*'             ; '*' 操作
        je integer_mul
        jne invalid_operator    ; 无效操作符

        integer_add:
            add eax, ebx            ; 执行加法
            mov [result], eax       ; 保存结果
            mov byte [result_type], 0
            jmp end_computation
        integer_sub:
            sub eax, ebx            ; 执行减法
            mov [result], eax       ; 保存结果
            mov byte [result_type], 0
            jmp end_computation
        
        integer_mul:
            imul eax, ebx           ; 执行乘法
            mov [result], eax       ; 保存结果
            mov byte [result_type], 0
            jmp end_computation


    float_computation:
        ; 将操作数转换为浮点数
        mov bl, byte [operand1_type]
        cmp bl, 0
        je convert_operand1_to_float

        mov bl, byte [operand2_type]
        cmp bl, 0
        je convert_operand2_to_float
        jne read_float

        convert_operand1_to_float:
            fild dword [operand1]
            fstp dword [operand1]
            jmp read_float

        convert_operand2_to_float:
            fild dword [operand2]
            fstp dword [operand2]
            jmp read_float

        read_float:
            ; 加载操作数
            fld dword [operand2]
            mov cl, byte [operator]

            ; switch(cl)
            cmp cl, '+'             ; '+' 操作
            je float_add
            cmp cl, '-'             ; '-' 操作
            je float_sub
            cmp cl, '*'             ; '*' 操作
            je float_mul
            jne invalid_operator    ; 无效操作符

            float_add:
                fadd dword [operand1]
                fstp dword [result]
                mov byte [result_type], 1
                jmp end_computation
            
            float_sub:
                fsub dword [operand1]
                fstp dword [result]
                mov byte [result_type], 1
                jmp end_computation               

            float_mul:
                fmul dword [operand1]
                fstp dword [result]
                mov byte [result_type], 1
                jmp end_computation                                        


    computation_error_handler:
        ; 默认处理：未知操作符
        invalid_operator:
            mov eax, 2              ; 错误码 2
            call error_handler      ; 调用错误处理函数
            jmp end_computation

        division_by_zero:
            mov eax, 1              ; 错误码 1，不使用
            call error_handler      ; 调用错误处理函数
            jmp end_computation

    end_computation:
        pop edx
        pop ecx
        pop ebx
        pop eax
        ret


;-------------------------------------
; 函数：计算表达式
; 参数：
;   input_buffer = 输入表达式的地址
;   input_length = 输入表达式的长度
;   operator_stack = 操作符栈的地址
;   operand_stack = 操作数栈的地址
;   operator_stack_top = 操作符栈顶指针
;   operand_stack_top = 操作数栈顶指针
; 返回：
;   [operand_stack.top] = 结果
;-------------------------------------
evaluate_expression:
    push eax
    push ebx
    push ecx
    push edx
    push esi
    push edi

    ; 初始化 esi 输入缓冲区
    xor esi, esi

    ; 初始化 operator_stack、operand_type_stack 和 operand_stack 以及栈顶指针
    mov edi, operator_stack
    mov ecx, 256
    xor al, al
    rep stosb               ; 清空操作符栈

    mov edi, operand_type_stack
    mov ecx, 256
    xor al, al
    rep stosb               ; 清空操作数类型栈

    mov edi, operand_stack
    mov ecx, 256
    xor eax, eax
    rep stosd               ; 清空操作数栈

    mov dword [operator_stack_top], -1      ; 栈顶指针初始化为 -1
    mov dword [operand_type_stack_top], -1
    mov dword [operand_stack_top], -4
    mov byte [operator_count], 0

    ; 循环开始
    evaluate_loop:
        ; 检查是否到达字符串末尾
        cmp esi, dword [input_length]
        jge end_evaluate_loop

        ; 读取当前字符
        mov al, byte [input_buffer + esi]   ; al = 当前字符

        ; 跳过空格
        cmp al, ' '
        je skip_space

        ; 处理数字
        call is_digit                           ; 检查是否为数字
        cmp ebx, 1                              ; 如果是数字
        je handle_digit

        ; 处理左括号
        cmp al, '('
        je handle_left_bracket

        ; 处理右括号
        cmp al, ')'
        je handle_right_bracket

        ; 处理负号
        ; 布尔表达式为 (c == '-' && (i == 0 || expr[i - 1] == '('))
        
        ; c == '-'
        cmp al, '-'
        jne handle_other_operator

        ; i == 0
        cmp esi, 0
        je handle_negative
        ; expr[i - 1] == '('
        mov bl, byte [input_buffer + esi - 1]
        cmp bl, '('
        je handle_negative
        
        jne handle_other_operator

        skip_space:
            inc esi                             ; 移动到下一个字符
            jmp evaluate_loop

        handle_digit:
            call save_number                   ; 保存数字到 converted_num

            ; nums.push([converted_num])
            mov edx, [operand_stack_top]        ; 用 32位 edx 保存操作数栈顶指针索引
            add edx, 4                          ; 指针 + 4, 因为每个元素是 4 字节
            mov eax, dword [converted_num]      ; 将转换完的数字保存到 eax 中
            mov dword [operand_stack + edx], eax
            mov dword [operand_stack_top], edx  ; 更新指针索引

            ; nums_type.push([converted_num_type])
            mov edx, [operand_type_stack_top]
            inc edx
            mov al, byte [converted_num_type]
            mov byte [operand_type_stack + edx], al
            mov dword [operand_type_stack_top], edx

            inc esi                             ; 移动到下一个字符
            jmp evaluate_loop

        handle_left_bracket:
            ; ops.push(al)
            mov edx, [operator_stack_top]       ; 用 32位 edx 保存操作符栈顶指针索引
            inc edx
            mov byte [operator_stack + edx], al ; 将符号压入操作符栈中
            mov [operator_stack_top], edx       ; 更新指针索引
            
            inc esi                             ; 移动到下一个字符
            jmp evaluate_loop

        handle_right_bracket:
            ; 局部参数：
            ;   edx = [stack_top]
            ;   bl = ops.top()
            ;   eax = nums.top()
            handle_right_bracket_loop:
                ; 循环条件：!ops.empty() && ops.top() != '('
                mov edx, [operator_stack_top]   ; edx = 操作符栈顶指针
                cmp edx, -1                     ; 指针索引为 -1 代表空
                je end_handle_right_bracket_loop

                mov bl, byte [operator_stack + edx]     ; 取栈顶符号于 bl 
                cmp bl, '('
                je end_handle_right_bracket_loop

                ; 当前栈顶符号 bl 不为空且不为 '('
                
                ; 1. 符号栈出栈: bl = ops.pop()
                mov byte [operator], bl
                dec edx
                mov dword [operator_stack_top], edx

                ; 2. 取两个数 a, b 于 eax
                ; [operand1] = nums.pop()
                ; [operand2] = nums.pop()
                mov edx, [operand_stack_top]
                mov eax, [operand_stack + edx]
                mov dword [operand1], eax
                sub edx, 4                                      ; 操作数栈出栈（1个操作数为 4 字节）
                
                mov eax, [operand_stack + edx]
                mov dword [operand2], eax
                sub edx, 4

                mov dword [operand_stack_top], edx              ; 将出栈的结果保存在栈顶指针

                ; 3. 将 a, b 的数据类型保存起来
                ; [operand1_type] = nums_type.pop()
                ; [operand2_type] = nums_type.pop()
                mov edx, [operand_type_stack_top]
                mov al, byte [operand_type_stack + edx]
                mov byte [operand1_type], al
                dec edx

                mov al, byte [operand_type_stack + edx]
                mov byte [operand2_type], al
                dec edx

                mov dword [operand_type_stack_top], edx                

                ; 4. 调用 computation 函数
                call computation
                
                ; 5. 将结果压入操作数栈
                ; nums.push([result])
                mov eax, dword [result]
                mov edx, [operand_stack_top]
                add edx, 4
                mov dword [operand_stack + edx], eax
                mov dword [operand_stack_top], edx

                ; nums_type.push([result_type])
                xor eax, eax
                mov al, byte [result_type]
                mov edx, [operand_type_stack_top]
                inc edx
                mov byte [operand_type_stack + edx], al
                mov dword [operand_type_stack_top], edx

                jmp handle_right_bracket_loop

            end_handle_right_bracket_loop:
                ; 弹出左括号
                ; ops.pop()
                mov edx, [operator_stack_top]
                dec edx
                mov dword [operator_stack_top], edx

                inc esi                             ; 移动到下一个字符
                jmp evaluate_loop
                    
        handle_negative:
            ; 隐式添加 0
            ; nums.push(0)
            mov edx, dword [operand_stack_top]
            add edx, 4
            mov dword [operand_stack + edx], 0
            mov dword [operand_stack_top], edx

            mov al, [operator_count]
            inc al
            mov [operator_count], al
            cmp al, 3
            jle minus_check_ok

            mov eax, 4
            mov ebx, 1
            mov ecx, too_many_ops_msg
            mov edx, too_many_ops_msg_len
            int 0x80
            jmp menu

        minus_check_ok:
            ; ops.push('-')
            mov edx, dword [operator_stack_top]
            inc edx
            mov byte [operator_stack + edx], al
            mov dword [operator_stack_top], edx

            ; nums_type.push(integer)
            mov edx, dword [operand_type_stack_top]
            inc edx
            mov byte [operand_type_stack + edx], 0
            mov dword [operand_type_stack_top], edx

            inc esi                             ; 移动到下一个字符
            jmp evaluate_loop

        ; 处理剩余的运算符
        handle_other_operator:

            ; 循环前，先将 al = c 存入 [spare_operator]
            ; 为了使结束循环时对应
            mov [spare_operator], al

            ; 类似于处理右括号的循环
                ; 局部参数：
                ;   edx = [stack_top]
                ;   bl = ops.top()
                ;   eax = nums.top()
            handle_other_operator_loop:
                ; 循环条件：!ops.empty() && getPriority(ops.top()) >= getPriority(c)

                ; !ops.empty()
                mov edx, dword [operator_stack_top]
                cmp edx, -1
                je end_handle_other_operator_loop

                ; getPriority(ops.top()) >= getPriority(c)
                ; operator1 = c
                ; operator2 = ops.top()
                mov al, [spare_operator]
                mov [operator1], al
                mov bl, [operator_stack + edx]
                mov [operator2], bl

                ; bl = get_priority(al)
                mov al, [operator1]
                call get_priority
                mov [priority1], bl         ; priority1 = getPriority(c)
                
                mov al, [operator2]
                call get_priority
                mov [priority2], bl         ; priority2 = getPriority(ops.top())

                ; al = getPriority(c)
                ; bl = getPriority(ops.top())
                mov al, [priority1]
                mov bl, [priority2]

                cmp al, bl
                jg end_handle_other_operator_loop


                ; 1. 符号栈出栈: bl = ops.pop()
                mov bl, byte [operator_stack + edx]
                mov byte [operator], bl
                dec edx
                mov dword [operator_stack_top], edx

                ; 2. 取两个数 a, b 于 eax
                ; [operand1] = nums.pop()
                ; [operand2] = nums.pop()
                mov edx, [operand_stack_top]
                mov eax, [operand_stack + edx]
                mov dword [operand1], eax
                sub edx, 4                                      ; 操作数栈出栈（1个操作数为 4 字节）
                
                mov eax, [operand_stack + edx]
                mov dword [operand2], eax
                sub edx, 4

                mov dword [operand_stack_top], edx              ; 将出栈的结果保存在栈顶指针

                ; 3. 将 a, b 的数据类型保存起来
                ; [operand1_type] = nums_type.pop()
                ; [operand2_type] = nums_type.pop()
                mov edx, [operand_type_stack_top]
                mov al, byte [operand_type_stack + edx]
                mov byte [operand1_type], al
                dec edx

                mov al, byte [operand_type_stack + edx]
                mov byte [operand2_type], al
                dec edx

                mov dword [operand_type_stack_top], edx                

                ; 4. 调用 computation 函数
                call computation
                
                ; 5. 将结果压入操作数栈
                ; nums.push([result])
                mov eax, dword [result]
                mov edx, [operand_stack_top]
                add edx, 4
                mov dword [operand_stack + edx], eax
                mov dword [operand_stack_top], edx

                ; nums_type.push([result_type])
                xor eax, eax
                mov al, byte [result_type]
                mov edx, [operand_type_stack_top]
                inc edx
                mov byte [operand_type_stack + edx], al
                mov dword [operand_type_stack_top], edx

                mov al, [operator_count]
                inc al
                mov [operator_count], al
                cmp al, 3
                jle handle_other_operator_loop

                mov eax, 4
                mov ebx, 1
                mov ecx, too_many_ops_msg
                mov edx, too_many_ops_msg_len
                int 0x80
                jmp menu
                
                ; 将 c = spare_operator 压入 ops 栈
                end_handle_other_operator_loop:
                    mov al, byte [spare_operator]
                    mov edx, [operator_stack_top]
                    inc edx
                    mov byte [operator_stack + edx], al
                    mov dword [operator_stack_top], edx

                    inc esi                             ; 移动到下一个字符
                    jmp evaluate_loop


    end_evaluate_loop:
        ; 处理剩余运算符
        ; 循环条件：!ops.empty()
        handle_left_operator_loop:
            mov edx, dword [operator_stack_top]
            cmp edx, -1
            je end_handle_left_operator_loop
            
            ; 1. 符号栈出栈: bl = ops.pop()
            mov bl, byte [operator_stack + edx]
            mov byte [operator], bl
            dec edx
            mov dword [operator_stack_top], edx

            ; 2. 取两个数 a, b 于 eax
            ; [operand1] = nums.pop()
            ; [operand2] = nums.pop()
            mov edx, [operand_stack_top]
            mov eax, [operand_stack + edx]
            mov dword [operand1], eax
            sub edx, 4                                      ; 操作数栈出栈（1个操作数为 4 字节）
            
            mov eax, [operand_stack + edx]
            mov dword [operand2], eax
            sub edx, 4

            mov dword [operand_stack_top], edx              ; 将出栈的结果保存在栈顶指针

            ; 3. 将 a, b 的数据类型保存起来
            ; [operand1_type] = nums_type.pop()
            ; [operand2_type] = nums_type.pop()
            mov edx, [operand_type_stack_top]
            mov al, byte [operand_type_stack + edx]
            mov byte [operand1_type], al
            dec edx

            mov al, byte [operand_type_stack + edx]
            mov byte [operand2_type], al
            dec edx

            mov dword [operand_type_stack_top], edx                

            ; 4. 调用 computation 函数
            call computation
            
            ; 5. 将结果压入操作数栈
            ; nums.push([result])
            mov eax, dword [result]
            mov edx, [operand_stack_top]
            add edx, 4
            mov dword [operand_stack + edx], eax
            mov dword [operand_stack_top], edx

            ; nums_type.push([result_type])
            xor eax, eax
            mov al, byte [result_type]
            mov edx, [operand_type_stack_top]
            inc edx
            mov byte [operand_type_stack + edx], al
            mov dword [operand_type_stack_top], edx

            jmp handle_left_operator_loop

        end_handle_left_operator_loop:
            ; 将 nums.top() 存入 [result] 之中
            mov edx, [operand_stack_top]
            mov eax, [operand_stack + edx]
            mov dword [result], eax

            ; [result_type] = nums_type.top()
            mov edx, dword [operand_type_stack_top]
            mov al, byte [operand_type_stack + edx]
            mov byte [result_type], al
            
            pop edi
            pop esi
            pop edx
            pop ecx
            pop ebx
            pop eax
            ret


;-------------------------------------
; 函数：输入表达式字符串
; 参数：
;   ecx = 缓冲区地址
; 返回：
;   eax = 实际读取的字符数（不含换行符）
;-------------------------------------
read_expression_string:
    push ebx
    push ecx
    push edx

    ; 清空缓冲区（填充 0）
    cld                     ; 确保 DF=0（指针递增）
    mov edi, input_buffer   ; edi 指向缓冲区起始地址
    mov ecx, 256            ; 重复次数 = 缓冲区大小
    mov al, 0               ; 要填充的值（0）
    rep stosb               ; 重复执行：将 0 写入缓冲区

    ; 读取输入（sys_read）
    mov eax, 3              ; sys_read
    mov ebx, 0              ; stdin
    mov ecx, input_buffer   ; 传入缓冲区地址至 ecx
    mov edx, 256            ; 传入缓冲区最大大小
    int 0x80

    ; 保存实际读取的字节数
    mov [input_length], eax

    ; 将换行符（0xA）替换为 null 终止符（0）
    mov esi, ecx            ; 缓冲区地址
    add esi, eax            ; 移动到输入末尾
    dec esi                 ; 最后一个字符的位置
    cmp byte [esi], 0xA     ; 检查是否是换行符
    jne _no_newline
    mov byte [esi], 0       ; 替换为 null
    dec eax                 ; 调整字符数（排除换行符）
    mov [input_length], eax

    _no_newline:
        pop edx
        pop ecx
        pop ebx
        ret


;-------------------------------------
; 函数：打印菜单
; 参数：
;   [menu_msg] = 菜单字符串
;   [menu_msg_len] = 菜单字符串长度 
; 返回：
;   无返回值
;-------------------------------------
print_menu:
    pusha           ; 保存所有通用寄存器到栈
    pushfd          ; 保存标志寄存器

    ; 打印菜单
    mov eax, 4
    mov ebx, 1
    mov ecx, menu_msg
    mov edx, menu_msg_len
    int 0x80

    popfd           ; 恢复标志寄存器
    popa            ; 恢复所有通用寄存器
    ret


;-------------------------------------
; 函数：保存整数结果到 int_part_buffer（逆序保存）
; 参数：
;   [int_part] = 整数结果
;   int_part_buffer = 缓冲区
; 返回：
;   [int_part_length] = 结果长度
;-------------------------------------
save_integer:
    push eax
    push ebx
    push ecx
    push edx
    push esi
    push edi

    ; 初始化 int_part_buffer
    mov ecx, 10
    mov edi, int_part_buffer
    xor eax, eax
    rep stosb

    ; edi 指向缓冲区起始位置
    mov edi, int_part_buffer  

    ; 处理符号位
    mov eax, [int_part]
    xor ebx, ebx                ; ebx 记录符号标志（0=正，1=负）
    test eax, eax
    jns positive_integer_of_float
    neg eax                     ; 取绝对值
    mov ebx, 1                  ; 标记为负数

    positive_integer_of_float:

        ; 步骤3：数字转字符串（逆序存储）
        mov ecx, 10                 ; 除数
        mov esi, edi                ; esi 指向缓冲区起始位置

    integer_of_float_convert_loop:
        xor edx, edx                ; 清空 edx 用于除法
        div ecx                     ; eax = 商, edx = 余数
        add dl, '0'                 ; 将余数转为 ASCII 字符
        mov [esi], dl               ; 存储到缓冲区
        inc esi                     ; 移动到下一个位置

        test eax, eax               ; 检查商是否为0
        jnz integer_of_float_convert_loop

    ; 处理符号位
    test ebx, ebx
    jz integer_of_float_no_sign
    mov byte [esi], '-'         ; 在末尾添加负号
    inc esi

    integer_of_float_no_sign:
        ; 步骤5：计算实际长度并保存
        sub esi, edi             ; esi - edi = 字符串长度
        mov [int_part_length], esi

    end_save_integer:
        pop edi
        pop esi
        pop edx
        pop ecx
        pop ebx
        pop eax
        ret


;-------------------------------------
; 函数：保存小数结果到 fraction_part_buffer（正序保存）
; 参数：
;   [fraction_part] = 小数结果
;   fraction_part_buffer = 缓冲区
; 返回：
;   [fraction_part_length] = 结果长度
;-------------------------------------
save_fraction:
    push eax
    push ebx
    push ecx
    push edx
    push esi
    push edi

    ; 初始化截断模式
    ; 1. 保存原始控制字
    fnstcw [old_cw]         ; 将当前控制字保存到 old_cw

    ; 2. 设置新控制字（向零舍入）
    mov ax, [old_cw]
    and ax, 0xF3FF          ; 清除 RC 字段（第10-11位）
    or ax, 0x0C00           ; 设置 RC=0b11（向零舍入）
    mov [new_cw], ax
    fldcw [new_cw]          ; 加载新控制字到 FPU

    ; 初始化 fraction_part_buffer
    mov ecx, 10
    mov edi, fraction_part_buffer
    xor eax, eax
    rep stosb

    ; edi 指向缓冲区起始位置
    mov edi, fraction_part_buffer

    ; 加载小数部分到 FPU 栈
    fld dword [fraction_part]
    fabs

    ; 提取小数位，最多 6 位
    mov ecx, 6

    fraction_of_float_convert_loop:
        ; 乘以10获取当前小数位
        fimul dword [constant_ten]      ; st(0) *= 10，如 0.456 → 4.56
        fld st0                         ; 复制当前值到 st(1)
        frndint                         ; st(0) = 整数部分，如 4.0
        fistp dword [temp_digit]        ; 保存整数部分到内存，如 4
        fisub dword [temp_digit]        ; 减去整数部分，st(0) = 0.56

        ; 将数字转为 ASCII 并保存到缓冲区
        mov eax, [temp_digit]
        add eax, '0'
        mov [edi], eax
        inc edi

        ; 提前退出条件：小数部分为0
        ftst                                        ; 比较 st0 和 0.0
        fstsw ax                                    ; 把比较结果（C0/C2/C3）存到 ax
        sahf
        loopne fraction_of_float_convert_loop      ; 若 st0 !=0 且 ecx > 0 则继续循环

    ; 计算实际有效位数
    ; 总处理次数 = 6 - ecx
    mov eax, 6
    sub eax, ecx
    mov dword [fraction_part_length], eax


    pop edi
    pop esi
    pop edx
    pop ecx
    pop ebx
    pop eax
    ret


;-------------------------------------
; 函数：调整尾数为十进制科学计数法
; 输入：
;   [result] = 结果
; 输出：
;   [result_decimal_mantissa] = 调整后的尾数（1.0 ≤ mantissa < 10.0）
;   [result_exp_10] = 十进制整数指数
;-------------------------------------
adjust_mantissa:
    pusha
    finit

    ; 初始化
    fld dword [result]  

    ; 初始化十进制指数为0
    mov dword [result_exp_10], 0

    adjust_loop:
        ; 检查 x >= 10.0 ?
        ficom dword [constant_ten]
        fstsw ax
        sahf
        jb mantissa_check_lower

        ; x >=10.0 -> 除以10，指数+1
        fidiv dword [constant_ten]
        inc dword [result_exp_10]
        jmp adjust_loop

    mantissa_check_lower:
        ; 检查 x < 1.0 ?
        fcom dword [constant_one]
        fstsw ax
        sahf
        jae end_adjust_mantissa

        ; x <1.0 -> 乘以10，指数-1
        fimul dword [constant_ten]
        dec dword [result_exp_10]
        jmp adjust_loop

    end_adjust_mantissa:
        ; 保存结果
        fstp dword [result_decimal_mantissa]
        popa
        ret


;-------------------------------------
; 函数：浮点尾数转字符串（格式：x.xxx）
; 输入：
;   [result_mantissa] = 规格化尾数（单精度浮点）
; 输出：
;   mantissa_buffer = 格式化的尾数字符串
;-------------------------------------
convert_mantissa:
    pusha
    finit

    ; 初始化截断模式
    ; 1. 保存原始控制字
    fnstcw [old_cw]         ; 将当前控制字保存到 old_cw

    ; 2. 设置新控制字（向零舍入）
    mov ax, [old_cw]
    and ax, 0xF3FF          ; 清除 RC 字段（第10-11位）
    or ax, 0x0C00           ; 设置 RC=0b11（向零舍入）
    mov [new_cw], ax
    fldcw [new_cw]          ; 加载新控制字到 FPU

    ; 初始化 mantissa_buffer
    mov ecx, 10
    mov edi, mantissa_buffer
    xor eax, eax
    rep stosb

    ; 加载尾数到 FPU 栈
    fld dword [result_decimal_mantissa]      ; st0 = 1.234

    ; 分离整数和小数部分
    fld st0
    frndint                                 ; st0=1.0, st1=1.234
    fsub st1, st0                           ; st1=0.234

    ; 整数部分转字符（1 → '1'）
    fistp dword [temp_int]
    mov eax, [temp_int]
    add al, '0'
    mov [mantissa_buffer], al               ; mantissa_buffer[0] = '1'

    ; 添加小数点
    mov byte [mantissa_buffer + 1], '.'     ; mantissa_buffer[1] = '.'

    ; 处理小数部分（最多3位）
    mov edi, mantissa_buffer + 2            ; 从小数点后开始填充
    mov ecx, 3                              ; 保留3位小数

    convert_mantissa_loop:
        fimul dword [constant_ten]          ; st0 *=10 → 0.234 → 2.34
        fld st0
        frndint
        fistp dword [temp_digit]             ; 提取当前位（例如 2）
        fisub dword [temp_digit]             ; 减去已处理部分（0.34）

        ; 转为ASCII并保存
        mov eax, [temp_digit]
        add al, '0'
        mov [edi], al
        inc edi

        loop convert_mantissa_loop

    ; 结束符
    mov byte [edi], 0
    popa
    ret


;-------------------------------------
; 函数：十进制指数转字符串（格式：+XX 或 -XX）
; 输入：
;   [result_exp_10] = 十进制指数（有符号整数）
; 输出：
;   exp_buffer = 格式化后的指数字符串
;-------------------------------------
convert_exponent:
    pusha
    finit

    ; 初始化 exp_buffer
    mov ecx, 3
    mov edi, exp_buffer
    xor eax, eax
    rep stosb

    mov edi, exp_buffer

    ; 处理符号
    mov eax, [result_exp_10]
    test eax, eax
    jns exp_positive
    neg eax
    mov byte [edi], '-'
    jmp convert_exp_digits

    exp_positive:
        mov byte [edi], '+'

    convert_exp_digits:
        inc edi

        ; 两位数字转换（示例：5 → "05"）
        mov ebx, 10
        xor edx, edx
        div ebx                    ; eax = 商（0）, edx = 余数（5）
        add dl, '0'                ; 十位（补零）
        add al, '0'                ; 个位
        mov [edi], al              ; 高位（补零）
        mov [edi + 1], dl          ; 低位

    ; 结束符
    mov byte [edi + 2], 0
    popa
    ret


;-------------------------------------
; 函数：打印结果
; 参数：
;   [result] = 结果
;   [result_type] = 结果类型
; 返回：
;   无参数
;-------------------------------------
print_result:
    push eax
    push ebx
    push ecx
    push edx
    push esi
    push edi

    ; 打印提示信息
    mov eax, 4
    mov ebx, 1
    mov ecx, result_msg
    mov edx, result_msg_len
    int 0x80

    ; 初始化 result_buffer
    mov ecx, 20
    mov edi, result_buffer
    xor eax, eax
    rep stosb

    mov al, [result_type]

    ; 结果为整数
    cmp al, 0
    je integer_result

    ; 结果为浮点数
    cmp al, 1
    je float_result

    integer_result:
            
        ; 初始化符号位
        mov byte [result_sign], 0

        ; 将 result 复制到 int_part
        mov eax, dword [result]
        mov dword [int_part], eax

        call save_integer

        mov ecx, [int_part_length]
        dec ecx
        mov ebx, 0
        mov esi, int_part_buffer
        mov edi, result_buffer

        integer_result_loop:
            cmp ecx, 0
            jl end_integer_result_loop

            mov al, [esi + ecx]
            mov [edi + ebx], al

            dec ecx
            inc ebx
            jmp integer_result_loop

        end_integer_result_loop:
            ; 增加换行符
            mov byte [edi + ebx], 0xA

        ; 计算长度
        inc ebx
        mov byte [result_length], bl

        xor edx, edx
        ; 输出结果
        mov eax, 4
        mov ebx, 1
        mov ecx, result_buffer
        mov dl, byte [result_length]
        int 0x80

        jmp end_print_result

    float_result:
        finit

        ; 初始化截断模式
        ; 1. 保存原始控制字
        fnstcw [old_cw]         ; 将当前控制字保存到 old_cw

        ; 2. 设置新控制字（向零舍入）
        mov ax, [old_cw]
        and ax, 0xF3FF          ; 清除 RC 字段（第10-11位）
        or ax, 0x0C00           ; 设置 RC=0b11（向零舍入）
        mov [new_cw], ax
        fldcw [new_cw]          ; 加载新控制字到 FPU

        ; 加载浮点数到 FPU 栈
        fld dword [result]

        ; 检查特殊值（NaN/Infinity）
        fld st0                 ; 复制 st(0) 到栈顶，避免破坏原始值
        ftst                    ; 比较 st(0) 与 0，得到各种比较标志
        fstsw ax                ; 将 FPU 状态字（含比较标志 C3,C2,C0）存到 ax
        sahf                    ; 把 ax 的高 8 位传到 CPU 标志寄存器： PF (奇偶标志) 接收 C2，ZF (零标志) 接收 C3
        jz handle_float_zero    ; 处理零值
        jp handle_float_nan_inf ; 处理非数值或无穷大

        ; 正常浮点数处理流程
        ; 提取指数
        fxtract                         ; st(0)=尾数（1.xxx）, st(1)=指数（二进制指数）
        fxch st1                        ; 交换 st(0) 和 st(1): st(0)=指数, st(1)=尾数
        fistp dword [result_exp_2]        ; 保存指数到内存: st(0) = 尾数
        mov eax, [result_exp_2]

        ; 提取尾数
        fstp dword [result_binary_mantissa]

        mov eax, dword [result_exp_2]

        ; 判断是否使用科学计数法：指数绝对值过大或过小
        cmp eax, 17                     ; 十进制指数 >= 5 对应 二进制指数 >= 17
        jge scientific_notation_convert
        cmp eax, -14                    ; 十进制指数 <= -4 对应 二进制指数 <= -14
        jle scientific_notation_convert


        ; 常规小数格式, 如 123.456
        standard_format_convert:
            ; 分离整数和小数部分
            fld st0                     ; st(0) = 复制的结果, st(1) = 原始结果
            frndint                     ; st(0) = 整数部分, st(1) = 原始结果
            fsub st1, st0               ; st(0) = 整数部分, st(1) = 小数部分

            ; 处理数字部分
            fistp dword [int_part]      ; 保存整数部分
            fstp dword [fraction_part]  ; 保存小数部分
            call save_integer
            call save_fraction

            ; 填充 result_buffer 循环
            
            ; esi = int_part_buffer 的末尾指针
            ; ecx = 循环长度
            mov edi, result_buffer
            mov esi, int_part_buffer
            mov ecx, dword [int_part_length]
            add esi, ecx
            dec esi
            standard_format_convert_integer_loop:
                cmp ecx, 0
                jle end_standard_format_convert_integer_loop

                mov al, byte [esi]
                mov byte [edi], al

                dec esi
                inc edi
                dec ecx
                jmp standard_format_convert_integer_loop



            end_standard_format_convert_integer_loop:
                ; 添加小数点
                mov byte [edi], '.'
                inc edi

            ; 处理小数部分
            ; esi = fraction_part_buffer 的初始指针
            ; ecx = 循环长度
            mov esi, fraction_part_buffer
            mov ecx, dword [fraction_part_length]
            standard_format_convert_fraction_loop:
                cmp ecx, 0
                jle end_standard_format_convert_fraction_loop

                mov al, byte [esi]
                mov byte [edi], al

                inc esi
                inc edi
                dec ecx
                jmp standard_format_convert_fraction_loop

            end_standard_format_convert_fraction_loop:
                ; 添加换行符
                mov byte [edi], 0xA
                inc edi

                ; 计算字符串长度
                mov eax, result_buffer
                mov edx, edi
                sub edx, eax
                mov byte [result_length], dl

                ; 输出结果
                mov eax, 4
                mov ebx, 1
                mov ecx, result_buffer
                int 0x80

                jmp end_print_result


        ; 科学计数法格式, 如 1.234e+5
        scientific_notation_convert:
            call adjust_mantissa

            ; 1. 转换尾数和指数
            call convert_mantissa
            call convert_exponent

            ; 2. 组合各部分到 sci_buffer
            mov esi, mantissa_buffer       ; 源：尾数字符串
            mov edi, result_buffer         ; 目标：最终缓冲区

            ; 复制尾数
            copy_mantissa:
                lodsb                       ; 加载字符到 al
                test al, al
                jz add_e
                stosb                       ; 存入 sci_buffer
                jmp copy_mantissa

            add_e:
                mov al, 'e'                 ; 添加 'e'
                stosb

            ; 复制指数
            mov esi, exp_buffer             ; 源：指数字符串
            copy_exp:
                lodsb
                test al, al
                jz end_scientific_notation_convert
                stosb
                jmp copy_exp

            end_scientific_notation_convert:
                mov byte [edi], 0xA         ; 换行符
                inc edi

                ; 计算字符串长度
                mov eax, result_buffer
                mov edx, edi
                sub edx, eax
                mov byte [result_length], dl

                ; 输出结果
                mov eax, 4
                mov ebx, 1
                mov ecx, result_buffer
                int 0x80

                jmp end_print_result


        handle_float_zero:
            mov eax, 4
            mov ebx, 1
            mov ecx, float_zero
            mov edx, float_zero_len
            int 0x80
            
            jmp end_print_result

        handle_float_nan_inf:
            mov eax, 4
            mov ebx, 1
            mov ecx, float_nan
            mov edx, float_nan_len
            int 0x80

            jmp end_print_result


    end_print_result:
        pop edi
        pop esi
        pop edx
        pop ecx
        pop ebx
        pop eax
        ret


; ----------------------------------- 主函数调用函数 ----------------------------------- ;
;-------------------------------------
; 函数：输入命令
; 参数：
;   ecx = 缓冲区地址
;   edx = 缓冲区最大容量为 2
; 返回：
;   eax = 实际读取的字符数（不含换行符）
;   [command] = 实际命令
;-------------------------------------
read_command:
    push ebx
    push ecx
    push edx

    ; 清空缓冲区（填充 0）
    cld                     ; 确保 DF=0（指针递增）
    mov edi, command_buffer ; edi 指向缓冲区起始地址
    mov ecx, 2              ; 重复次数 = 缓冲区大小
    mov al, 0               ; 要填充的值（0）
    rep stosb               ; 重复执行：将 0 写入缓冲区

    ; 读取输入（sys_read）
    mov eax, 3              ; sys_read
    mov ebx, 0              ; stdin
    mov ecx, command_buffer ; 传入缓冲区地址至 ecx
    mov edx, 2              ; 传入缓冲区最大大小
    int 0x80

    ; 保存实际读取的命令
    movzx ebx, byte [command_buffer]
    sub ebx, '0'            ; 将字符转换为数字
    mov byte [command], bl

    ; 将换行符（0xA）替换为 null 终止符（0）
    mov esi, ecx            ; 缓冲区地址
    add esi, eax            ; 移动到输入末尾
    dec esi                 ; 最后一个字符的位置
    cmp byte [esi], 0xA     ; 检查是否是换行符
    jne _no_command_newline
    mov byte [esi], 0       ; 替换为 null
    dec eax                 ; 排除换行符

    _no_command_newline:
        pop edx
        pop ecx
        pop ebx
        ret


;-------------------------------------
; 函数：退出程序命令
; 参数：
;   无参数
; 返回：
;   无参数
;-------------------------------------
exit:
    pusha           ; 保存所有通用寄存器到栈
    pushfd          ; 保存标志寄存器

    ; 退出程序
    mov eax, 1
    xor ebx, ebx
    int 0x80

    popfd           ; 恢复标志寄存器
    popa            ; 恢复所有通用寄存器
    ret


; main 函数入口
_start:
    menu:
        call print_menu
        call read_command

        ; switch([command])
        cmp byte [command], 1
        je calculate
        cmp byte [command], 3
        je exit_program

        ; 默认处理：未知命令
        mov eax, 0          ; 错误码 0
        call error_handler   ; 调用错误处理函数

        ; end_switch 语句
        end_switch:
            jmp menu
    
    calculate:
        ; 显示输入提示
        mov eax, 4              ; sys_write
        mov ebx, 1              ; stdout
        mov ecx, calculate_msg
        mov edx, calculate_msg_len
        int 0x80
    
        call read_expression_string
        call evaluate_expression

        mov al, [result_type]
        cmp al, 0
        jne wrong_result_type

        mov eax, dword [result]
        cmp eax, 8888
        je valid

        ; 不等：输出提示并回菜单
        mov eax, 4
        mov ebx, 1
        mov ecx, wrong_msg
        mov edx, wrong_msg_len
        int 0x80
        jmp finally
        
    wrong_result_type:
        mov eax, 4
        mov ebx, 1
        mov ecx, wrong_type_msg
        mov edx, wrong_type_msg_len
        int 0x80
        jmp finally

    valid:
        mov eax, 4
        mov ebx, 1
        mov ecx, success_msg
        mov edx, success_msg_len
        int 0x80

    finally:
        call print_result

        ; calculate 过程结束
        jmp end_switch

    exit_program:
        ; 退出程序

        call exit

;answer:112*121-22*212,由于乘法的交换律，一共有4个解

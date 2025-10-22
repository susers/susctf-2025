#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/mman.h>
#include <ctype.h>

#define MAX_SHELLCODE_SIZE 4096

int is_printable_shellcode(const char *shellcode, size_t len) {
    for (size_t i = 0; i < len; ++i) {
        if (!isprint((unsigned char)shellcode[i])) {
            return 0;
        }
    }
    return 1;
}

void execute_shellcode(char *shellcode, size_t len) {
    // 对齐到页面大小
    size_t page_size = getpagesize();
    void *aligned_address = (void *)((long)shellcode & ~(page_size - 1));

    // 修改内存权限为可执行
    if (mprotect(aligned_address, page_size, PROT_READ | PROT_WRITE | PROT_EXEC) == -1) {
        perror("mprotect");
        exit(EXIT_FAILURE);
    }

    // 类型转换为函数指针并调用
    void (*func)();
    func = (void (*)())shellcode;
    printf("[*] running...\n");
    func();
}

int main() {
    char shellcode[MAX_SHELLCODE_SIZE];
    ssize_t len;

    // 提示用户输入 shellcode
    puts("enter magic code: ");

    // 使用 read 读取输入
    len = read(STDIN_FILENO, shellcode, sizeof(shellcode) - 1);
    if (len <= 0) {
        puts("err");
        return 1;
    }

    shellcode[len] = '\0'; // 添加字符串终止符

    // 检查是否全为可打印字符
    if (is_printable_shellcode(shellcode, len)) {
        execute_shellcode(shellcode, len);
    } else {
        puts("[-] error!!!!\n");
    }

    return 0;
}


//gcc -s -fno-stack-protector -z execstack -o shellcd shellcd.c

#include <stdio.h>
#include <string.h>
#include <unistd.h>


#define MAX_LEN 100
void init(){
    fflush(stdin);
    setvbuf(stdout, 0, 2, 0);
    fflush(stderr);
    setvbuf(stderr, 0, 2, 0);
}
int main() {
    init();
    char username[MAX_LEN];
    char password[MAX_LEN];

    // 预设的正确账号密码
    const char correct_username[] = "admin";
    const char correct_password[] = "sus1SG0od";

    puts("username: ");
    read(STDIN_FILENO, username, 0x100);


    printf("password: ");
    read(STDIN_FILENO, password, 0x100);

    // 比较输入的用户名和密码是否与预设一致
    if (strcmp(username, correct_username) == 0 && strcmp(password, correct_password) == 0) {
        puts("success!");
    } else {
        puts("wrong username or password!");
    }

    return 0;
}

//gcc -s login.c -o login -fno-stack-protector -no-pie -Wl,-z,relro
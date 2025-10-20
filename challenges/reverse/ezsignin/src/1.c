#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>

typedef struct {
    unsigned char S[256];
    int i, j;
} rc4_ctx;

static const char map[] = {'E', '1', '1', '1', '0', '0',
    '0', '0', '0', '1', '0', '0',
    '0', '0', '0', '1', '0', '0',
    '0', '1', '1', '1', '0', '0',
    '0', '1', '0', '0', '0', '0',
    '0', '1', '1', '1', '1', 'O'};
    
static const char base64_chars[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";

static const char base58_chars[] = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz";

static const unsigned char key[] = "YourKey";

static const uint8_t encryption[] = {0x32, 0x77, 0x48, 0x46, 0x77, 0x36, 0x58, 0x52, 0x51, 0x46, 0x4a, 0x65, 0x78, 0x77, 0x59, 0x63, 0x69, 0x7a, 0x57, 0x46, 0x4a, 0x56, 0x55, 0x38, 0x37, 0x47, 0x6e, 0x50, 0x50, 0x62, 0x75, 0x52, 0x5a, 0x46, 0x39, 0x39, 0x74, 0x38, 0x38, 0x38, 0x34, 0x53, 0x78, 0x54, 0x65, 0x52, 0x70, 0x74, 0x67, 0x76, 0x41, 0x6d, 0x66, 0x7a, 0x64, 0x71, 0x6d, 0x45, 0x39, 0x73, 0x6b, 0x43, 0x53, 0x52, 0x62, 0x45, 0x4d, 0x55, 0x63, 0x38, 0x72, 0x35, 0x57, 0x63, 0x47, 0x51, 0x34, 0x61, 0x71, 0x38, 0x67, 0x4a, 0x51, 0x32, 0x66, 0x70, 0x55, 0x51, 0x67, 0x69, 0x69, 0x4e, 0x76, 0x6b, 0x45, 0x51, 0x58, 0x4c, 0x34, 0x47, 0x6f, 0x51, 0x35, 0x72, 0x42, 0x5a, 0x66, 0x65, 0x6a, 0x59, 0x46, 0x74, 0x45, 0x70, 0x54, 0x41, 0x35, 0x78, 0x31, 0x6b, 0x79, 0x62, 0x74, 0x65, 0x6e, 0x65, 0x41, 0x75, 0x45, 0x43, 0x71, 0x70, 0x33, 0x75, 0x4c, 0x43, 0x44, 0x6e, 0x75, 0x55, 0x34, 0x47, 0x77, 0x44, 0x31, 0x6b, 0x4b, 0x65, 0x74, 0x38, 0x42, 0x6d, 0x71, 0x62, 0x34, 0x65, 0x69, 0x64, 0x50, 0x57, 0x45, 0x63, 0x72, 0x36, 0x62, 0x53, 0x4e, 0x4e, 0x55, 0x33, 0x77, 0x72, 0x35, 0x78, 0x78, 0x74, 0x48, 0x70, 0x63, 0x34, 0x33, 0x54, 0x79, 0x48, 0x4d, 0x53, 0x4b, 0x67, 0x67, 0x42, 0x52, 0x5a, 0x72};

void init(rc4_ctx *ctx, const unsigned char key[]){
    int length = strlen(key);
    __asm__ __volatile__ (
        ".byte 0x75, 0x02, 0xE9, 0xED"
    );
    for(int i = 0; i < 256; i ++){
        ctx->S[i] = i;
    }

    int j = 0;
    for(int i = 0; i < 256; i ++){
        j = (j + ctx->S[i] + key[i % length]) % 256;
        unsigned char temp = ctx->S[i];
        ctx->S[i] = ctx->S[j];
        ctx->S[j] = temp;
    }

    ctx->i = 0;
    ctx->j = 0;
}

int get_length(uint8_t target[]){
    int length = 0;
    while(target[length] != 0xff){
        length ++;
    }
    return length;
}

void crypt(rc4_ctx *ctx, uint8_t flag[]){
    int length = get_length(flag);
    int i = ctx->i;
    int j = ctx->j;
    __asm__ __volatile__ (
        ".byte 0x75, 0x02, 0xE9, 0xED"
    );
    for(int k = 0; k < length; k ++){
        i = (i + 1) % 256;
        j = (j + ctx->S[i]) % 256;
        unsigned char temp = ctx->S[i];
        ctx->S[i] = ctx->S[j];
        ctx->S[j] = temp;
        int t = (ctx->S[i] + ctx->S[j]) % 256;
        flag[k] = flag[k] ^ ctx->S[t];
    }

    ctx->i = i;
    ctx->j = j;
}

void encrypt1(uint8_t flag[]) {
    int length = get_length(flag);
    int key = 0x66;
    for(int i = 0; i < length; i ++){
        flag[i] = flag[i] ^ key;
    }
}

void encrypt2(uint8_t flag[]) {
    int length = get_length(flag);
    uint8_t *temp = (uint8_t *)malloc(length);
    memcpy(temp, flag, length);
    temp[length] = 0xff;
    int zeros = 0;
    __asm__ __volatile__ (
        ".byte 0x75, 0x02, 0xE9, 0xED"
    );
    while(zeros < length && temp[zeros] == 0){
        zeros ++;
    }

    int size = length * 138 / 100 + 1;
    uint8_t * buffer = (uint8_t *)calloc(size, sizeof(flag[0]));
    for(int i = 0; i < length; i ++){
        unsigned int carry = temp[i];
        for(int j = size - 1; j >= 0; j --){
            carry += 256 * buffer[j];
            buffer[j] = carry % 58;
            carry /= 58;
        }
    }

    int first_digit = 0;
    while(first_digit < size && buffer[first_digit] == 0){
        first_digit ++;
    }

    int out_cursor = 0;
    for(int i = 0; i < zeros; i ++){
        flag[out_cursor ++] = base58_chars[0];
    }
    for(int i = first_digit; i < size; i ++){
        flag[out_cursor ++] = base58_chars[buffer[i]];
    }

    flag[out_cursor] = 0xff;
    free(temp);
    free(buffer);
}

void encrypt3(uint8_t flag[], const unsigned char key[]) {
    rc4_ctx ctx;
    init(&ctx, key);
    crypt(&ctx, flag);
}

void encrypt4(uint8_t flag[]) {
    srand(time(NULL));
    int length = get_length(flag);
    for(int i = 0; i < length; i ++){
        int key = rand();
        flag[i] = flag[i] ^ key;
    }
}

int main() {
    char steps[50];
    char flag[300];
    uint8_t int_flag[300];
    printf("Please enter the steps: ");
    scanf("%s", &steps);
    int i = 0;
    int position = 0;
    while(steps[i] != '\0') {
        switch(steps[i]) {
            case '1':
                if((position + 1) % 6 == 0 || map[position + 1] == '0') {
                    printf("No Way!!!");
                    return 0;
                }
                position = position + 1;
                break;
            case '2':
                if((position / 6) + 1 == 6 || map[position + 6] == '0') {
                    printf("No Way!!!");
                    return 0;
                }
                position = position + 6;
                break;
            case '3':
                if((position - 1) % 6 == 5 || map[position - 1] == '0') {
                    printf("No Way!!!");
                    return 0;
                }
                position = position - 1; 
                break;
            case '4':
                if((position / 6) - 1 == -1 || map[position - 6] == '0') {
                    printf("No Way!!!");
                    return 0;
                }
                position = position - 6;
                break;
            default:
                printf("No Way!!!");
                return 0;
        }
        i ++;
    }
    if(map[position] == 'O') {
        printf("You Win The Game!!!\n");
    }else{
        printf("You Lose!!!");
        return 0;
    }
    printf("Please enter the flag: ");
    scanf("%s", &flag);
    for(int k = 0; ; k ++){
        int_flag[k] = (uint8_t)flag[k];
        if(flag[k] == '\0'){
            int_flag[k] = 0xff;
            break;
        }
    }
    int j = 0;
    __asm__ __volatile__ (
        ".byte 0x75, 0x02, 0xE9, 0xED"
    );
    while(steps[j] != '\0') {
        switch(steps[j]) {
            case '1':
                encrypt1(int_flag);
                break;
            case '2':
                encrypt2(int_flag);
                break;
            case '3':
                encrypt3(int_flag, key);
                break;
            case '4':
                encrypt4(int_flag);
                break;
        }
        j ++;
    }
    int size = sizeof(encryption);
    if(!memcmp(int_flag, encryption, size)){
        printf("You are Right!!!");
    }else{
        printf("Your are Wrong!!!");
    }

    return 0;
}

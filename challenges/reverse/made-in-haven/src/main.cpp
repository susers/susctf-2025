#include <cstdio>
#include <Windows.h>
#include <winternl.h>
#include <cstdint>

#define IsBeingDebugged (((PPEB)__readgsqword(0x60))->BeingDebugged) // 调试器检测
#define Delta 0xdeadbeef
#define FlagLen 32

// 全局变量区域
unsigned char key[] = { 0x65, 0x6c, 0x67, 0x76, 0x64, 0x69, 0x73, 0x6c, 0x68, 0x61, 0x70, 0x79, 0x62, 0x73, 0x79, 0x22, 0x0 };
unsigned char xor_delta[] = { 1, 9, 2, 6, 0, 8, 1, 7 };
unsigned char add_delta[] = { 2, 0, 2, 5, 1, 0, 0, 1 };
unsigned char flag[] = { 0x6f, 0x47, 0xa, 0x56, 0xd1, 0x3a, 0xbc, 0xf8, 0xe3, 0x93, 0xc2, 0xa6, 0x11, 0x8f, 0xb, 0x6f, 0xf7, 0x7d, 0xa5, 0x81, 0x57, 0x32, 0xb3, 0xf5, 0x61, 0x85, 0x70, 0xa0, 0xe1, 0x93, 0x39, 0xec, 0 };
unsigned char success_msg[] = { 0x70, 0x64, 0x67, 0x68, 0x23, 0x6c, 0x71, 0x23, 0x6b, 0x64, 0x79, 0x68, 0x71, 0x24, 0 };
unsigned char failed_msg[] = { 0x6d, 0x6e, 0x1f, 0x6d, 0x6e, 0x20, 0 };

void my_xor_eq(unsigned char* num1, unsigned char num2) {
	*num1 ^= num2;
}

void my_sub_eq(unsigned char* num1, unsigned char num2) {
	*num1 -= (num2);
}

void tea(uint32_t* v, const uint32_t* k) {
	unsigned int sum = 0;
	uint32_t v0 = v[0];
	uint32_t v1 = v[1];
	for (int i = 0;i < 32;i++) {
		sum += Delta;
		v0 += ((v1 << 4) + k[0]) ^ (v1 + sum) ^ ((v1 >> 5) + k[1]);
		v1 += ((v0 << 4) + k[2]) ^ (v0 + sum) ^ ((v0 >> 5) + k[3]);
	}
	v[0] = v0, v[1] = v1;
}

int main() {
	printf("input your flag: ");
	unsigned char input_flag[33];
	scanf_s("%32s", input_flag, (unsigned)sizeof(input_flag));

	// 还原 key
	for (int i = 0; i < 8; i++) {
		unsigned char* k = &key[i];
		unsigned char d = xor_delta[i];
		my_xor_eq(k, d);
	}
	for (int i = 0; i < 8; i++) {
		unsigned char* k = &key[i + 8];
		unsigned char d = add_delta[i];
		my_sub_eq(k, d);
	}

	// TEA
	for (int i = 0; i < FlagLen / 4; i += 2) {
		uint32_t* f = (uint32_t*)input_flag + i;
		uint32_t* k = (uint32_t*)key;
		tea(f, k);
	}

	bool res = true;
	for (int i = 0; i < FlagLen; i++) {
		res = (flag[i] == input_flag[i]);
	}
	if (res) {
		for (int i = 0; i < 14; i++) {
			success_msg[i] -= 3;
		}
		puts((char *)success_msg);
	}
	else {
		for (int i = 0; i < 6; i++) {
			failed_msg[i] += 1;
		}
		puts((char *)failed_msg);
	}

	return 0;
}
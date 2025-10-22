#include <stdio.h>
#include <string.h>

void transform(char *input, int len) {
  for (int i = 0; i < len; i++) {
    input[i] ^= (i * 7 + 13) & 0xFF;
  }
}

#define LEN 24
int check_password(const char *input) {
  char transformed[LEN + 1];
  const char secret[] = {0x7e, 0x61, 0x68, 0x41, 0x5d, 0x56, 0x4c, 0x7d,
                         0x73, 0x29, 0x30, 0x31, 0x52, 0x1a, 0x30, 0x24,
                         0x18, 0xf2, 0xee, 0xe0, 0xea, 0x93, 0xc3, 0xd3};

  if (strlen(input) != LEN) {
    return 0;
  }

  strncpy(transformed, input, LEN);
  transformed[LEN] = '\0';

  transform(transformed, LEN);

  if (memcmp(transformed, secret, LEN) == 0) {
    return 1;
  }
  return 0;
}

int main() {
  char input[LEN + 1];
  printf("Enter the flag: ");
  fgets(input, sizeof(input), stdin);

  // strip newline
  input[strcspn(input, "\n")] = 0;

  if (check_password(input)) {
    puts("Access granted!");
  } else {
    puts("Access denied!");
  }
  return 0;
}

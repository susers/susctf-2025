#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LEN 100
char buf[MAX_LEN];

void init() {
  fflush(stdin);
  setvbuf(stdout, 0, 2, 0);
  fflush(stderr);
  setvbuf(stderr, 0, 2, 0);
}

int main() {
  init();

  printf("Welcome to pwn signin!\n");

  while (1) {
    printf("Enter command: ");
    if (!fgets(buf, sizeof(buf), stdin))
      break;

    if (strncmp(buf, "exit", 4) == 0) {
      printf("Bye!\n");
      break;
    }

    if (strncmp(buf, "shell", 5) == 0) {
      printf("Spawning bash shell...\n");
      system("/bin/bash");
      continue;
    }

    printf("You sent: %s", buf);
  }

  return 0;
}

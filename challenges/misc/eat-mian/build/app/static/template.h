#include <stdio.h>
#include <stdlib.h>
#include <time.h>

{{ code }}

int main(int argc, char **argv) {
  srand(time(NULL));
  int n = rand();
  printf("I int %d cups of main! wwwww\n", n);
  return 0;
}

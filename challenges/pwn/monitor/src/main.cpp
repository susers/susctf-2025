#include "layer.h"

int main();

void _start(void) {
    __asm__(
        "push rax"  // for stack alignment
    );
    main();
    __asm__ (
        "mov rax, 0xe7\n"   // exit_group
        "xor rdi, rdi\n"    // status 0
        "syscall"
    );
}

int waf(char *buf, int len)
{
    if (
        _memmem(buf, len, "./", 2) ||
        _memmem(buf, len, "../", 3) ||
        _memmem(buf, len, "..", 2) ||
        buf[0] == '/')
        return 1;
    return 0;
}

int check(char * buf, int len) {
    if (_memmem(buf, len, "susctf", 6)) {
        return 1;
    }
    return 0;
}

long nbytes;
long fd;
int choice;

#define name (fb.filename + 2)

void process()
{
    struct {
        char buf[PAGESIZE];
        char filename[128];
    } fb;
    char buf[PAGESIZE];

    while (1)
    { 
        // leak pie and stack
        _write(1, "What file you want open?\n", 25);
        nbytes = _read(0, name, 128 - 2 + 9); // for rbp abuse

        if(nbytes <= 0) {
            continue;
        }

        if (name[nbytes - 1] == '\n')
        {
            name[nbytes - 1] = '\0';
        }

        if (waf(name, nbytes))
        {
            _write(1, "Path contain illegal pattern\n", 29);
            continue;
        }

        if (name[0] == '\0') {
            continue;
        }

        if (_memmem(name, 8, "exit.run", 8))
        {
            return;
        }
        fb.filename[0] = '.';
        fb.filename[1] = '/';

        _write(1, "OK, I will show you something in this file.\n", 44);
        fd = _open(fb.filename, 0, 0);
        if (fd < 0)
        {
            _write(1, "Open file wrong.\n", 17);
            continue;
        }
        nbytes = _read(fd, buf, PAGESIZE);
        if (nbytes < 0) {
            _write(1, "Read file wrong.\n", 17);
            continue;
        }
        if(check(buf, nbytes)) {
            _write(1, "Are you sure? See the SECRET will broken the system! (y/n)\n", 58);
            if(_read(0, (char *)&choice, 2) < 0 || (choice & 0xff) == 'n') {
                goto end;
            }
        }
        _write(1, buf, nbytes); 
end:
        _close(fd);
    }
}

void hello()
{
    _write(1, "Hello, Welcome to my file contain browser! Give the file name, "
              "I wiil show the secret for you!\n",
           95);
    _write(1, "But... It won't give you the most valuable FLAG.\n"
              "No one can steal the FLAG...\n"
              "No one....\n",
           89);
}

int main()
{
    hello();
    process();
}


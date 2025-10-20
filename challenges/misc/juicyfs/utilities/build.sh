python3 gen.py 'susctf{yOu_Ar3_ju1cef$_mAs7er!!1}' 5 32768

# macos
# clang -O2 main_macos.c -o chall -Wl,-sectcreate,__DATA,__blob,blob.bin
# ./chall

# linux
objcopy -I binary -O elf64-x86-64 -B i386:x86-64 blob.bin blob.o
gcc -O2 --static -s main.c blob.o -o chall
./chall
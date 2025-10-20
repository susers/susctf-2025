

build:
	g++ -o liblayer.so -z relro -z now -L. -Wl,-rpath,. -fPIC -shared -fstack-protector-strong layer.cpp -lcrypto -lseccomp -lm
	g++ -o monitor -z relro -z now -L. -Wl,-rpath,. -masm=intel -nostdlib -fno-stack-protector main.cpp -llayer
	strip liblayer.so

debug:
	g++ -o liblayer.so -z relro -z now -g -L. -Wl,-rpath,. -fPIC -masm=intel -shared -fstack-protector-strong layer.cpp -lcrypto -lseccomp -lm
	g++ -o monitor -z relro -z now -g -L. -Wl,-rpath,. -masm=intel -nostdlib -fno-stack-protector main.cpp -llayer

clean:
	rm -f monitor liblayer.so

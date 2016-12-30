all: index

clean:
	rm -rf build

mkdir:
	mkdir -p build

index: mkdir build/index.html

build/index.html:
	bin/index.py

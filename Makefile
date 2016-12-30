all: build

clean:
	rm -rf build

build: index

pip:
	pip3 install -r requirements.txt

mkdir:
	mkdir -p build

index: mkdir build/index.html

build/index.html:
	bin/index.py

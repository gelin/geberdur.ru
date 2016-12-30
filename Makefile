RSYNC_HOST=141.8.195.84
RSYNC_PATH=domains/geberdur.ru/public_html

all: build

clean:
	rm -rf build

build: index static

deploy:
	rsync -rlptvz build/ $(RSYNC_HOST):$(RSYNC_PATH)/

pip:
	pip3 install -r requirements.txt

mkdir:
	mkdir -p build


index: mkdir build/index.html

build/index.html:
	bin/index.py


static: build/favicon.ico

build/favicon.ico:
	cp -rv src/static/* build/



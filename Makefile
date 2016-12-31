RSYNC_USER?=gelin
RSYNC_HOST?=141.8.195.84
RSYNC_REMOTE_PATH?=domains/geberdur.ru/public_html


all: build

clean:
	rm -rf build/*

build: index static

deploy:
	rsync -rlptvz build/ $(RSYNC_USER)@$(RSYNC_HOST):$(RSYNC_REMOTE_PATH)/

pip:
	pip3 install -r requirements.txt

mkdir:
	mkdir -p build


index: mkdir build/index.html

build/index.html:
	./bin/index.py


static: build/favicon.ico

build/favicon.ico:
	cp -av src/static/* build/


docker-build:
	docker build -f src/docker/Dockerfile -t gelin/geberdur.ru-pipeline .

docker-push:
	docker push gelin/geberdur.ru-pipeline

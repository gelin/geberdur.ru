RSYNC_USER?=gelin
RSYNC_HOST?=141.8.195.84
RSYNC_REMOTE_PATH?=domains/geberdur.ru/public_html


all: build

clean:
	rm -rf build/*

build: static tales index

deploy:
	rsync -rlptvz build/ $(RSYNC_USER)@$(RSYNC_HOST):$(RSYNC_REMOTE_PATH)/

pip:
	pip3 install -r requirements.txt

mkdirs:
	mkdir -p build/tale


index: mkdirs build/index.html

build/index.html:
	./bin/index.py


tales: mkdirs build/tale/*

build/tale/%: src/tales/%.md
	./bin/tale.py $<


static: mkdirs build/*.ico

build/*.ico:
	cp -av src/static/* build/


docker-build:
	docker build -f src/docker/Dockerfile -t gelin/geberdur.ru-pipeline .

docker-push:
	docker push gelin/geberdur.ru-pipeline

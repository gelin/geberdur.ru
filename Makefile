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

mkdirs: build/tale

build/tale:
	mkdir -p build/tale


index: mkdirs build/index.html

build/index.html: src/templates/index.pug src/tales/*.md
	./bin/index.py


tales: mkdirs build/tale/*/index.html

build/tale/%/index.html: src/templates/tale.pug src/tales/*-%.md
	./bin/tales.py $^


static: mkdirs build/*.ico

build/%: src/static/%
	@echo Copying static resources
	cp -a src/static/* build/


docker-build:
	docker build -f src/docker/Dockerfile -t gelin/geberdur.ru-pipeline .

docker-push:
	docker push gelin/geberdur.ru-pipeline

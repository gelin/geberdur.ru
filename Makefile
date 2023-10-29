RSYNC_USER ?= root
RSYNC_HOST ?= ftp.geberdur.ru
RSYNC_REMOTE_PATH ?= /srv/www/geberdur.ru
WWW_USER ?= www-data

export SHELL = /usr/bin/zsh

.PHONY: all
all: build

.PHONY: clean
clean:
	rm -rf build/*

.PHONY: build
build: static tales index feed 404

.PHONY: deploy
deploy:
	rsync -rlptvz --chown=$(WWW_USER):$(WWW_USER) build/ $(RSYNC_USER)@$(RSYNC_HOST):$(RSYNC_REMOTE_PATH)/

.PHONY: init
init:
	pyenv install -s 3.8.18
	pyenv virtualenv 3.8.18 geberdur || true
	pyenv local geberdur
	pyenv activate geberdur	

.PHONY: install
install:
	pip install -r requirements.txt

.PHONY: mkdirs
mkdirs: build/tale

build/tale:
	mkdir -p build/tale


.PHONY: index
index: mkdirs build/index.html

build/index.html: src/templates/layout.pug src/templates/index.pug src/tales/*.md
	python ./bin/index.py


.PHONY: tales
tales: mkdirs build/tale/*/index.html

build/tale/%/index.html: src/templates/layout.pug src/templates/tale.pug src/tales/*-%.md
	python ./bin/tales.py $^


.PHONY: static
static: mkdirs build/*.ico build/*.png build/*.json build/js/* build/css/* build/.htaccess

build/%: src/static/%
	@echo Copying static resources
	cp -a src/static/* build/

build/.htaccess: src/static/.htaccess
	cp -a src/static/.htaccess build/


.PHONY: feed
feed: mkdirs build/feed.xml

build/feed.xml: src/templates/rss.pug src/tales/*.md
	python ./bin/feed.py


.PHONY: 404
404: mkdirs build/404.html

build/404.html: src/templates/404.pug src/templates/layout.pug
	python ./bin/404.py


.PHONY: docker-build
docker-build:
	docker build -f docker/Dockerfile -t gelin/geberdur.ru-pipeline .

.PHONY: docker-push
docker-push:
	docker push gelin/geberdur.ru-pipeline

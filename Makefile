RSYNC_USER?=gelin
RSYNC_HOST?=141.8.195.84
RSYNC_REMOTE_PATH?=domains/geberdur.ru/public_html


all: build

clean:
	rm -rf build/*

build: static tales index feed 404

deploy:
	rsync -rlptvz build/ $(RSYNC_USER)@$(RSYNC_HOST):$(RSYNC_REMOTE_PATH)/

pip:
	pip3 install -r requirements.txt

mkdirs: build/tale

build/tale:
	mkdir -p build/tale


index: mkdirs build/index.html

build/index.html: src/templates/layout.pug src/templates/index.pug src/tales/*.md
	./bin/index.py


tales: mkdirs build/tale/*/index.html

build/tale/%/index.html: src/templates/layout.pug src/templates/tale.pug src/tales/*-%.md
	./bin/tales.py $^


static: mkdirs build/*.ico build/*.png build/*.json build/js/* build/css/* build/.htaccess

build/%: src/static/%
	@echo Copying static resources
	cp -a src/static/* build/

build/.htaccess: src/static/.htaccess
	cp -a src/static/.htaccess build/

feed: mkdirs build/feed.xml

build/feed.xml: src/templates/rss.pug src/tales/*.md
	./bin/feed.py


404: mkdirs build/404.html

build/404.html: src/templates/404.pug src/templates/layout.pug
	./bin/404.py


docker-build:
	docker build -f docker/Dockerfile -t gelin/geberdur.ru-pipeline .

docker-push:
	docker push gelin/geberdur.ru-pipeline

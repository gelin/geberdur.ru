#!/usr/bin/env sh

if [ ! -f ~/opt/LanguageTool/languagetool-commandline.jar ]
then
    echo Download LanguageTool: https://www.languagetool.org/
    echo And unpack it to ~/opt/LanguageTool/
    exit 1
fi

for t in $(dirname $0)/../src/tales/*-*.md
do
    echo $(basename "$t")
    java -jar ~/opt/LanguageTool/languagetool-commandline.jar -c UTF-8 -l ru "$t" \
        > "${t}_lang-check.txt"
done

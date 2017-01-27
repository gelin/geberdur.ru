#!/usr/bin/env bash

if [ ! -f ~/opt/LanguageTool/languagetool-commandline.jar ]
then
    echo Download LanguageTool: https://www.languagetool.org/
    echo And unpack it to ~/opt/LanguageTool/
    exit 1
fi

TOOL_SPELLING=~/opt/LanguageTool/org/languagetool/resource/ru/hunspell/spelling.txt
THIS_SPELLING=$(dirname $0)/../src/tales/spelling.txt

echo Adding to hunspell...
for line in $(diff --new-line-format="" --unchanged-line-format="" <(sort "$THIS_SPELLING") <(sort "$TOOL_SPELLING"))
do
    echo $line
    echo $line >> "$TOOL_SPELLING"
done

checkfile() {
    file="$1"
    echo $(basename "$file")
    java -jar ~/opt/LanguageTool/languagetool-commandline.jar -c UTF-8 -l ru "$file" \
    > "${file}_lang-check.txt"
}

if [ -n "$1" ]
then
    checkfile "$1"
    exit
fi

for t in $(dirname $0)/../src/tales/*-*.md
do
    checkfile "$t"
done

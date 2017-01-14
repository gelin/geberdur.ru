#!/usr/bin/env python3
"""
Converts tales from FB2 file to MD files.
"""

import sys
import io
import codecs
import re
from xml.dom import pulldom
from libtypograf import typograf


def parse_tales(fb2file):
    doc = pulldom.parse(fb2file)
    text = None
    in_section = False
    in_paragraph = False
    for event, node in doc:
        if event == pulldom.START_ELEMENT and node.tagName == 'section':
            text = io.StringIO()
            in_section = True
        elif in_paragraph:
            if event == pulldom.END_ELEMENT and node.tagName == 'p':
                in_paragraph = False
                text.write('\n\n')
            elif event == pulldom.CHARACTERS:
                text.write(node.data)
            elif event == pulldom.START_ELEMENT:
                text.write('<%s>' % node.tagName)
            elif event == pulldom.END_ELEMENT:
                text.write('</%s>' % node.tagName)
        elif in_section:
            if event == pulldom.END_ELEMENT and node.tagName == 'section':
                in_section = False
                yield text.getvalue()
                text.close()
            elif event == pulldom.START_ELEMENT and node.tagName == 'title':
                doc.expandNode(node)
                title = node.firstChild.data.strip()
                title = re.sub(r'(?<!\.)\.$', '', title)    # removes ending dot, but not ellipsis
                text.write('# ')
                text.write(title)
                text.write('\n\n')
            elif event == pulldom.START_ELEMENT and node.tagName == 'p':
                in_paragraph = True


def main(fb2file):
    i = 1
    for tale in parse_tales(fb2file):
        if i == 165:
            i += 1
        file = 'src/tales/{0:04d}-{0:d}.md'.format(i)
        print('Writing', file)
        tale = typograf(tale)
        with codecs.open(file, mode='w', encoding='utf-8') as mdfile:
            mdfile.write(tale)
        i += 1


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: fromfb2 tales.fb2')
        exit(1)
    main(sys.argv[1])

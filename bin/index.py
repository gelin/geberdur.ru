#!/usr/bin/env python3
"""
Renders index.html
"""


import os
import os.path
import codecs
from mako.lookup import TemplateLookup
from pypugjs.ext.mako import preprocessor as pug_preprocessor
import hoep


class HeaderCatcher(hoep.Hoep):

    def __init__(self, extensions=0, render_flags=0):
        super(HeaderCatcher, self).__init__(extensions, render_flags)
        self.first_head = None

    def header(self, text, level):
        if self.first_head is None and level == 1:
            self.first_head = text
        return ''


def list_tales():
    for mdfile in filter(lambda f: f.endswith('.md'),
                    sorted(os.listdir('src/tales'))):
        tale = {
            'link': mdfile.split('-', maxsplit=1)[1].rsplit('.', maxsplit=1)[0]
        }
        with codecs.open(os.path.join('src/tales', mdfile), mode='r', encoding='utf-8') as md:
            text = md.read()
            catcher = HeaderCatcher()
            catcher.render(text)
            tale['title'] = catcher.first_head
        yield tale


def main():
    print('Building index.html')
    with open('build/index.html', 'wt') as htmlfile:
        lookup = TemplateLookup(directories=['src/templates'],
                                input_encoding='utf-8',
                                preprocessor=pug_preprocessor)
        htmlfile.write(lookup.get_template('index.pug').render(
            tales=list(list_tales())
        ))


if __name__ == '__main__':
    main()

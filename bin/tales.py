#!/usr/bin/env python3
"""
Renders /tale/*/index.html.
"""

import sys
import re
import os.path
import codecs
from mako.lookup import TemplateLookup
from pypugjs.ext.mako import preprocessor as pug_preprocessor
import hoep


TALE_PATTERN = re.compile(r'(.*/)?[^\-]+-.+.md')


class Markdown(object):

    def __init__(self, mdfile):
        with codecs.open(mdfile, mode='r', encoding='utf-8') as md:
            self.text = md.read()

    def render(self):
        return hoep.render(self.text)


class TalesNavigator(object):

    def __init__(self):
        self.tales = list(self.list_tales())
        self.talesdict = {}
        self.fill_dict()

    @staticmethod
    def list_tales():
        for mdfile in filter(TALE_PATTERN.match, sorted(os.listdir('src/tales'))):
            tale = {
                'link': mdfile.split('-', maxsplit=1)[1].rsplit('.', maxsplit=1)[0]
            }
            yield tale

    def fill_dict(self):
        prev = None
        for tale in self.tales:
            self.talesdict[tale['link']] = tale
            if prev is not None:
                tale['prev_tale'] = prev
                prev['next_tale'] = tale
            prev = tale

    def find_next_tale(self, talelink):
        return self.talesdict[talelink].get('next_tale')

    def find_prev_tale(self, talelink):
        return self.talesdict[talelink].get('prev_tale')


def render_tale(talefile, navigator):
    tale = talefile.split('-', maxsplit=1)[1].rsplit('.', maxsplit=1)[0]
    print('Building tale/{}/index.html'.format(tale))
    os.makedirs('build/tale/{}'.format(tale), exist_ok=True)
    with open('build/tale/{}/index.html'.format(tale), 'wt') as htmlfile:
        lookup = TemplateLookup(directories=['src/templates'],
                                input_encoding='utf-8',
                                preprocessor=pug_preprocessor)
        htmlfile.write(lookup.get_template('tale.pug').render(
            tale=Markdown(talefile),
            next_tale=navigator.find_next_tale(tale),
            prev_tale=navigator.find_prev_tale(tale)
        ))


def main(args):
    navigator = TalesNavigator()
    for talefile in filter(TALE_PATTERN.match, args):
        render_tale(talefile, navigator)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: tale.py src/tales/__.md ..')
        exit(1)
    main(sys.argv[1:])

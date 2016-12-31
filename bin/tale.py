#!/usr/bin/env python3
"""
Renders /tale/*/index.html.
"""

import sys
import os.path
import codecs
from mako.lookup import TemplateLookup
from pypugjs.ext.mako import preprocessor as pug_preprocessor
import hoep


class Markdown(object):

    def __init__(self, mdfile):
        with codecs.open(mdfile, mode='r', encoding='utf-8') as md:
            self.text = md.read()

    def render(self):
        return hoep.render(self.text)


def main(talefile):
    tale = talefile.split('-', maxsplit=1)[1].rsplit('.', maxsplit=1)[0]
    os.makedirs('build/tale/{}'.format(tale), exist_ok=True)
    with open('build/tale/{}/index.html'.format(tale), 'wt') as htmlfile:
        lookup = TemplateLookup(directories=['src/templates'],
                                input_encoding='utf-8',
                                preprocessor=pug_preprocessor)
        htmlfile.write(lookup.get_template('tale.pug').render(
            tale=Markdown(talefile)
        ))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: tale.py src/tales/__.md')
        exit(1)
    main(sys.argv[1])

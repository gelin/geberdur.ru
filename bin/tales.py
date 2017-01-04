#!/usr/bin/env python3
"""
Renders /tale/*/index.html.
"""

import sys
import os.path
from mako.lookup import TemplateLookup
from pypugjs.ext.mako import preprocessor as pug_preprocessor
from libtales import tale_link, Tales, TALE_PATTERN


def render_tale(talefile, tales):
    talelink = tale_link(talefile)
    print('Building tale/{}/index.html'.format(talelink))
    os.makedirs('build/tale/{}'.format(talelink), exist_ok=True)
    with open('build/tale/{}/index.html'.format(talelink), 'wt') as htmlfile:
        lookup = TemplateLookup(directories=['src/templates'],
                                input_encoding='utf-8',
                                preprocessor=pug_preprocessor)
        tale = tales[talelink]
        tale.find_title()
        htmlfile.write(lookup.get_template('tale.pug').render(
            tale=tale
        ))


def main(args):
    tales = Tales()
    for talefile in filter(TALE_PATTERN.match, args):
        render_tale(talefile, tales)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: tale.py src/tales/__.md ..')
        exit(1)
    main(sys.argv[1:])

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
    tale = tale_link(talefile)
    print('Building tale/{}/index.html'.format(tale))
    os.makedirs('build/tale/{}'.format(tale), exist_ok=True)
    with open('build/tale/{}/index.html'.format(tale), 'wt') as htmlfile:
        lookup = TemplateLookup(directories=['src/templates'],
                                input_encoding='utf-8',
                                preprocessor=pug_preprocessor)
        htmlfile.write(lookup.get_template('tale.pug').render(
            tale=tales[tale]
        ))


def main(args):
    tales = Tales(read_markdown=True)
    for talefile in filter(TALE_PATTERN.match, args):
        render_tale(talefile, tales)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: tale.py src/tales/__.md ..')
        exit(1)
    main(sys.argv[1:])

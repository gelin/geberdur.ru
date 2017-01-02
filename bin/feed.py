#!/usr/bin/env python3
"""
Renders feed.xml
"""

from email.utils import formatdate
from mako.lookup import TemplateLookup
from pypugjs.ext.mako import preprocessor as pug_preprocessor
from libtales import Tales


def main():
    print('Building feed.xml')
    with open('build/feed.xml', 'wt') as htmlfile:
        lookup = TemplateLookup(directories=['src/templates'],
                                input_encoding='utf-8',
                                preprocessor=pug_preprocessor)
        htmlfile.write(lookup.get_template('rss.pug').render(
            tales=reversed(list(Tales(read_markdown=True))),
            buildDate=formatdate(timeval=None, localtime=False, usegmt=True)
        ))


if __name__ == '__main__':
    main()

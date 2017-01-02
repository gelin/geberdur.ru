#!/usr/bin/env python3
"""
Renders index.html
"""


from mako.lookup import TemplateLookup
from pypugjs.ext.mako import preprocessor as pug_preprocessor
from libtales import Tales


def main():
    print('Building index.html')
    with open('build/index.html', 'wt') as htmlfile:
        lookup = TemplateLookup(directories=['src/templates'],
                                input_encoding='utf-8',
                                preprocessor=pug_preprocessor)
        htmlfile.write(lookup.get_template('index.pug').render(
            tales=list(Tales(read_markdown=True))
        ))


if __name__ == '__main__':
    main()

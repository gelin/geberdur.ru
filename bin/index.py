#!/usr/bin/env python3

from mako.template import Template
from mako.lookup import TemplateLookup
from pypugjs.ext.mako import preprocessor as pug_preprocessor


def main():
    with open('build/index.html', 'wt') as f:
        lookup = TemplateLookup(directories=['src/templates'],
                                input_encoding='utf-8',
                                preprocessor=pug_preprocessor)
        f.write(lookup.get_template('index.pug').render())


if __name__ == '__main__':
    main()

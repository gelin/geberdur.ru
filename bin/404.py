#!/usr/bin/env python3
"""
Renders 404.html
"""


from mako.lookup import TemplateLookup
from pypugjs.ext.mako import preprocessor as pug_preprocessor


def main():
    print('Building 404.html')
    with open('build/404.html', 'wt') as htmlfile:
        lookup = TemplateLookup(directories=['src/templates'],
                                input_encoding='utf-8',
                                preprocessor=pug_preprocessor)
        htmlfile.write(lookup.get_template('404.pug').render())


if __name__ == '__main__':
    main()

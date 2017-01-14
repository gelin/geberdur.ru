"""
Common library to list and render tales.
"""

import re
import os.path
import codecs
import hoep


__all__ = ['TALE_PATTERN', 'tale_link', 'Tales']


TALES_PATH = 'src/tales'
TALE_PATTERN = re.compile(r'(.*/)?[^\-]+-(?P<link>.+).md')


def tale_link(file_path):
    """
    Extracts link to tale from the markdown file path.
    :param file_path: path to source markdown tale file
    :return: short part of the link
    """
    match = TALE_PATTERN.fullmatch(file_path)
    if match and match.group('link'):
        return match.group('link')
    else:
        return None


class HeaderCatcher(hoep.Hoep):

    def __init__(self, extensions=0, render_flags=0):
        super(HeaderCatcher, self).__init__(extensions, render_flags)
        self.first_head = None

    def header(self, text, level):
        if self.first_head is None and level == 1:
            self.first_head = text
        return ''


class Tale(object):

    def __init__(self, mdfile, read_markdown=False):
        self.mdfile = mdfile
        self.link = tale_link(mdfile)
        self.mdtext = None
        self.title = None
        self.prev = None
        self.next = None
        if read_markdown:
            self.read_mdtext()
            self.find_title()

    def read_mdtext(self):
        with codecs.open(self.mdfile, mode='r', encoding='utf-8') as md:
            self.mdtext = md.read()

    def find_title(self):
        if self.mdtext is None:
            self.read_mdtext()
        catcher = HeaderCatcher()
        catcher.render(self.mdtext)
        self.title = catcher.first_head

    def render(self):
        if self.mdtext is None:
            self.read_mdtext()
        return hoep.render(self.mdtext)


class Tales(object):
    """
    Builds the list of tales objects.
    The list is ordered according to source file names.
    Each tale has a link and references to next and previous.
    If read_markdown is set to True,
    each link also has the title.
    """

    def __init__(self, read_markdown=False):
        """
        List source directory and provides list of tales.
        :param read_markdown: if True the markdown files are read to take title for the tale
        """
        self.tales = list(self.list_tales(read_markdown))
        self.talesdict = {}
        self.fill_dict()

    @staticmethod
    def list_tales(read_markdown):
        for mdfile in filter(TALE_PATTERN.match, sorted(os.listdir(TALES_PATH))):
            tale = Tale(os.path.join(TALES_PATH, mdfile), read_markdown)
            yield tale

    def fill_dict(self):
        prev = None
        for tale in self.tales:
            self.talesdict[tale.link] = tale
            if prev is not None:
                tale.prev = prev
                prev.next = tale
            prev = tale

    def __iter__(self):
        return self.tales.__iter__()

    def __getitem__(self, item):
        return self.talesdict[item]

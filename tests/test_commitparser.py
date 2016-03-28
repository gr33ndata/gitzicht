from unittest import TestCase
from gitzicht import *


example_commit = '''00ab5014a5b
Author: Tarek Amr <gr33ndata@twitter.com>
Date:   Thu Feb 4 15:32:46 2016 +0100

    ISSUE-3840 rename function one to function two
    ISSUE-3832 Add functions three and four 

13  0   README.rst
17  0   irlib/matrix.py'''

class TestCommitParser(TestCase):

    def setUp(self):
        self.cp = CommitParser(example_commit)

    def test_getId(self):
        m = self.cp.getId('commit 00ab5014a5b')
        self.assertEqual(m,'00ab5014a5b')
        m = self.cp.getId('00ab5014a5b')
        self.assertEqual(m,'00ab5014a5b')

    def test_getAuthor(self):
        m = self.cp.getAuthor('Author: Tarek Amr <gr33ndata@twitter.com>')
        self.assertEqual(m['name'],'Tarek Amr')
        self.assertEqual(m['email'],'gr33ndata@twitter.com')
        m = self.cp.getAuthor('Author: Tarek ')
        self.assertEqual(m['name'],'Tarek')
        self.assertEqual(m['email'],'')

    def test_getDate(self):
        m = self.cp.getDate('Date:   Thu Feb 4 15:32:46 2016 +0100')
        self.assertEqual(m.day, 4)
        self.assertEqual(m.month, 2)
        self.assertEqual(m.year, 2016)
        self.assertEqual(m.hour, 15)
        self.assertEqual(m.minute, 32)

    def test_getMessage(self):
        m = self.cp.getMessage('    parsing csv files')
        self.assertEqual(m,'parsing csv files')

    def test_getFiles(self):
        m = self.cp.getFiles([
            '13  0   README.rst',
            '17  0   irlib/matrix.py',
            '',
        ])
        self.assertEqual(len(m), 2)
        self.assertEqual(m[0][0], 'README.rst')
        self.assertEqual(m[0][1], 13)
        self.assertEqual(m[0][2], 0)
        self.assertEqual(m[1][0], 'irlib/matrix.py')
        self.assertEqual(m[1][1], 17)
        self.assertEqual(m[1][2], 0)

    def test_to_map(self):
        self.cp = CommitParser(example_commit)
        m = self.cp.to_map()
        self.assertEqual(m['id'],'00ab5014a5b')
        self.assertEqual(m['author']['name'],'Tarek Amr')
        self.assertEqual(m['author']['email'],'gr33ndata@twitter.com')
        self.assertEqual(len(m['files']), 2)
        self.assertEqual(m['files'][0][0], 'README.rst')
        self.assertEqual(m['files'][0][1], 13)
        self.assertEqual(m['files'][0][2], 0)

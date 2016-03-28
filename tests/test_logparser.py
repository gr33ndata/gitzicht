import os

from unittest import TestCase
from gitzicht import *


class TestLogParser(TestCase):

    def setUp(self):
        tests_path = os.path.dirname(os.path.realpath(__file__))
        file_path = '{}/example_data/example.log'.format(tests_path)
        self.lp = LogParser(file_path)

    def test_read_file(self):
        commits = self.lp.get_commits()
        self.assertEqual(len(commits),188)




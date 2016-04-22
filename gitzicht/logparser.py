from commits import Commits
from commitparser import CommitParser
from sys import stdin

class LogParser:

    def __init__(self, filename):
        self.commits = Commits()
        self.parsed_commits = 0
        self.ignored_commits = 0
        self.filename = filename
        self.read_file(self.filename)

    def read_file(self, filename):
        if filename == 'STDIN':
            file_data = stdin.read()
        else:
            with open(filename, 'r') as fd:
                file_data = fd.read()
        for commit in file_data.split('\ncommit'):
            commit = commit.strip()
            try:
                self.commits.append(self.parse_commit(commit))
                self.parsed_commits += 1
            except:
                self.ignored_commits += 1

    def print_debug_message(self):
        print 'File [{}] has been read.'.format(self.filename)
        print '* {} commits parsed successfully.'.format(self.parsed_commits)
        if self.ignored_commits:
            print '* {} commits ignored.'.format(self.ignored_commits)

    def get_commits(self, per_file=False):
        if per_file:
            return self.commits.per_file()
        else:
            return self.commits

    def parse_commit(self, commit):
        parsed_commit = CommitParser(commit)
        return parsed_commit.to_map()
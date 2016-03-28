import re
from dateutil import parser as data_parser 

from commits import Commits

class CommitParser:

    def __init__(self, commit=''):
        if not commit:
            raise Exception('empty commit') 
        try:
            commit_parts = commit.split('\n\n')
            if len(commit_parts) == 3:
                header, message, changes = commit_parts
            elif len(commit_parts) == 2:
                header, changes = commit_parts
                message = ''
            else:
                raise Exception
            header_lines = [
                line.strip() 
                for line in header.split('\n')
            ]
            message = message.replace('\n', ' ')
            changes_lines = [
                line.strip() 
                for line in changes.split('\n')
            ]
            self.commitId = self.getId(header_lines[0])
            self.commitAuthor = self.getAuthor(header_lines[1])
            self.commitDate = self.getDate(header_lines[2])
            self.commitMessage = self.getMessage(message)
            self.commitFiles = self.getFiles(changes_lines)
        except:
            raise Exception('could not parse commit') 

    def to_map(self):
        return {
            'id': self.commitId,
            'author': self.commitAuthor,
            'date': self.commitDate,
            'message': self.commitMessage,
            'files': self.commitFiles
        }

    def getId(self, line):
        return line.rsplit(' ',1)[-1]

    def getAuthor(self, line):
        match = re.match(r"Author: (?P<name>[a-zA-Z0-9\s]+) <(?P<email>[a-zA-Z0-9\_\@\.]+)>", line)
        if match:
            name = match.group('name').strip()
            email = match.group('email').strip()
        else:
            name = line.rsplit(':',1)[-1].strip()
            email = ''
        return { 
            'name': name, 
            'email': email
        }

    def getDate(self, line):
        date_part = line[len('Date:'):]
        return data_parser.parse(date_part)

    def getMessage(self, line):
        return line.strip()

    def atoi(self, s):
        s = s.strip() 
        if s == '-':
            return 0
        else:
            return int(s)

    def parseFileLine(self, file_line):
        addition, deletion, path = [
            item.strip() 
            for item in file_line.split(None, 2)
        ]
        return (path, self.atoi(addition), self.atoi(deletion))

    def getFiles(self, lines):
        parsed_lines = [
            self.parseFileLine(file_line)
            for file_line in lines
            if file_line.strip()
        ]
        return parsed_lines


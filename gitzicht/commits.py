import copy

class Commits:

    def __init__(self):
        self.data = []

    def __len__(self):
        return len(self.data)

    def __getitem__(self, i):
        return self.data[i]

    def __iter__(self):
        for commit in self.data:
            yield commit

    def per_file(self):
        for commit in self.data:
            for file in commit['files']:
                commit_ = copy.deepcopy(commit)
                commit_['files'] = file
                yield commit_ 
    
    def append(self, commit):
        self.data.append(commit)
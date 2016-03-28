import pandas as pd

from commits import Commits

class Pivot:

    def __init__(self, dim1=None, dim2=None, metric=None):
        self.dim1 = Pivot._dim1 if dim1 is None else dim1 
        self.dim2 = Pivot._dim2 if dim2 is None else dim2 
        self.metric = Pivot._metric if metric is None else metric 

    @classmethod
    def _dim1(cls, commit):
        return Pivot.dim_year(commit)

    @classmethod
    def _dim2(cls, commit):
        return 'total commits'

    @classmethod
    def _metric(cls, commit):
        return Pivot.metric_commits(commit)

    @classmethod
    def dim_year(cls, commit): 
        return str(commit['date'].year)

    @classmethod
    def dim_month(cls, commit): 
        return "%02d" % commit['date'].month

    @classmethod
    def dim_year_month(cls, commit):
        year = cls.dim_year(commit)
        month = cls.dim_month(commit)
        return '{}-{}'.format(year, month)

    @classmethod
    def dim_module_name(cls, commit):
        path = commit['files'][0].split('/')
        if len(path) > 1:
            module_path = '/'.join(path[:-1])
        else:
            module_path = 'ROOT'
        return module_path

    @classmethod    
    def dim_file_name(cls, commit):
        path = commit['files'][0].split('/')
        return path[-1]

    @classmethod
    def metric_commits(cls, commit):
        return 1

    @classmethod
    def metric_additions(cls, commit):
        _, addition, _ = commit['files']
        return addition

    @classmethod
    def metric_deletions(cls, commit):
        _, _, deletion = commit['files']
        return deletion

    @classmethod
    def metric_changes(cls, commit):
        return (cls.metric_additions(commit) + cls.metric_deletions(commit))

    @classmethod
    def list_dims(cls):
        return [attr for attr in dir(cls) if attr.startswith('dim_')]

    @classmethod
    def list_metrics(cls):
        return [attr for attr in dir(cls) if attr.startswith('metric_')]

    def calculate(self, commits, as_dataframe=True):
        p = {}
        for commit in commits:
            dim1 = self.dim1(commit)
            dim2 = self.dim2(commit)
            metric = self.metric(commit)
            p[dim1] = p.get(dim1, {}) 
            p[dim1][dim2] = p[dim1].get(dim2, 0) + metric
        if as_dataframe:
            return pd.DataFrame(p).fillna(0) 
        else:
            return p

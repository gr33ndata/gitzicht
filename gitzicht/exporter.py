import pandas as pd
from sys import stdout

class Exporter:

    def __init__(self, df):
        self.df = df

    def to_csv(self, file_name, index_label='index'):
        if file_name == 'STDOUT':
            self.df.to_csv(stdout, index_label=index_label)
        else:
            with open(file_name, 'w') as fd:
                self.df.to_csv(fd, index_label=index_label)
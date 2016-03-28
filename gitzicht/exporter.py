import pandas as pd

class Exporter:

    def __init__(self, df):
        self.df = df

    def to_csv(self, file_name, index_label='index'):
        with open(file_name, 'w') as fd:
            self.df.to_csv(fd, index_label=index_label)
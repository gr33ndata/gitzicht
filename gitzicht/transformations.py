class Transformations:

    @classmethod
    def dim1_filter_regex(cls, df, regex='.*\.java'):
        return df.filter(regex=regex)

    @classmethod
    def dim2_filter_regex(cls, df, regex='201[456]'):
        df = df.T
        return df.filter(regex=regex).T

    @classmethod
    def dim1_top_n(cls, df, n=10):
        top_n_list = [
            k for k, v 
            in df.sum().rank(ascending=False).to_dict().items() 
            if v < (n+1)
        ]
        return df.filter(items=top_n_list)
    
import pandas as pd

class MinMaxScaler:

    def __init__(self):
        
        self.min = None
        self.max = None

    def fit(self,
            x):

        if type(x) == pd.core.frame.DataFrame:
            x = x.to_numpy()

        self.min = x.min(axis=0)
        self.max = x.max(axis=0)

    def transform(self,
                  x):
        
        x = (x - self.min) / (self.max - self.min)
        return x
    
    def fit_transform(self, x):

        self.fit(x)
        x = self.transform(x)

        return x
import pandas as pd

class Load():
    def __init__(self):
        self.example_path = '.\TestData\daily power.csv'

    def load_profile(self):
        profile = pd.read_csv(self.example_path,index_col=0)
        profile = profile['total'] * 24 * 60 * 60
        return profile

    def get_output(self):

        pass

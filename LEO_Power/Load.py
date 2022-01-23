import pandas as pd

class Load():
    def __init__(self):
        self.example_path = '.\TestData\daily power.csv'
        self.path = '.\Data\demand(noEV).csv'

    def load_profile(self):
        demand = pd.read_csv(self.path)
        demand['Energy'] = demand['Power']*0.5
        return demand


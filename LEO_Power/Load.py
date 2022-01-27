import pandas as pd

class Load():
    def __init__(self):
        self.example_path = '.\TestData\daily power.csv'
        self.path = '.\Data\demand(noEV).csv'

    def load_profile(self,duration=1):
        demand = pd.read_csv(self.path)
        demand['Energy'] = demand['Power']*0.5
        return demand

if __name__ == 'main':
    myload=Load()
    demand = myload.load_profile(2)
    print(demand)

import pandas as pd

class Load():
    def __init__(self,duration=1):
        self.path = '.\Data\demand(noEV).csv'
        self.duration = duration

    def load_profile(self):
        demand = pd.read_csv(self.path)
        demand['Energy'] = demand['Power']*0.5
        demand = demand.drop(labels=['Unnamed: 0', "Power"], axis=1)
        demand.drop([len(demand)-1],inplace=True)
        i = 1
        demand_p = demand.copy()
        while i < self.duration:
            demand_p['Energy'] = demand_p['Energy'] * 1.005
            demand = pd.concat([demand, demand_p], axis=0, ignore_index=True)
            i+=1
        return demand

if __name__ == 'main':
    myload=Load()

    demand = myload.load_profile()


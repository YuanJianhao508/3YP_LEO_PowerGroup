import pandas as pd
import utils

class Load():
    def __init__(self,duration=1):
        self.path = '.\Data\demand(noEV).csv'
        self.duration = duration

    def load_profile(self):
        demand = pd.read_csv(self.path)
        demand['Energy'] = demand['Power']*0.5
        demand = demand.drop(labels=['Unnamed: 0', "Power",'Datetime'], axis=1)
        demand.drop([len(demand)-1],inplace=True)

        i = 1
        demand_p = demand.copy()
        size = len(demand['Energy'])
        while i < self.duration:
            noise = utils.gaussian_noise(size, form='series', on='load', sigma=0.0001, mu=0)
            demand_p['Energy'] = demand_p['Energy'] * 1.005 + noise
            demand = pd.concat([demand, demand_p], axis=0, ignore_index=True)
            i+=1
        return demand

    def new_load_profile(self):
        pass

if __name__ == 'main':
    myload=Load()

    demand = myload.load_profile()


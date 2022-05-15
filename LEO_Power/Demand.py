import pandas as pd
import numpy as np
import utils

class Demand():
    def __init__(self,duration=1,nhousehold=3500,PVTcapacity=2):
        self.path = '.\Data\demand(noEV).csv'
        self.hw = '.\Data\DHW_HH2.csv'
        self.alle = '.\Data\HH_electricity.csv'
        self.ev = '.\Data\demandEVMW.csv'
        self.sh = '.\Data\HH_spaceheating_heat.csv'
        self.PVT = '.\Data\solar.csv'
        self.duration = duration
        self.nhousehold = nhousehold
        self.CopHotWater = 2.2
        self.CopSpaceHeating = 3.2
        self.PVTcapacity = PVTcapacity

    def load_profile(self):
        hw = pd.read_csv(self.hw)
        alle = pd.read_csv(self.alle)
        ev = pd.read_csv(self.ev)
        sh = pd.read_csv(self.sh)
        PVT = pd.read_csv(self.PVT)

        # PVT balance
        PVT['Heat'] = PVT['Power (MW)'] * 2 * self.PVTcapacity
        # print(sum(PVT['Heat']),'PVT')
        P2DHW = hw['Heat']-PVT['Heat']

        excessDHW = np.maximum(P2DHW, 0)
        PH2 = -np.minimum(P2DHW, 0)
        P2SH = sh['Heat'] - PH2
        excessSH = np.maximum(P2SH, 0)

        demand = pd.DataFrame()
        demand['Energy'] = 0.5 * ((1/self.CopSpaceHeating)*excessSH+(1/self.CopHotWater)*excessDHW+ev['Power']+alle['Power'])
        demand = (self.nhousehold/3500) * demand

        i = 1
        demand_p = demand.copy()
        size = len(demand['Energy'])
        while i < self.duration:
            noise = utils.gaussian_noise(size, form='series', on='load', sigma=1, mu=0)
            demand_p['Energy'] = demand_p['Energy'] * (1.00)**i + noise
            demand = pd.concat([demand, demand_p], axis=0, ignore_index=True)
            i+=1


        # print('total load',demand['Energy'].sum(),'MWh')
        return demand



load = Demand(1)
load_profile = load.load_profile()
load_profile.to_csv('demand_feat')


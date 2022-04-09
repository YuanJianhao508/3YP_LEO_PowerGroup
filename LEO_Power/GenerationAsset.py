import pandas as pd
import utils



class GenerationAsset():
    def __init__(self,capacity,duration=1,type='solar'):
        # possible design factor size, angle, power factor etc...
        self.solar_path = '.\Data\solar.csv'
        self.wind_path = '.\Data\wind.csv'
        self.capacity = capacity
        self.duration = duration
        self.type = type
        self.wearout = {'solar':0.998,'solarPVT':0.998,'wind':0.998}

    def load_profile(self):
        if self.type == 'solar':
            solar = pd.read_csv(self.solar_path)
        elif self.type == 'solarPVT':
            solar = pd.read_csv(self.solar_path)
            solar['Power (MW)'] = solar['Power (MW)'] * 1.1
        elif self.type == 'wind':
            solar = pd.read_csv(self.wind_path)

        # print(self.type)

        solar['Power'] = solar['Power (MW)']
        solar['Power'] = solar['Power'] * self.capacity
        solar['Energy'] = solar['Power'] * 0.5
        solar = solar.drop(labels=['Power (MW)', "Power",'Datetime'], axis=1)
        i = 1
        solar_p = solar.copy()
        size = len(solar['Energy'])
        while i < self.duration:
            noise = utils.gaussian_noise(size, form='series', on='solar',sigma=1, mu=0)
            solar_p['Energy'] = (solar_p['Energy'] * (self.wearout[self.type])**i) + noise

            solar = pd.concat([solar, solar_p], axis=0, ignore_index=True)
            i+=1
        return solar



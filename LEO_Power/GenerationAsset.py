import pandas as pd
import utils



class GenerationAsset():
    def __init__(self,capacity,duration=1,type='solar'):
        # possible design factor size, angle, power factor etc...
        self.solar_path = '.\Data\solar.csv'
        self.wind_path = '.\Data\solar.csv'
        self.capacity = capacity
        self.duration = duration
        self.type = type

    def load_profile(self):
        if self.type == 'solar':
            solar = pd.read_csv(self.solar_path)
        elif self.type == 'wind':
            solar = pd.read_csv(self.wind_path)
        solar['Power'] = solar['Power (MW)']
        solar['Power'] = solar['Power'] * self.capacity
        solar['Energy'] = solar['Power'] * 0.5
        solar = solar.drop(labels=['Power (MW)', "Power",'Datetime'], axis=1)
        i = 1
        solar_p = solar.copy()
        size = len(solar['Energy'])
        while i < self.duration:
            noise = utils.gaussian_noise(size, form='series', on='solar',sigma=0.0001, mu=0)
            solar_p['Energy'] = solar_p['Energy'] * 0.990 + noise
            solar = pd.concat([solar, solar_p], axis=0, ignore_index=True)
            i+=1
        return solar


if __name__ == 'main':
    solar = GenerationAsset(100)
    solar_profile = solar.load_profile()
    print(type(solar_profile))

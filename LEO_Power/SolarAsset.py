import pandas as pd




class SolarAsset():
    def __init__(self,capacity,duration=1):
        # possible design factor size, angle, power factor etc...
        self.path = '.\Data\solar.csv'
        self.capacity = capacity
        self.duration=duration

    def load_profile(self):
        solar = pd.read_csv(self.path)
        solar['Power'] = solar['Power (MW)']
        solar['Power'] = solar['Power'] * self.capacity
        solar['Energy'] = solar['Power'] * 0.5
        solar = solar.drop(labels=['Power (MW)', "Power"], axis=1)
        i = 1
        solar_p = solar.copy()
        while i < self.duration:
            solar_p['Energy'] = solar_p['Energy'] * 0.990
            solar = pd.concat([solar, solar_p], axis=0, ignore_index=True)
            i+=1
        return solar


if __name__ == 'main':
    solar = SolarAsset(100)
    solar_profile = solar.load_profile()
    print(type(solar_profile))

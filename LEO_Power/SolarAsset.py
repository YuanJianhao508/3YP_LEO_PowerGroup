import pandas as pd

class SolarAsset():
    def __init__(self,capacity):
        # possible design factor size, angle, power factor etc...
        self.path = '.\Data\solar.csv'
        self.capacity = capacity
        self.unit_cost = 100

    def load_profile(self):
        solar = pd.read_csv(self.path)
        solar['Power'] = solar['Power (MW)']
        solar['Power'] = solar['Power'] * self.capacity
        solar['Energy'] = solar['Power'] * 0.5
        return solar


if __name__ == 'main':
    solar = SolarAsset(100)
    solar_profile = solar.load_profile()

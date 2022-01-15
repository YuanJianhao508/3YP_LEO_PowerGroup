import pandas as pd

class SolarAsset():
    def __init__(self,size):
        # possible design factor size, angle, power factor etc...
        self.example_path = '.\TestData\Daily_Solar_Generation.csv'
        self.capacity = size

        self.unit_cost = 100

    def load_profile(self):
        profile = pd.read_csv(self.example_path)
        profile = profile['Energy (MWh)'] * self.capacity
        return profile

    def get_output(self):
        pass

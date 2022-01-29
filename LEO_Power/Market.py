import pandas as pd
import numpy as np

class Market():
    def __init__(self,net_nondispatchable_load,load_profile_lis,generation_profile_lis,storage_profile_lis):
        self.solar_profile = generation_profile_lis
        self.storage_profile = storage_profile_lis
        self.load_profile = load_profile_lis
        self.net_load_profile = net_nondispatchable_load


    def load_info(self):
        pass

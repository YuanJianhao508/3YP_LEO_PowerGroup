import numpy as np
import pandas as pd
from datetime import datetime



def generation_list2dict(solar_lis,wind_lis):
    """
    transfer list of generation capacity to dictionary required by EnergySystem
    :param solar_lis: list of solar power capacity []
    :param wind_lis: list of wind power capacity []
    :return: dictionary contain capacity and type
    """
    res = []
    for i in solar_lis:
        res.append({'size': i,'type':'solar'})
    for i in wind_lis:
        res.append({'size': i, 'type': 'wind'})
    return res

def gaussian_noise(size,form='np',on='solar',sigma=0.05,mu=0):
    """
    create gaussian noise
    :param size: size of array
    :param form: np_array or series
    :param on: solar or load
    :param sigma: variance
    :param mu: mean
    :return: gaussian noise
    """
    noise = np.random.normal(mu,sigma,size)

    if form == 'series':
        noise = pd.Series(noise)
    return noise





def get_day_sample():
    sample = []
    s = ['00','01','02','03','04','05','06','07','08','09','10','11','12','13',
         '14','15','16','17','18','19','20','21','22','23']
    half = False
    for i in s:
        for r in range(2):
            if half:
                sample.append(i+':30')
                half = False
            else:
                sample.append(i+':00')
                half = True
    # print(sample)
    return sample

def get_index_day(prefix,window):
    index = []
    for i in range(1,window+1):
        index.append(prefix+str(i))

    return index
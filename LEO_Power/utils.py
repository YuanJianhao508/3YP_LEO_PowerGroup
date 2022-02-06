import numpy as np
import pandas as pd


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
    if on == 'solar':
        noise = abs(noise)

    if form == 'series':
        noise = pd.Series(noise)

    return noise


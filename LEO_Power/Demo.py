import Optimizer as op
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt

# # Basic simulation
solar = [30,17.5]
load = True
storage = [[7.5,20],[7.5,20]]
net_profile = op.basic_simulation__visualization(load,solar,storage,True)
net_profile = net_profile[:-1]
print(sum(net_profile))


#grid search 2d test
#Run
# solar_search = list(range(20, 20 + 100, 2))
# storage_search_power = list(range(20, 20 + 80, 2))
# nplis = op.grid_search_2d(solar_search,storage_search_power,load=True)
# np.save('Result/2d_search_nplis_2.npy', nplis)
#
# nplis = np.load('Result/2d_search_nplis_2.npy')
# ta_lis = []
# pa_lis = []
# money_lis = []
# for i in tqdm(nplis):
#     ta_lis.append(sum(i * 0.5))
#     pa = 0
#     for j in i:
#         if j>0:
#             pa += j*0.5
#     pa_lis.append(pa)
#
#
# print(pa_lis)
# plt.plot(np.arange(len(pa_lis)),np.array(pa_lis))
# plt.show()


# np.save('Result/2d_search_metric_test2.npy', m)
# np.save('Result/2d_search_setting_test2.npy', s)

#Analyze
# m = np.load('Result/2d_search_metric_test1.npy')
# s = np.load('Result/2d_search_setting_test1.npy')

# op_setting = op.grid_search_analysis(m,s)
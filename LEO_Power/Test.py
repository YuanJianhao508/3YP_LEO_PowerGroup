import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
from GenerationAsset import GenerationAsset
from Demand import Demand
from EnergySystem import EnergySystem
import utils
# from PredictiveModel import *
from gurobipy import *
import pyomo.environ as pyo

def ObjRule(model):
    return sum(pimp[i]*model.Ed[i] for i in model.Ed) - sum(pexp[k] * model.Es[k] for k in model.Es) + \
           pfin*(model.state[sindex[-1]])

def ed_con1(model,i):
    return model.Ed[i] >= model.Lnet[i]
#
def ed_con2(model,i):
    return model.Ed[i] >= 0

def es_con1(model,i):
    return model.Es[i] <= model.Lnet[i]

def es_con2(model,i):
    return model.Es[i] <= 0

def state_con1(model,i):
    return model.sout[i] >= -energy + model.state[i]

def state_con2(model,i):
    return model.sout[i] <= model.state[i]

def eq1(model,i):
    return model.Lnet[i] == predgen[i] - model.sout[i]

window = 48


sindex = utils.get_index_day('s',window)

def basic_simulation(load,solar,storage,duration):
    LEO = EnergySystem(load,solar,storage,duration)
    [net_profile,load_profile_lis,generation_profile_lis,storage_profile_lis,metric] = LEO.simulate('all_detail')
    return [net_profile,load_profile_lis,generation_profile_lis,storage_profile_lis,metric]

solar = [{'size':2,'type':'solarPVT'},{'size':11,'type':'solar'},{'size':5,'type':'wind'}]
load = 3500
power = 7.4
energy = 32
storage = [[power,energy,'local']]
g_labels = ['Rooftop PVT','Solar Farm PV','Wind']
s_labels = ['Local Battery']
duration = 1

[net_profile,load_profile_lis,generation_profile_lis,storage_profile_lis,metric] = basic_simulation(load,solar,storage,duration)

load_profile = load_profile_lis[0]['profile']['Energy'].to_numpy()

exist = False
for i in generation_profile_lis:
    k = i['profile']['Energy'].to_numpy()
    if not exist:
        generation_profile = k
        exist = True
    else:
        generation_profile += k


load_profile=np.concatenate([load_profile,load_profile[:48]])
generation_profile=np.concatenate([generation_profile,generation_profile[:48]])
netraw_profile = load_profile-generation_profile

pimp = [2 for i in range(window)]
pexp = [1 for i in range(window)]
pfin = pexp[-1]
pimp = dict(zip(sindex, pimp))
pexp = dict(zip(sindex, pexp))

sout_lis = []
state_lis = []
ini_state = 10
time = 1

for i in tqdm(range(len(netraw_profile)-48)):
    try:
        horizon = netraw_profile[i:i+48]
        # print(horizon)

        predgen = dict(zip(sindex, horizon))

        model = pyo.ConcreteModel()
        model.sout = pyo.Var(sindex, bounds=(-power * 0.5, power * 0.5))
        model.Ed = pyo.Var(sindex, bounds=(0, None))
        model.Es = pyo.Var(sindex, bounds=(None, 0))
        model.state = pyo.Var(sindex, bounds=(0, energy))
        model.Lnet = pyo.Var(sindex)

        model.obj = pyo.Objective(rule=ObjRule)

        model.con1 = pyo.Constraint(sindex, rule=ed_con1)
        model.con2 = pyo.Constraint(sindex, rule=es_con1)
        model.con3 = pyo.Constraint(sindex, rule=state_con1)
        model.con4 = pyo.Constraint(sindex, rule=state_con2)
        model.eq1 = pyo.Constraint(sindex, rule=eq1)

        model.limits = pyo.ConstraintList()
        for i in range(len(sindex)):
            if i == 0:
                model.limits.add(expr=model.state[sindex[i]] == ini_state)
            else:
                model.limits.add(expr=model.state[sindex[i]] == model.state[sindex[i - 1]] - model.sout[sindex[i - 1]])

        # model.pprint()
        opt = pyo.SolverFactory('gurobi').solve(model)

        # print('System Cost:', pyo.value(model.obj))

        sout = []
        # ed = []
        # es = []
        state = []
        # Lnet = []
        for i in sindex:
            sout.append(pyo.value(model.sout[i]))
            # ed.append(pyo.value(model.Ed[i]))
            # es.append(pyo.value(model.Es[i]))
            # Lnet.append(pyo.value(model.Lnet[i]))
            state.append(pyo.value(model.state[i]))

        # print('sout:', sout)
        # print('state:', state)
        # print('Lnet', Lnet)
        # print('ed:', ed)
        # print('es:', es)
        # print('netraw',horizon)

        sout_lis.append(sout[0])
        ini_state = state[1]
        state_lis.append(ini_state)

    except:
        print("nmsl")

np.save('TestData/sout_lis_3', sout_lis)
np.save('TestData/state_lis_3', state_lis)
    # time += 1
    # if time == 48:
    #     net = horizon - sout
    #     plt.plot(net)
    #     plt.show()
    #     break













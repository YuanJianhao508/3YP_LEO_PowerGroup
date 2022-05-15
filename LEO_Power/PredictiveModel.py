import torch
import os
import numpy as np
import pandas as pd
from tqdm import tqdm
import seaborn as sns
from pylab import rcParams
import matplotlib.pyplot as plt
from matplotlib import rc
from sklearn.preprocessing import MinMaxScaler
import torch
from torch.utils.data import Dataset, DataLoader
from torch import nn, optim
import pytorch_lightning as pl
import Demand

from GenerationAsset import GenerationAsset
from Demand import Demand
plt.style.use("fivethirtyeight")  # 538样式


class LEODataset(Dataset):
    def __init__(self, sequences):
        self.sequences = sequences

    def __len__(self):
        return len(self.sequences)

    def __getitem__(self, idx):
        sequence, label = self.sequences[idx]
        return dict(
            sequence=torch.Tensor(sequence.to_numpy()),
            label=torch.tensor(label).float()
        )

class LEOModule(pl.LightningDataModule):

    def __init__(self, train_sequences, test_sequences, batch_size):
        super().__init__()
        self.train_sequences = train_sequences
        self.test_sequences = test_sequences
        self.batch_size = batch_size

    def setup(self):
        self.trainDataset = LEODataset(self.train_sequences)
        self.testDataset = LEODataset(self.test_sequences)

    def trainDataLoader(self):
        return DataLoader(
            self.trainDataset,
            batch_size=self.batch_size,
            shuffle=False
        )

    def testDataLoader(self):
        return DataLoader(
            self.testDataset,
            batch_size=1,
            shuffle=False
        )


# Model
class PredictiveModle(nn.Module):
    def __init__(self, n_features, n_hidden=64, n_layers=1):
        super().__init__()

        self.n_hidden = n_hidden
        self.lstm = nn.LSTM(
            input_size=n_features,
            hidden_size=n_hidden,
            num_layers=n_layers,
            batch_first=True
        )
        self.regressor = nn.Linear(n_hidden, 1)

    def forward(self, x):
        self.lstm.flatten_parameters()
        _, (hidden, _) = self.lstm(x)
        out = self.regressor(hidden[-1])
        return out

# Pre-processing

def create_sequence(input_data,target_column,sequence_length):
    sequence_lis = []
    data_size = len(input_data)
    for i in tqdm(range(data_size-sequence_length)):
        sequence = input_data[i:i+sequence_length]
        label_position = i+sequence_length
        label = input_data.iloc[label_position][target_column]
        sequence_lis.append((sequence,label))
    return sequence_lis

def load_checkpoint(model, checkpoint_PATH, optimiser):
    if checkpoint_PATH != None:
        model_CKPT = torch.load(checkpoint_PATH)
        model.load_state_dict(model_CKPT['state_dict'])
        print('loading checkpoint!')
        optimiser.load_state_dict(model_CKPT['optimizer'])
    return model, optimiser

def load_checkpoint_hist(model, checkpoint_PATH, optimiser):
    if checkpoint_PATH != None:
        model_CKPT = torch.load(checkpoint_PATH)
        model.load_state_dict(model_CKPT['state_dict'])
        print('loading checkpoint!')
        optimiser.load_state_dict(model_CKPT['optimizer'])
        train_hist = model_CKPT['train_hist']
        test_hist = model_CKPT['test_hist']
    return model, train_hist, test_hist

def load_data():
    solar = pd.read_csv('.\Data\solar.csv')
    wind = pd.read_csv('.\Data\wind.csv')
    weatherin = pd.read_csv('.\Data\weather_clean.csv')

    weatherin['wind_gen'] = wind['Power (MW)']
    weatherin['solar_gen'] = solar['Power (MW)']

    weatherin.set_index('time',inplace=True)
    weatherin.reset_index(inplace=True)
    weatherin.drop(columns=['time'],inplace=True)
    return weatherin



def train_model(target,SequenceLength=100,BatchSize=16,Epoch=4,vis=True):

    weatherin = load_data()

    # Prepare Training Data
    data = weatherin[:500]

    train_size = int(len(data) * 0.9)
    train_df,test_df = data[:train_size],data[train_size:]

    #Normalize Data
    scaler = MinMaxScaler(feature_range=(-1,1))
    scaler = scaler.fit(train_df)

    #Prepare DataSet
    train_df = pd.DataFrame(
        scaler.transform(train_df),
        index = train_df.index,
        columns = train_df.columns
    )

    test_df = pd.DataFrame(
        scaler.transform(test_df),
        index = test_df.index,
        columns = test_df.columns
    )

    train_sequences = create_sequence(train_df,target,SequenceLength)
    test_sequences = create_sequence(test_df,target,SequenceLength)
    n_features = train_df.shape[1]
    data_module = LEOModule(train_sequences,test_sequences,BatchSize)
    data_module.setup()
    model = PredictiveModle(n_features)

    #Train
    optimiser = torch.optim.Adam(model.parameters(), lr=1e-3)
    loss_fn = torch.nn.MSELoss(reduction='sum')
    train_hist = np.zeros(Epoch+1)
    test_hist = np.zeros(Epoch+1)
    t=0

    for t in tqdm(range(Epoch+1)):
        #     for item in tqdm(data_module.trainDataLoader(),leave=False):
        for item in data_module.trainDataLoader():

            out = model(item["sequence"])
            loss = loss_fn(out.float(), item["label"])

            with torch.no_grad():
                for s in data_module.testDataLoader():
                    y_test_pred = model(s["sequence"])
                    test_loss = loss_fn(y_test_pred.float(), s["label"])
                    test_hist[t] = test_loss.item()

            train_hist[t] = loss.item() / BatchSize
            optimiser.zero_grad()
            loss.backward()
            optimiser.step()

        if t == Epoch - 1:
            torch.save({'epoch': t + 1, 'state_dict': model.state_dict(), 'best_loss': loss,
                        'optimizer': optimiser.state_dict()},
                       './Model' + '/m-' + str("%.4f" % loss) + '.pth')
    #Shown training process
    if vis:
        fig, ax1 = plt.subplots(figsize=(15, 7))
        ax1.plot(train_hist, linewidth=5, markersize=12,label="Training loss")
        ax1.plot(test_hist, linewidth=5, markersize=12, label="Test loss")
        ax1.set_xlabel("No. Iteration")
        ax1.set_ylabel("MSE Loss")
        ax1.set_title('Training')
        plt.legend()
        plt.show()


def plot_hist(path):


    weatherin = load_data()
    n_features = weatherin.shape[1]
    model = PredictiveModle(n_features)
    optimiser = torch.optim.Adam(model.parameters(), lr=1e-3)
    model, train_hist, test_hist = load_checkpoint_hist(model, path, optimiser)

    fig, ax1 = plt.subplots(figsize=(15, 7))
    ax1.axhline(y=0, color='black', linewidth=1.3, alpha=.7)
    #solar
    ax1.plot(train_hist/16, label="Training loss")
    ax1.plot(test_hist[::-1], label="Test loss")


    ax1.set_ylabel("MSE Loss")
    ax1.set_xlabel("Training Epoch")
    ax1.set_title("Training and Validation Loss of Solar")
    ax1.set_xticks(list(range(1,21)))
    ax1.legend()
    plt.show()


def predict_all(target,window,mon,SequenceLength=100,path = './model/m-0.6836solar.pth',vis = True):


    weatherin = load_data()

    start = mon * window
    weatherin = weatherin[start-SequenceLength:start + window]

    n_features = weatherin.shape[1]
    train_size = int(len(weatherin) * 0.9)
    train_df, test_df = weatherin[:train_size], weatherin[train_size:]
    #Normalize Data
    scaler = MinMaxScaler(feature_range=(-1,1))
    scaler = scaler.fit(train_df)

    model = PredictiveModle(n_features)
    optimiser = torch.optim.Adam(model.parameters(), lr=1e-3)
    model, optimiser = load_checkpoint(model, path, optimiser)

    val_df = pd.DataFrame(
        scaler.transform(weatherin),
        index = weatherin.index,
        columns = weatherin.columns
    )

    val_s = create_sequence(val_df, target, SequenceLength)
    depDataset = LEODataset(val_s)
    depDataLoader = DataLoader(depDataset, batch_size=1)
    # predict
    with torch.no_grad():
        preds = []
        gt = []
        for s in tqdm(depDataLoader):
            y_test_pred = model(s["sequence"])
            preds.append(torch.flatten(y_test_pred).item())
            gt.append(torch.flatten(s["label"]).item())
    preds = np.array(preds)
    gt = np.array(gt)
    target_scaler = scaler.fit(np.array(weatherin[target]).reshape(-1, 1))
    predicted_cases = target_scaler.inverse_transform(preds.reshape(-1, 1)).flatten()
    gt_cases = target_scaler.inverse_transform(gt.reshape(-1, 1)).flatten()

    #result plot
    if vis:
        fig, ax1 = plt.subplots(figsize=(15, 7))
        ax1.axhline(y=0, color='black', linewidth=1.3, alpha=.7)
        ax1.plot(predicted_cases, linewidth=5, markersize=12,label='Prediction')
        ax1.plot(gt_cases,linewidth=5, markersize=12,label='GroundTruth')
        ax1.set_ylabel("Energy (MWh)")
        ax1.set_xlabel("Half-hourly period over a week")
        ax1.set_title("Solar Generation Prediction Over a Week")
        ax1.legend()
        plt.show()
        return predicted_cases
    else:
        return predicted_cases,gt_cases

# predict_all('solar_gen',336,24,100,'./model/m-0.6836solar.pth')
# plot_hist('./model/m-0.6836solar.pth')
# 24
# predict_all('wind_gen',336,51,100,'./model/m-3.6187wind.pth')
# plot_hist('./model/m-3.6187wind.pth')
# 51

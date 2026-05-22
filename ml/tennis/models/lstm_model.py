import torch
import torch.nn as nn
from torch.utils.data import DataLoader

class TennisLSTM(nn.Module):
    def __init__(self, input_size=23, hidden1=128, hidden2=64, dropout=0.3):
        super(TennisLSTM, self).__init__()
        self.lstm1 = nn.LSTM(input_size, hidden1, batch_first=True)
        self.dropout1 = nn.Dropout(dropout)
        self.lstm2 = nn.LSTM(hidden1, hidden2, batch_first=True)
        self.dropout2 = nn.Dropout(dropout)
        self.fc1 = nn.Linear(hidden2, 32)
        self.fc2 = nn.Linear(32, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        # x shape: [batch, 15, 23]
        out, _ = self.lstm1(x)
        out = self.dropout1(out)
        out, _ = self.lstm2(out)
        out = self.dropout2(out)
        # Take the last sequence output
        out = self.fc1(out[:, -1, :])
        out = torch.relu(out)
        out = self.fc2(out)
        return self.sigmoid(out)

    def train_model(self, train_loader, val_loader, epochs=100, lr=0.001):
        optimizer = torch.optim.AdamW(self.parameters(), lr=lr)
        scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, 'min')
        criterion = nn.BCELoss()
        # Training loop logic here...

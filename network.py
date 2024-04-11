import torch
import time

from torch import nn

device = "cuda"

class Residual(nn.Module):
    def __init__(self):
        super().__init__()
        self.pre = nn.Sequential(
            nn.Conv2d(256, 256, 3, 1, 1),
            nn.BatchNorm2d(256),
            nn.ReLU(),
            nn.Conv2d(256, 256, 3, 1, 1),
            nn.BatchNorm2d(256),
            )
        self.relu = nn.ReLU()
    
    def forward(self, x):
        pre = self.pre(x)
        skipped = x + pre
        return self.relu(skipped)
        

class NeuralNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        self.convolution = nn.Sequential(
            nn.Conv2d(119, 256, 3, 1, 1),
            nn.BatchNorm2d(256),
            nn.ReLU(),
        )

        residual = []
        for _ in range(76):
            residual.append(Residual())

        self.residual = nn.Sequential(*residual)

    def forward(self, x):
        x = self.convolution(x)
        x = self.residual(x)
        return x


model = NeuralNetwork().to(device)

print(model)

X = torch.randn(1, 119, 64, 64).to(device)

for _ in range(10):
    result = model(X)

start = time.time()
for _ in range(1000):
    result = model(X)
end = time.time()

print(result)

print(f"That took an average of {(end-start) / 1000} seconds.")

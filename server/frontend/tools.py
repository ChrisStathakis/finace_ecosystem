import torch
import torchvision
from torchvision import transforms, datasets
import matplotlib.pyplot as plt
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

train = datasets.MNIST("datasets/", train=True, download=True,
                       transform=transforms.Compose([transforms.ToTensor(), ])
                       )
test = datasets.MNIST("datasets/", train=False, download=True,
                       transform=transforms.Compose([transforms.ToTensor(), ])
                       )

# trainset = torch.utils.data.DataLoader(train, batch_size=10, shuffle=True)
# testset = torch.utils.data.DataLoader(test, batch_size=10, shuffle=True)


class Net(nn.Module):

    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(28 * 28, 64)
        self.fc2 = nn.Linear(64, 64)
        self.fc3 = nn.Linear(64, 64)
        self.fc4 = nn.Linear(64, 10)


    @staticmethod
    def dataset(data, batch_size=10, shuffle=True):
        return torch.utils.data.DataLoader(data, batch_size=batch_size, shuffle=shuffle)
    
    def trainset(self, optimizer, trainset, epochs=3, ):
        EPOCHS = epochs
        for epoch in range(EPOCHS):
            for data in trainset:
                X, y = data
                self.zero_grad()
                output = self(X.view(-1, 28*28))
                loss = F.nll_loss(output, y)
                loss.backward()  # apply this loss backwards thru the network's parameters
                optimizer.step()
            print(loss)


    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        x = self.fc4(x)
        return F.log_softmax(x)
        return x





net = Net()
loss_function = nn.CrossEntropyLoss()
optimizer = optim.Adam(net.parameters(), lr=0.001)
trainset = net.dataset(data=train)
net.trainset(trainset=trainset, optimizer=optimizer)


"""
EPOCHS = 3

for epoch in range(EPOCHS):
    for data in trainset:
        X, y = data
        net.zero_grad()
        output = net(X.view(-1, 28*28))
        loss = F.nll_loss(output, y)
"""
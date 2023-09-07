import torch
from tqdm.auto import tqdm
import torch.nn as nn
import torch.optim as optim
import time
import torchvision
from model import build_model
from datasets import getdatasets, getdataloaders

seed = 42
torch.manual_seed(seed)
torch.cuda.manual_seed(seed)


epochs=50
def train(model, trainloader, optimizer, criterion):
    print('Training')
    model.train()
    train_running_loss = 0.0
    train_running_correct = 0
    counter = 0
    for i, data in tqdm(enumerate(trainloader), total=len(trainloader)):
        counter += 1
        image, labels = data
        image = image.to(device)
        labels = labels.to(device)
        optimizer.zero_grad()
        outputs = model(image)
        loss = criterion(outputs, labels)
        train_running_loss += loss.item()
        _, preds = torch.max(outputs.data, 1)
        train_running_correct += (preds == labels).sum().item()
        loss.backward()
        optimizer.step()
    
    epoch_loss = train_running_loss / counter
    epoch_acc = 100. * (train_running_correct / len(trainloader.dataset))
    return epoch_loss, epoch_acc

def validate(model, testloader, criterion, class_names):
    print('Validation')
    model.eval()
    valid_running_loss = 0.0
    valid_running_correct = 0
    counter = 0

    with torch.no_grad():
        for i, data in tqdm(enumerate(testloader), total=len(testloader)):
            counter += 1
            image, labels = data
            image = image.to(device)
            labels = labels.to(device)
            outputs = model(image)
            loss = criterion(outputs, labels)
            valid_running_loss += loss.item()
            _, preds = torch.max(outputs.data, 1)
            valid_running_correct += (preds == labels).sum().item()
        
    epoch_loss = valid_running_loss / counter
    epoch_acc = 100. * (valid_running_correct / len(testloader.dataset))
    return epoch_loss, epoch_acc

if __name__ == '__main__':
    dataset_train, dataset_valid, dataset_classes = getdatasets()

    train_loader, valid_loader = getdataloaders(dataset_train, dataset_valid)

    device = ('cuda' if torch.cuda.is_available() else 'cpu')
    model = build_model(
        weights=torchvision.models.EfficientNet_B1_Weights.IMAGENET1K_V1,
        fine_tune=True, 
        num_classes=len(dataset_classes)
    ).to(device)

    optimizer = optim.Adam(model.parameters(), lr=.001)
    criterion = nn.CrossEntropyLoss()


    # Start the training.
    for epoch in range(epochs):
        print(f"[INFO]: Epoch {epoch+1} of {epochs}")
        train_epoch_loss, train_epoch_acc = train(model, train_loader, 
                                                optimizer, criterion)
        valid_epoch_loss, valid_epoch_acc = validate(model, valid_loader,  
                                                    criterion, dataset_classes)
        #fallback for hardware failure
        if epoch %3 == 0:
                torch.save(model, f"./models/models{epoch}.pth")
        time.sleep(2)
    torch.save(model, f"./models/models{epoch}.pth")
    print('TRAINING COMPLETE')
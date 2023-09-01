import torchvision
import torch
from torch.utils.data import DataLoader

train='./input/car_data/car_data/train/'
valid='./input/car_data/car_data/test/'
imgsize=224
batchsize=32
workers=4

def traintransform(imgsize):
    train_transform= torchvision.transforms.Compose([torchvision.transforms.Resize((imgsize, imgsize)),
                                                     torchvision.transforms.RandomHorizontalFlip(p=0.5),
                                                     torchvision.transforms.RandomVerticalFlip(p=0.5),
                                                     torchvision.transforms.RandomGrayscale(p=0.5),
                                                     torchvision.transforms.RandomRotation(90),
                                                     torchvision.transforms.RandomAdjustSharpness(sharpness_factor=4.0, p=0.5),
                                                     torchvision.transforms.RandomPerspective(distortion_scale=1.0, p=0.5),
                                                     torchvision.transforms.RandomPosterize(bits=5, p=0.5),
                                                     torchvision.transforms.ToTensor(),
                                                     torchvision.transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])])
    return train_transform

def validtransform(imgsize):
    valid_transform= torchvision.transforms.Compose([torchvision.transforms.Resize((imgsize, imgsize)),
                                                     torchvision.transforms.ToTensor(),
                                                     torchvision.transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])])
    return valid_transform

def getdatasets():
    dataset_train=torchvision.datasets.ImageFolder(train, transform=(traintransform(imgsize)))
    dataset_valid=torchvision.datasets.ImageFolder(valid, transform=(validtransform(imgsize)))
    return dataset_train, dataset_valid, dataset_train.classes

def getdataloaders(dataset_train, dataset_valid):
    trainloader = DataLoader(dataset_train, batch_size=batchsize, shuffle=True, num_workers=workers)
    validloader=DataLoader(dataset_valid, batch_size=batchsize, shuffle=False, num_workers=workers)
    return trainloader, validloader
import torch.nn as nn
from torchvision import models
def build_model(weights=models.EfficientNet_B1_Weights.IMAGENET1K_V2, fine_tune=True, num_classes=10):
    model= models.efficientnet_b1(weights=models.EfficientNet_B1_Weights.IMAGENET1K_V2)
    for params in model.parameters():
        params.requires_grad = True
    model.classifier[1]=nn.Linear(in_features=1280, out_features=num_classes)
    return model
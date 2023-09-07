import os
import torchvision
import torch
import PIL.Image as Image
from model import build_model

model = build_model(
        weights=torchvision.models.EfficientNet_B1_Weights.IMAGENET1K_V1,
        fine_tune=True, 
        num_classes=196
    )
checkpoint=torch.load('./models/model.pth')
model.load_state_dict(checkpoint['model_state_dict'])
classes = os.listdir("./input/car_data/car_data/train")
mean=[0.485, 0.456, 0.406]
std=[0.229, 0.224, 0.225]
imagetransforms=torchvision.transforms.Compose([torchvision.transforms.ToTensor(), torchvision.transforms.Resize((224, 224), antialias=True), torchvision.transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])])
def predict(model, path, tranformsers, classes):
    model.eval()
    image=Image.open(path)
    image = tranformsers(image).float()
    result = model(image.unsqueeze(0))
    _, think = torch.max(result.data, 1)
    print(classes[think.item()])

# Supra is download.jpg
predict(model, "C:/Users/Manjot Singh/Downloads/download.jpg", imagetransforms,  classes)
print("exit")

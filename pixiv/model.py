import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import PIL
from PIL import Image
import matplotlib.pyplot as plt
import torchvision.transforms as transforms
import torchvision.models as models
from torch.utils.data import DataLoader, TensorDataset
import copy
import os


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

imsize = 224

PIL.Image.MAX_IMAGE_PIXELS = None

# Define the transform to be applied to the image required by resnet50.
loader = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], 
                             [0.229, 0.224, 0.225])
    ])

# Load image and convert it to tensor.
def image_loader(image_name):
    image = Image.open(image_name)
    image = image.convert("RGB")
    # fake batch dimension required to fit network's input dimensions
    image = loader(image).unsqueeze(0)
    return image.to(torch.float)

# Use resnet50 to give a score to a setu.
def setu_score(setu_name, model_name, num_class):
    model = models.resnet50(weights = False)
    num_ftrs = model.fc.in_features
    model.fc = nn.Linear(num_ftrs, num_class)
    model = model.to(device)
    model.load_state_dict(torch.load(model_name))
    tensor = image_loader(setu_name)
    model.eval()
    #tensor = tensor.unsqueeze(0)
    with torch.no_grad():
        tensor = tensor.to(device)
        score = model(tensor)
        if(num_class>2):
            score = nn.functional.softmax(score, dim = 1)
        score = score.cpu().numpy()
    return(score)
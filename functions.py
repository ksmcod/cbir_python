import torch
import torchvision.transforms as transforms
import torchvision.models as models
from PIL import Image
import torch.nn as nn
import os
import numpy as np
from torch.nn.functional import cosine_similarity
import h5py

# Store extracted features for all database images
image_folder = "static/uploads"

# initalize model
vgg16 = models.vgg16()
model_path = "models/vgg16-397923af.pth"

vgg16.load_state_dict(torch.load(model_path))
vgg16.eval()


# Apply transform to images
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])


# Function to extract features
def extract_features(image_path,model,transform):
  image = Image.open(image_path).convert("RGB")
  image = transform(image).unsqueeze(0)

  with torch.inference_mode():
    features = model(image)
    return features.flatten().numpy()






# Function to retrieve images
def retrieve_images(query_image,features="features.h5",model=vgg16,transform=transform, top_k=10):
  query_image_features = extract_features(query_image,model,transform)

  with h5py.File(features, 'w') as f:
    for image_name in os.listdir(image_folder):
      image_path = os.path.join(image_folder, image_name)

      if(os.path.isfile(image_path)):
        image_features = extract_features(image_path, vgg16, transform)
        f.create_dataset(image_name, data=image_features)
        print(image_name)

  similarities = []

  with h5py.File('features.h5', 'r') as f:
    for image_name in f.keys():
      stored_image_features = f[image_name][:]
      # similarity = manhattan_similarity(query_image_features, stored_image_features)
      similarity = cosine_similarity(torch.tensor(query_image_features), torch.tensor(stored_image_features), dim=0)
      similarities.append((image_name, similarity))

  similarities.sort(key=lambda x: x[1], reverse=True)

  return similarities[:top_k]

# print(retrieve_images("features.h5",vgg16,transform,"static/uploads/laptop-8.webp"))
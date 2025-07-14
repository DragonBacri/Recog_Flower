import torch
import torchvision.models as models
from PIL import Image
import torchvision.transforms as transforms

import pandas as pd
# Step 1: Define the model architecture (Must match the trained model)
model = models.resnet50(pretrained=False)
model.fc = torch.nn.Linear(in_features=2048, out_features=102)  # Ensure output matches 102 classes

# Step 2: Load the fine-tuned model weights
model_path = "model/fine_tuned_resnet50.pth"  # Ensure the file is in the correct directory
model.load_state_dict(torch.load(model_path, map_location=torch.device("cpu")))

# Step 3: Set model to evaluation mode
model.eval()
df_labels = pd.read_csv('data/labels.csv')
print("model ok")

def recognize_flower(image):
    # Load the image
    #image_path = image # Replace with your test image
    
    image = image.convert("RGB")  # Ensure 3-channel format

    # Define preprocessing (same as used during training)
    transform = transforms.Compose([
        transforms.Resize((224, 224)),  # Resize to match model input
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    # Apply transformations
    image = transform(image).unsqueeze(0)  # Add batch dimension

    # Perform inference
    with torch.no_grad():
        output = model(image)

    # Convert output to class prediction
    top3_probs, top3_classes = torch.topk(output, 3)

   # Get the class indices from the tensor
    top3_indices = top3_classes.tolist()[0]
    
    # Look up the flower names in order
    top3_Flower = [df_labels.loc[df_labels['id'] == i, 'Flower'].iloc[0] for i in top3_indices]

    return top3_Flower


with open("examples/rose.jpg", "rb") as img_file:
    print(recognize_flower(Image.open(img_file)))
import torch
import torchvision.models as models
from PIL import Image
import torchvision.transforms as transforms

from flask import Flask, request, jsonify
from PIL import Image
import io
import pandas as pd
import os

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


app = Flask(__name__)

# Fonction factice pour reconnaître une fleur
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

    #print("Top 3 class indices:", )
    top3_Flower = df_labels[df_labels['id'].isin(top3_classes.tolist()[0])]['Flower'].to_list()

    return top3_Flower

@app.route("/predict", methods=["POST"])
def predict():
    if "image" not in request.files:
        return jsonify({"error": "No image provided"}), 400

    image = request.files["image"]
    image = Image.open(io.BytesIO(image.read())).convert("RGB")

    flower_name = recognize_flower(image)

    return jsonify({"flower": flower_name})

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug= False)
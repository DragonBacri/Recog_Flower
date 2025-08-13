import torch
import torchvision.models as models
from PIL import Image
import torchvision.transforms as transforms
import google.auth
from google.cloud import storage
from google.auth.exceptions import DefaultCredentialsError
from flask import Flask, request, jsonify
from PIL import Image
import io
import pandas as pd
import sys
import os

# Always add the parent of this file's directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db_engine import get_engine
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

#Step 4 : Mandatory on local (but i need to auth before) and on Google cloud run
try:
        # The client library constructor calls google.auth.default() under the hood.
        # This is the recommended and most common way to authenticate.
        storage_client = storage.Client()

        # If you wanted to get the credentials and project ID explicitly, you could:
        # credentials, project_id = google.auth.default()
        # storage_client = storage.Client(credentials=credentials, project=project_id)

        print(f"Successfully authenticated using project: {storage_client.project}")

except DefaultCredentialsError:
    print(
        "Authentication failed. Please run 'gcloud auth application-default login' "
        "in your terminal to configure your credentials."
    )

#get labels from database
engine = get_engine()
df_labels = pd.read_sql("SELECT  * from dbo.dim_flower", engine)

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

   # Get the class indices from the tensor
    top3_indices = top3_classes.tolist()[0]
    
    # Look up the flower names in order
    top3_Flower = [df_labels.loc[df_labels['id'] == i, 'Flower'].iloc[0] for i in top3_indices]

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
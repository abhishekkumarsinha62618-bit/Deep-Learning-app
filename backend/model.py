import io
import torch
import torchvision.transforms as transforms
from torchvision.models import resnet18, ResNet18_Weights
from PIL import Image

# 1. Load Pretrained ResNet18 Model
weights = ResNet18_Weights.DEFAULT
model = resnet18(weights=weights)
model.eval()

# Get ImageNet class labels
categories = weights.meta["categories"]

# 2. Define Image Preprocessing Pipeline
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    ),
])

def predict_image(image_bytes: bytes) -> dict:
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    tensor = transform(image).unsqueeze(0)

    with torch.no_grad():
        outputs = model(tensor)
        probabilities = torch.nn.functional.softmax(outputs[0], dim=0)

    top3_prob, top3_catid = torch.topk(probabilities, 3)
    
    results = []
    for i in range(top3_prob.size(0)):
        results.append({
            "label": categories[top3_catid[i]],
            "confidence": round(float(top3_prob[i]) * 100, 2)
        })

    return {"predictions": results}
from fastapi import FastAPI, File, UploadFile, HTTPException
from backend.model import predict_image

app = FastAPI(
    title="Deep Learning Image Classification API",
    description="FastAPI Backend serving PyTorch ResNet18 model"
)

@app.get("/")
def health_check():
    return {"status": "online", "message": "Deep Learning API is running!"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if file.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
        raise HTTPException(status_code=400, detail="Invalid image format. Upload JPEG or PNG.")

    contents = await file.read()
    results = predict_image(contents)
    return results
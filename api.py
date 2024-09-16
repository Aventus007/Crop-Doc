from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf

app = FastAPI()

Inception_V3 = tf.keras.models.load_model("InceptionV3_trained\InceptionV3_15Epoch_accuracy_0.9618.h5")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Class_Names = ["Apple___Apple_scab",
 "Apple___Black_rot",
 "Apple___Cedar_apple_rust",
 "Apple___healthy",
 "Cherry_(including_sour)___Powdery_mildew",
 "Cherry_(including_sour)___healthy",
 "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
 "Corn_(maize)___Common_rust_",
 "Corn_(maize)___Northern_Leaf_Blight",
 "Corn_(maize)___healthy",
 "Grape___Black_rot",
 "Grape___Esca_(Black_Measles)",
 "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)",
 "Grape___healthy",
 "Orange___Haunglongbing_(Citrus_greening)",
 "Peach___Bacterial_spot",
 "Peach___healthy",
 "Pepper,_bell___Bacterial_spot",
 "Pepper,_bell___healthy",
 "Potato___Early_blight",
 "Potato___Late_blight",
 "Potato___healthy",
 "Rice__Bacterial leaf blight",
 "Rice__Brown spot",
 "Rice__Leaf smut",
 "Soybean___healthy",
 "Strawberry___Leaf_scorch",
 "Strawberry___healthy",
 "Tomato___Bacterial_spot",
 "Tomato___Early_blight",
 "Tomato___Late_blight",
 "Tomato___Leaf_Mold",
 "Tomato___Septoria_leaf_spot",
 "Tomato___Spider_mites Two-spotted_spider_mite",
 "Tomato___Target_Spot",
 "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
 "Tomato___Tomato_mosaic_virus",
 "Tomato___healthy",
 "Wheat__Healthy",
 "Wheat__septoria",
 "Wheat__stripe_rust"]

async def read_and_process_image(file):
    image_data = await file.read()
    image = Image.open(BytesIO(image_data))

    # Resize and rescale the image
    image = image.resize((224, 224), Image.ANTIALIAS)  # Maintain aspect ratio
    image_data = np.array(image)
    image_data = image_data.astype(np.float32)  # Convert to float32 for rescaling
    image_data /= 255.0  # Rescale by dividing each pixel value by 255

    return image_data

@app.post("/detect")
async def predict(file: UploadFile = File(...)):
    processed_image = await read_and_process_image(file)
    img_batch = np.expand_dims(processed_image, axis=0)
    
    predictions = Inception_V3.predict(img_batch)

    predicted_class = Class_Names[np.argmax(predictions[0])]
    confidence = np.max(predictions[0])

    return {
        "class": predicted_class,
        "confidence": float(confidence)
    }

if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=8000)
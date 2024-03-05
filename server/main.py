from fastapi import FastAPI, UploadFile
import uvicorn
from io import BytesIO
from PIL import Image
import numpy as np
import tensorflow as tf
MODEL= tf.keras.models.load_model("../models/1")
LABELS=['Early Blight', 'Late Blight', 'Healthy' ]

app= FastAPI()
@app.get("/ping")
async def ping():
    return "Hello world"

@app.post("/api/predict")
async def predict(
    file:UploadFile
):
    image= read_file_as_image(await file.read())
    img_batch= np.expand_dims(image, 0)
    print(img_batch.shape)
    predictions= MODEL.predict(img_batch)
    label= LABELS[np.argmax(predictions[0])]
    confidence= round(np.max(predictions[0]) * 100, 2)
    return {
            "label":label,
            "confidence":confidence
    }
    


def read_file_as_image(data)->np.array:
   image= np.array( Image.open(BytesIO(data)))
   return image
if __name__=="__main__":
    uvicorn.run(app, host='localhost', port=8888)
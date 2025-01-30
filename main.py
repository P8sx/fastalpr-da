from fastapi import FastAPI, File, UploadFile, Form
from fast_alpr import ALPR
from PIL import Image
import io
import os
import numpy as np
app = FastAPI()

alpr = ALPR(
    detector_model=os.getenv("DETECTOR_MODEL", "yolo-v9-t-384-license-plate-end2end"),
    ocr_model=os.getenv("OCR_MODEL", "european-plates-mobile-vit-v2-model"),
)


@app.post("/recognize")
async def recognize_plate(
    file: UploadFile = File(...),
    crop_x: int = Form(None), 
    crop_y: int = Form(None),  
    crop_width: int = Form(None),
    crop_height: int = Form(None),
):
    try:
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data))
        
        if crop_x is not None and crop_y is not None and crop_width != 0 and crop_height != 0:
            image = image.crop((crop_x, crop_y, crop_x + crop_width, crop_y + crop_height))
    
        image_np = np.array(image)

        results = alpr.predict(image_np)
        
        return {"plates": results}
    except Exception as e:
        return {"error": str(e)}
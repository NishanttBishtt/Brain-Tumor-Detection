from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

import tensorflow as tf
import numpy as np
import cv2
import imutils
import io
import os
import uuid
from PIL import Image

from gradcam import (
    make_gradcam_heatmap,
    save_gradcam
)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # or ["http://localhost:8501"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Create folders if they don't exist
os.makedirs("uploads", exist_ok=True)
os.makedirs("gradcam_outputs", exist_ok=True)
os.makedirs("segmentation_outputs", exist_ok=True)

# Serve Grad-CAM images
app.mount(
    "/gradcam",
    StaticFiles(directory="gradcam_outputs"),
    name="gradcam"
)
app.mount(
    "/segmentation",
    StaticFiles(directory="segmentation_outputs"),
    name="segmentation"
)

model = tf.keras.models.load_model(
    "brain_tumor_model.keras"
)
segmentation_model = tf.keras.models.load_model(
    "tumor_segmentation.keras",
    compile=False
)

class_names = [
    "glioma",
    "meningioma",
    "notumor",
    "pituitary"
]
# preprocessing

# NLM DENOISING
def apply_nlm(image):
    denoised = cv2.fastNlMeansDenoisingColored(
        image,
        None,
        h=10,
        hColor=10,
        templateWindowSize =7,
        searchWindowSize=21
    )
    return denoised

#cropping
def crop_image(image):

    img_gray = cv2.cvtColor(
        image,
        cv2.COLOR_RGB2GRAY
    )

    img_blur = cv2.GaussianBlur(
        img_gray,
        (5, 5),
        0
    )

    img_thresh = cv2.threshold(
        img_blur,
        45,
        255,
        cv2.THRESH_BINARY
    )[1]

    img_thresh = cv2.erode(
        img_thresh,
        None,
        iterations=2
    )

    img_thresh = cv2.dilate(
        img_thresh,
        None,
        iterations=2
    )

    contours = cv2.findContours(
        img_thresh.copy(),
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_NONE
    )

    contours = imutils.grab_contours(
        contours
    )

    c = max(
        contours,
        key=cv2.contourArea
    )

    extLeft = tuple(
        c[c[:, :, 0].argmin()][0]
    )

    extRight = tuple(
        c[c[:, :, 0].argmax()][0]
    )

    extTop = tuple(
        c[c[:, :, 1].argmin()][0]
    )

    extBottom = tuple(
        c[c[:, :, 1].argmax()][0]
    )

    new_img = image[
        extTop[1]:extBottom[1],
        extLeft[0]:extRight[0]
    ]

    return new_img

def generate_segmentation(image, base_url):
    # image is the original RGB image as a NumPy array
    original_height, original_width = image.shape[:2]

    # Match U-Net training preprocessing
    seg_image = cv2.resize(
        image,
        (256, 256),
        interpolation=cv2.INTER_LINEAR
    )

    seg_image = seg_image.astype(np.float32) / 255.0
    seg_image = np.expand_dims(seg_image, axis=0)

    # Predict mask
    prediction = segmentation_model.predict(
        seg_image,
        verbose=0
    )[0, :, :, 0]

    # Convert probabilities into a binary mask
    mask = (prediction >= 0.5).astype(np.uint8) * 255

    # Resize mask back to original image dimensions
    mask = cv2.resize(
        mask,
        (original_width, original_height),
        interpolation=cv2.INTER_NEAREST
    )

    # Create a red overlay on the original MRI
    overlay = image.copy()
    tumor_pixels = mask > 127

    red = np.zeros_like(image)
    red[:, :, 0] = 255

    overlay[tumor_pixels] = (
        0.5 * image[tumor_pixels]
        + 0.5 * red[tumor_pixels]
    ).astype(np.uint8)

    # Save unique filenames
    mask_filename = f"{uuid.uuid4().hex}_mask.png"
    overlay_filename = f"{uuid.uuid4().hex}_overlay.jpg"

    mask_path = os.path.join(
        "segmentation_outputs",
        mask_filename
    )
    overlay_path = os.path.join(
        "segmentation_outputs",
        overlay_filename
    )

    Image.fromarray(mask).save(mask_path)
    Image.fromarray(overlay).save(overlay_path)

    return {
        "segmentation_mask_url": (
            f"{base_url}segmentation/{mask_filename}"
        ),
        "segmentation_overlay_url": (
            f"{base_url}segmentation/{overlay_filename}"
        )
    }

@app.post("/predict")
async def predict(
    request: Request,
    file: UploadFile = File(...)
):

    try:

        contents = await file.read()

        upload_path = os.path.join(
            "uploads",
            file.filename
        )

        with open(upload_path, "wb") as f:
            f.write(contents)

        image = Image.open(
            io.BytesIO(contents)
        ).convert("RGB")

        original_image = np.array(image)

        # Generate segmentation using the original image
        base_url = str(request.base_url)

        segmentation_results = generate_segmentation(
            original_image,
            base_url
        )

        # Continue the existing classification preprocessing
        image = apply_nlm(original_image.copy())
        
        image = crop_image(image)

        image = cv2.resize(
            image,
            (240, 240)
        )

        image = image.astype(
            np.float32
        )

        image = np.expand_dims(
            image,
            axis=0
        )

# prediction

        pred = model.predict(
            image,
            verbose=0
        )

        pred_idx = np.argmax(pred)

        pred_class = class_names[
            pred_idx
        ]

        confidence = float(
            np.max(pred)
        )

        probabilities = {

            class_names[i]:
            float(pred[0][i])

            for i in range(
                len(class_names)
            )
        }
        print("Image type:", type(image))
        print("Image shape:", image.shape)

        heatmap = make_gradcam_heatmap(
            image,
            model,
            "top_conv"
        )

        output_filename = f"{uuid.uuid4().hex}.jpg"

        output_path = os.path.join(
            "gradcam_outputs",
            output_filename
        )
        base_url = str(request.base_url)

        gradcam_url = (
            f"{base_url}gradcam/{output_filename}"
        )

        save_gradcam(
            upload_path,
            heatmap,
            output_path
        )

        return JSONResponse({

            "prediction":
                pred_class,

            "confidence":
                round(
                    confidence * 100,
                    2
                ),

            "probabilities":
                probabilities,

            "gradcam_url": gradcam_url,
            **segmentation_results

        })

    except Exception as e:

        return JSONResponse(
            status_code=500,
            content={
                "error": str(e)
            }
        )
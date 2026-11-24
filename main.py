# Dependencies
    #fastAPI
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
    #Uvicorn
#uv
    #Docker (nrq'd)
    #opencv
import cv2 as cv
    #numpy
import numpy as np

#fastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://RAFM-EBSD-ITP5.github.io"],
    allow_credentials=False,
    allow_methods=["POST", "GET", "OPTIONS"],
    allow_headers=["*"],
)

@app.post("/img_inbox")
#should be either .tif/.png
async def recv_img(file: UploadFile = File(...)):
    data = await file.read()
    image = cv.imdecode(np.frombuffer(data, np.uint8), cv.IMREAD_GRAYSCALE) #decode image from tiff/png to 8bit binary arr
    """
    if image is None:
        raise HTTPException(400, "Could not decode image (expected .tif or .png)") # send http error if image cannot be decoded
    """
    active_img = make_green(image) #makes image green pixels only
    ok, buffer = cv.imencode(".png", active_img) #encodes binary array (buffer) as image
    img_send = buffer.tobytes() # converts binary array to image bytes
    return Response(content=img_send, media_type="image/png") #send png image to web source

def make_green(image):
    output = np.zeros((*image.shape, 3), dtype=np.uint8)
    output[:, :, 1] = image
    return output
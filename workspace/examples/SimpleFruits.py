'''
Not tested yet
'''


from roboflow import Roboflow
#rf = Roboflow(api_key="K3sks4IiHf1jC7nMw6YN")
#project = rf.workspace().project("simplefruits")
#model = project.version(1).model

# infer on a local image
#print(model.predict("your_image.jpg", confidence=40, overlap=30).json())

# visualize your prediction
# model.predict("your_image.jpg", confidence=40, overlap=30).save("prediction.jpg")

# infer on an image hosted elsewhere
# print(model.predict("URL_OF_YOUR_IMAGE", hosted=True, confidence=40, overlap=30).json())

# load config
import cv2 as cv
import base64
import numpy as np
import requests

ROBOFLOW_API_KEY = "K3sks4IiHf1jC7nMw6YN"
ROBOFLOW_MODEL = "simplefruits/1"  # eg xx-xxxx--#
ROBOFLOW_SIZE = 416

upload_url = "".join([
    "https://detect.roboflow.com/",
    ROBOFLOW_MODEL,
    "?access_token=",
    ROBOFLOW_API_KEY,
    "&format=image",
    "&stroke=5"
])

print(upload_url)

video = cv.VideoCapture(0)

# Check if camera opened successfully
if (video.isOpened()):
    print("successfully opening video stream or file")


# Infer via the Roboflow Infer API and return the result
def infer():
    # Get the current image from the webcam
    ret, frame = video.read()

    # Resize (while maintaining the aspect ratio)
    # to improve speed and save bandwidth
    height, width, channels = frame.shape
    scale = ROBOFLOW_SIZE / max(height, width)
    img = cv.resize(frame, (round(scale * width), round(scale * height)))

    # Encode image to base64 string
    retval, buffer = cv.imencode('.jpg', img)
    img_str = base64.b64encode(buffer)

    # Get prediction from Roboflow Infer API
    upload_url = "https://detect.roboflow.com/simplefruits/1?access_token=K3sks4IiHf1jC7nMw6YN&format=image&stroke=5"
    resp = requests.post(upload_url, data=img_str, headers={
        "Content-Type": "application/x-www-form-urlencoded"
    }, stream=True).raw


    # Parse result image
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv.imdecode(image, cv.IMREAD_COLOR)

    return image


# Main loop; infers sequentially until you press "q"
while video.isOpened():
    # On "q" keypress, exit
    key = cv.waitKey(5)
    if key == ord("q"):
        break

    # Synchronously get a prediction from the Roboflow Infer API
    image = infer()
    # And display the inference results
    cv.imshow('image', image)

# Release resources when finished
video.release()
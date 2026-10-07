'''
Not tested yet
'''


from roboflow import Roboflow
import cv2

rf = Roboflow(api_key="K3sks4IiHf1jC7nMw6YN")
project = rf.workspace().project("simplefruits")
model = project.version(1).model


# define a video capture object
vid = cv2.VideoCapture(1)
while(True):
    ret, frame = vid.read()
    cv2.imshow('Original', frame)
    image = frame

    # infer on a local image
    predictions = model.predict(frame, confidence=40, overlap=30).json()

    for bounding_box in predictions['predictions']:
        x0 = bounding_box['x'] - bounding_box['width'] / 2
        x1 = bounding_box['x'] + bounding_box['width'] / 2
        y0 = bounding_box['y'] - bounding_box['height'] / 2
        y1 = bounding_box['y'] + bounding_box['height'] / 2

        start_point = (int(x0), int(y0))
        end_point = (int(x1), int(y1))
        cv2.rectangle(image, start_point, end_point, color=(255, 0, 0), thickness=1)

        cv2.putText(
            image,
            bounding_box["class"],
            (int(x0), int(y0) - 10),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=0.6,
            color=(255, 255, 255),
            thickness=2
        )
    cv2.imshow('predictions', image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# After the loop release the cap object
vid.release()

# visualize your prediction
# model.predict("your_image.jpg", confidence=40, overlap=30).save("prediction.jpg")

# infer on an image hosted elsewhere
# print(model.predict("URL_OF_YOUR_IMAGE", hosted=True, confidence=40, overlap=30).json())
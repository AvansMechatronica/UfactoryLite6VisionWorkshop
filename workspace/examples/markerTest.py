import cv2
# import the opencv library
import keyboard  # load keyboard package
import time
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # allow running this file directly
from libraries.vision.usbCamera import usbCamera
from libraries.vision.markers_detection import *
from libraries.vision.enums import *

camera_index = 0

def main():
    camera = usbCamera(camera_index, rotate_frame= True)

    while True:
        if keyboard.is_pressed("q"):  # returns True if "q" is pressed
            camera.end();
            break

        if keyboard.is_pressed("p"):  # returns True if "q" is pressed
            image = camera.take_photo(display_photo=False);
            result = False
            result, crop_image = extract_img_markers(image, workspace_ratio=1.0)
            if result:
                cv2.imshow("Crop", crop_image)
            else:
                print("Unable to extract image markers")

            result, marker_image = draw_markers(image, workspace_ratio=1.0)
            if result:
                cv2.imshow("Marker", marker_image)
            else:
                print("Unable to draw image markers")

            cv2.waitKey(1)
            time.sleep(1)

if __name__ == "__main__":
    main()
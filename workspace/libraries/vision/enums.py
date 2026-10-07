#from enum import Enum, unique
import cv2



# -- Text Display
RED = (0, 0, 255)
PURPLE = (255, 0, 255)
ORANGE = (0, 127, 255)
GREEN = (0, 255, 0)
BLUE = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
#font = cv2.FONT_HERSHEY_SIMPLEX
font_scale_big = 2.0
font_scale_normal = 0.7
thickness_big = 3
thickness_small = 2


# Command list

class Command:
    GET_OBJECT_POS = 1
    GET_OBJECT_RELATIVE_POS = 2


# Values for HSV threshold

class ColorHSV:
    """
    MIN HSV, MAX HSV, Invert Hue (bool)
    """
    BLUE = [90, 50, 85], [125, 255, 255], False
    RED = [15, 80, 75], [170, 255, 255], True
    GREEN = [40, 60, 75], [85, 255, 255], False
    ANY = [0, 50, 100], [179, 255, 255], False


# Values use for HS'V thresholding
class ColorHSVPrime:
    """
    MIN HSV, MAX HSV, Invert Hue (bool)
    """
    BLUE = [90, 70, 100], [115, 255, 255], False
    RED = [15, 70, 100], [170, 255, 255], True
    GREEN = [40, 70, 100], [85, 255, 255], False
    ANY = [0, 70, 140], [179, 255, 255], False


# Different object types handle by the API. The value corresponds to the object's number of sides
class ObjectType:
    SQUARE = 4
    CIRCLE = -1
    ANY = 0


class MorphoType:
    ERODE = cv2.MORPH_ERODE
    DILATE = cv2.MORPH_DILATE
    OPEN = cv2.MORPH_OPEN
    CLOSE = cv2.MORPH_CLOSE


class KernelType():
    RECT = cv2.MORPH_RECT
    ELLIPSE = cv2.MORPH_ELLIPSE
    CROSS = cv2.MORPH_CROSS

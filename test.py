from math import dist
import cv2 as cv
from time import sleep
from display import Display

image = Display.update_called_numbers_display("55")

cv.imshow(Display.window_name, image)
cv.waitKey()
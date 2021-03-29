from pytesseract import image_to_boxes, Output
import cv2 as cv

img = cv.imread("cut_book.jpg")
config ="outputbase digits"
boxes = image_to_boxes(img, output_type=Output.DICT, config=config)

print(boxes["char"])
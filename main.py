import cv2 as cv
from time import sleep

from page_extractor import Page_extractor
from house import House

called_numbers = ['7', '13','52','0', '83', '9', '0', '20', '0', '48', '58', '64', '0', '0', "37"]

img_path = "output_with_numbers/1.png"

def extract_houses():  
    img_array = Page_extractor.house_extractor("bingo_book.jpg")
    return img_array
img_array = extract_houses()

house_array = Page_extractor.get_house_as_array(img_array[0])

game1 = House(house_array)
game1.check_all(called_numbers)
import cv2 as cv
from time import sleep

from page_extractor import Page_extractor

img_path = "output_with_numbers/1.png"
def extract_houses():  
    Page_extractor.house_extractor("bingo_book.jpg")
    sleep(1)

whole_game_array = Page_extractor.get_whole_game_as_array(img_path)

for elem in whole_game_array:
    print(elem)
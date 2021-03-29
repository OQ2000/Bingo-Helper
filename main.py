import cv2 as cv
from time import sleep

from page import Page
from game import Game
from display import Display

called_numbers = []

img_path = "bingo_book.jpg"

page1 = Page("page1")

page1.extract_houses(img_path)

for house in page1.list_houses:
    for House in house.house:
        print(House)

while True:
    called_numbers.append(input("Called: "))
    page1.check_all_houses(called_numbers)
    image = Display.update_called_numbers_display(called_numbers)

    cv.imshow(Display.window_name, image)
    cv.waitKey(1)
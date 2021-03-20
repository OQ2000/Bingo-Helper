from math import floor, ceil
import cv2 as cv

class Display:
    window_name = 'Called_numbers'
    path = "psd/array_numbers.jpg"
    image = cv.imread(path)
    @classmethod
    def update_called_numbers_display(cls, called_numbers):
        def get_pos_nums(num):
            num = int(num)-1
            # if num != 1:
            #     num = num 
            pos_nums = []
            while num != 0:
                pos_nums.append(num % 10)
                num = num // 10
            while len(pos_nums) != 2:
                pos_nums.insert(1,0)
            return pos_nums
        for called_number in called_numbers:
            digits = get_pos_nums(called_number)
            top_left = ((digits[0]) * 50,digits[1] * 50)
            bottom_right = (top_left[0] + 50,top_left[1] + 50)
            # Blue color in BGR 
            color = (255, 0, 0) 
            # Line thickness of 2 px 
            thickness = 2
            image = cv.rectangle(cls.image, top_left, bottom_right, color, thickness)
        return image
            # cv.imshow(cls.window_name, image)
            # cv.waitKey(200)

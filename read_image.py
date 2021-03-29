from pytesseract import image_to_string
import cv2 as cv
import numpy as np

class Read_image:
    @classmethod
    def read_image(cls, img):
        custom_config = r'--oem 1 --psm 8 outputbase digits'
        txt = image_to_string(img, config=custom_config)
        # cv.imshow("Tess Img", img)
        # Read_image.test(txt)
        # cv.waitKey(500)
        # cv.destroyAllWindows()
        return txt

    @classmethod
    def test(cls, txt):
        img = np.zeros((50,50,3), np.uint8)
        # Write some Text
        font                   = cv.FONT_HERSHEY_SIMPLEX
        bottomLeftCornerOfText = (10,40)
        fontScale              = 1
        fontColor              = (255,255,255)
        lineType               = 2

        cv.putText(img,txt, 
            bottomLeftCornerOfText, 
            font, 
            fontScale,
            fontColor,
            lineType)

        #Display the image
        cv.imshow("img",img)
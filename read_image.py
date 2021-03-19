from pytesseract import image_to_string

class Read_image:
    @classmethod
    def read_image(cls, img):
        custom_config = r'--oem 3 --psm 6 outputbase digits'
        txt = image_to_string(img, config=custom_config)
        return txt

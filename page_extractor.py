import cv2 as cv
import numpy as np
from read_image import Read_image

class Page_extractor:
    @classmethod
    def sort_contours(cls, cnts, method="top-to-bottom"):
        # initialize the reverse flag and sort index
        reverse = False
        i = 0

        # handle if we need to sort in reverse
        if method == "right-to-left" or method == "bottom-to-top":
            reverse = True

        # handle if we are sorting against the y-coordinate rather than
        # the x-coordinate of the bounding box
        if method == "top-to-bottom" or method == "bottom-to-top":
            i = 1

        # construct the list of bounding boxes and sort them from top to
        # bottom
        boundingBoxes = [cv.boundingRect(c) for c in cnts]
        (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
                                            key=lambda b: b[1][i], reverse=reverse))

        # return the list of sorted contours and bounding boxes
        return (cnts, boundingBoxes)

    #Functon for extracting the games from the page
    @classmethod
    def house_extractor(cls, img_for_box_extraction_path):
        print("Reading image..")
        img = cv.imread(img_for_box_extraction_path, 0)  # Read the image
        # img = img[...,:3]

        (thresh, img_bin) = cv.threshold(img, 128, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)  # Thresholding the image
        img_bin = 255-img_bin  # Invert the image

        # print("Storing binary image to Images/Image_bin.jpg..")
        # cv.imwrite("Images/Image_bin.jpg",img_bin)

        print("Applying Morphological Operations..")
        # Defining a kernel length
        kernel_length = np.array(img).shape[1]//40
        
        # A verticle kernel of (1 X kernel_length), which will detect all the verticle lines from the image.
        verticle_kernel = cv.getStructuringElement(cv.MORPH_RECT, (1, kernel_length))
        # A horizontal kernel of (kernel_length X 1), which will help to detect all the horizontal line from the image.
        hori_kernel = cv.getStructuringElement(cv.MORPH_RECT, (kernel_length, 1))
        # A kernel of (3 X 3) ones.
        kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))

        # Morphological operation to detect verticle lines from an image
        img_temp1 = cv.erode(img_bin, verticle_kernel, iterations=3)
        verticle_lines_img = cv.dilate(img_temp1, verticle_kernel, iterations=3)
        # cv.imwrite("Images/verticle_lines.jpg",verticle_lines_img)

        # Morphological operation to detect horizontal lines from an image
        img_temp2 = cv.erode(img_bin, hori_kernel, iterations=3)
        horizontal_lines_img = cv.dilate(img_temp2, hori_kernel, iterations=3)
        # cv.imwrite("Images/horizontal_lines.jpg",horizontal_lines_img)

        # Weighting parameters, this will decide the quantity of an image to be added to make a new image.
        alpha = 0.5
        beta = 1.0 - alpha
        # This function helps to add two image with specific weight parameter to get a third image as summation of two image.
        img_final_bin = cv.addWeighted(verticle_lines_img, alpha, horizontal_lines_img, beta, 0.0)
        img_final_bin = cv.erode(~img_final_bin, kernel, iterations=2)
        (thresh, img_final_bin) = cv.threshold(img_final_bin, 128, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)

        # For Debugging
        # Enable this line to see verticle and horizontal lines in the image which is used to find boxes
        # print("Binary image which only contains boxes: Images/img_final_bin.jpg")
        # cv.imwrite("Images/img_final_bin.jpg",img_final_bin)
        # Find contours for image, which will detect all the boxes
        contours, hierarchy = cv.findContours(img_final_bin, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        # Sort all the contours by top to bottom.
        (contours, boundingBoxes) = Page_extractor.sort_contours(contours, method="top-to-bottom")
        # print("Output stored in Output directiory!")
        idx = 0
        img_array = []
        for c in contours:
            # Returns the location and width,height for every contour
            x, y, w, h = cv.boundingRect(c)

            # If the box height is greater then 20, width is > 80, then only save it as a box in "cropped/" folder.
            if (w > 80 and h > 20) and w > 3*h:
                idx += 1
                new_img = img[y:y+h, x:x+w]
                img_array.append(new_img)
                # cv.imwrite("output_with_numbers/" + str(idx) + '.png', new_img)
        return img_array
    @classmethod
    def detect_box(cls, image,line_min_width=41,min_val=120,max_val=255):
        # gray_scale=cv.cvtColor(image,cv.COLOR_BGR2GRAY) # Changed to using image in threshold due to path errors
        th1,img_bin=cv.threshold(image,min_val,max_val,cv.THRESH_BINARY)
        kernal_h=np.ones((1,line_min_width), np.uint8)
        kernal_v=np.ones((line_min_width,1), np.uint8)
        img_bin_h=cv.morphologyEx(~img_bin, cv.MORPH_OPEN, kernal_h)
        img_bin_v=cv.morphologyEx(~img_bin, cv.MORPH_OPEN, kernal_v)
        img_bin_final=img_bin_h|img_bin_v
        final_kernel=np.ones((3,3), np.uint8)
        img_bin_final=cv.dilate(img_bin_final,final_kernel,iterations=1)
        ret, labels, rects ,centroids = cv.connectedComponentsWithStats(~img_bin_final, connectivity=8, ltype=cv.CV_32S)
        return rects

    @classmethod
    def group_rectangles(cls, rectangles):
        rectangles, weights = cv.groupRectangles(np.array(rectangles).tolist(), groupThreshold=1, eps=0.5)
        return rectangles

    @classmethod
    def get_individual_boxes(cls, img, row="top"):
        '''
        row=(top,middle,bottom)
        '''
        # game = cv.imread(img_path)  # Read the image
        # game = game[...,:3]
        rects = Page_extractor.detect_box(img)
        retangles = []
        for x,y,w,h,area in rects[2:]:
            rect = [x,y,w,h]
            retangles.append(rect)
            retangles.append(rect)
        retangles = Page_extractor.group_rectangles(retangles)
        
        cur_row = []
        for x,y,w,h in retangles:
            if row == "top":
                if y < 20:
                    cur_row.append((x,y,w,h))
                    cur_row.append((x,y,w,h))
            if row == "middle":
                if y < 90 and y > 10:
                    cur_row.append((x,y,w,h))
                    cur_row.append((x,y,w,h))
            if row == "bottom":
                if y > 91:
                    cur_row.append((x,y,w,h))
                    cur_row.append((x,y,w,h))

        def myFunc(elem):
            return elem[0]
        cur_row.sort(key=myFunc)
        cur_row = Page_extractor.group_rectangles(cur_row)
        # print("Sorted: \n", cur_row)
        # idx = 0
        # boxes = []
        # for x,y,w,h in cur_row:
        #     idx += 1
        #     new_img = game[y:y+h, x:x+w]
        #     # Need to implement saving these in storage and reading them using tesseract
        #     boxes.append(new_img)

        #     # cv.imwrite("boxes/"+str(idx) + '.png', new_img)
        #     # cv.rectangle(game,(x,y),(x+w,y+h),(0,255,0),2)
        return cur_row

    @classmethod
    def get_house_as_array(cls, img): # Swapped to passing img in instead of saving and reading for no reason
        methods = ["top", "middle", "bottom"]
        whole_game = []
        for i in range(3):
            boxes = Page_extractor.get_individual_boxes(img, row=methods[i])
            new_str = []
            for x,y,w,h in boxes:
                new_img = img[y:y+h, x:x+w]
                contours, hierarchy = cv.findContours(new_img,cv.RETR_TREE,cv.CHAIN_APPROX_NONE)
                if len(contours) > 3:
                    s = Read_image.read_image(new_img)
                    s = s.strip()
                    if s != "":
                        new_str.append(s)
                else:
                    new_str.append("0")
            whole_game.append(new_str)
        return whole_game
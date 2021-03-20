from page_extractor import Page_extractor
from house import House

class Page:
    name = ""
    list_houses = []

    def __init__(self, name, houses=[]):
        self.name = name
        self.list_houses = houses
    
    def extract_houses(self, img_path):
        self.list_houses = []
        array_of_house_arrays_as_string = Page_extractor.house_extractor(img_path)
        houses = []
        for i in range(len(array_of_house_arrays_as_string)):
            
            house = House(array_of_house_arrays_as_string[i])
            houses.append(house)

        self.list_houses = houses
    
    def check_all_houses(self, called_numbers):
        for i in range(len(self.list_houses)):
            rtn = self.list_houses[i].check_all(called_numbers)
            if rtn == 1:
                print("Line Found on {} in house {}".format(self.name, i + 1))
            if rtn == 2:
                print("Double Line Found on {} in house {}".format(self.name, i + 1))
            if rtn == 3:
                print("Full House Found on {} in house {}".format(self.name, i + 1))
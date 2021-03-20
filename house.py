class House:
    house = []
    def __init__(self, house):
        self.house = house

    @classmethod
    def check_house(cls, house, called_numbers, rtn_type="bool"):
        '''
        called_numbers needs to be a list of strings\n
        rtn:\n
            bool -- returns true if there is a line\n
            line -- returns any full lines\n
            total -- returns how many full lines there are
            returns None if none found
        '''
        no_of_lines = 0
        for line in house:
            num_need_to_find = len(line)
            for elem in line:
                if elem in called_numbers or elem == "0":
                    num_need_to_find = num_need_to_find - 1
            if num_need_to_find == 0:
                if rtn_type == "bool":
                    return True# line is true
                elif rtn_type == "line":
                    return line
                if rtn_type == "total":
                    no_of_lines = no_of_lines + 1
        if rtn_type == "total":
            if no_of_lines == 0:
                return None
            else:
                return no_of_lines

    def check_for_line(self, called_numbers):
        if House.check_house(self.house, called_numbers):
            print("Line Found")

    def check_for_double_line(self, called_numbers):
        if House.check_house(self.house, called_numbers, rtn_type="total") >= 2:
            print("Double Line Found")

    def check_for_full_house(self, called_numbers):
        if House.check_house(self.house, called_numbers, rtn_type="total") >= 3:
            print("Full House Found")

    def check_all(self, called_numbers):
        rtn = House.check_house(self.house, called_numbers, rtn_type="total")
        return rtn

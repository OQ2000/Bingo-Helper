class Game:
    game_state = "play" 
    called_numbers = []
    playing_for = "line" # can be line, double, house
    
    def in_play(self, houses):
        # take in numbers and check to see if youve won
        pass
    
    def new_number_called(self, number):
        self.called_numbers.append(number)
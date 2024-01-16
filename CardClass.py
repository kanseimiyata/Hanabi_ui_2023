class Card:
    
    def __init__(self,number, color):##constructor
        self.number = number
        self.color = color
        
    def set_contents(self, num,clr):##rewrite contents
        self.number = num
        self.color = clr

    def set_number(self, num):## rewrite only number
        self.number = num
    
    def set_color(self,clr):##rewrite only color
        self.color = clr
        
    def print_card(self):
        print(self.number,self.color, end="  ")
        ##print(self.color)
### BoardClass.py 

from CardClass import Card
from macro import PLAYERNUMBER
from macro import HANDNUM
from macro import SEARCHDEPTH
from macro import color_list
from macro import player

class Board:
    
    def __init__(self):
        self.phand = [[[Card(0,"_") for i in range(HANDNUM)] for i in range(PLAYERNUMBER + 1)] for i in range(SEARCHDEPTH+1)]
        self.prov_hand_PO = [[[Card(i+1,color_list[i]) for i in range(5)] for i in range(HANDNUM)] for i in range(PLAYERNUMBER + 1)] 
        self.discard_count = 0##12/27追加　廃棄カウントのための一時的変数
        self.alldiscarded_list = []##12/27追加 全廃棄されたカードのリスト
        self.deck  = [] 
        self.discarded_set = []
        self.visible_cards_set = [[3,2,2,2,1] for i in range(len(color_list))]
        self.fireworks = [Card(0,"W"),Card(0,"R"),Card(0,"B"),Card(0,"Y"),Card(0,"G")]
        self.played_card = Card(0, "_")
        self.discarded_card = Card(0, "_")
        self.red_token = 0
        self.blue_token = 8
        
    def alldiscarded_check(self,check_card):##12/27追加
        if check_card.number==5:##5は1枚しかないので捨てられた段階で全廃棄扱い
            self.alldiscarded_list.append(check_card)
        for i in self.discarded_set:
            if i.color==check_card.color and i.number==check_card.number:##同じカードが何枚捨てられたか数える
                self.discard_count=self.discard_count+1
        if check_card.number==1 and self.discard_count==3:##1が3枚捨てられていたら全廃棄扱い
            self.alldiscarded_list.append(check_card)
        elif check_card.number!=1 and self.discard_count==2:##それ以外が2枚捨てられていたら全廃棄扱い
            self.alldiscarded_list.append(check_card)
        self.discard_count=0
        
        


    def deck_init(self):

        for i in range(5):
            for j in range(3):
                self.deck.append(Card(1,color_list[i]))
            for j in range(3):
                for _k in range(2):
                    self.deck.append(Card(2+j,color_list[i]))
            self.deck.append(Card(5,color_list[i]))
            
    def play_processing(self):
        
        succeeded_flag = False
        for i in range(5):
            ###num and color are checked
            if self.played_card.color != self.fireworks[i].color:
                continue
            elif self.played_card.number == self.fireworks[i].number + 1:
                self.fireworks[i].number += 1
                succeeded_flag = True
                if self.fireworks[i].number == 5 and self.blue_token < 8:
                    self.blue_token += 1

        if succeeded_flag == False:
            self.red_token += 1
            self.discarded_set.append(self.played_card)
            self.alldiscarded_check(self.played_card)
        
    def discard_processing(self):

        self.discarded_set.append(self.discarded_card)
        self.alldiscarded_check(self.discarded_card)
        if self.blue_token < 8:
           self.blue_token += 1





        
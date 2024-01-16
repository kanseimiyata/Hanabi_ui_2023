import random
import PlayerClass
from PlayerClass import Player
from BoardClass import Board
from macro import color_list
from macro import player
from macro import PLAYERNUMBER
from macro import HANDNUM
from macro import hand_index
from macro import color_to_tell_list

class DecideAgent(Player):

    def __init__(self,player_index,is_bot):
        super().__init__(player_index,is_bot)
        self.opponent_index=0
        self.act_index=0




    def choice_act(self):
        if self.player_index==1:##opponentの設定
            self.opponent_index=2
        elif self.player_index==2:
            self.opponent_index=1
        provmax=[5] * HANDNUM
        for i in range(HANDNUM):##各手札の最大値の確定(0,2,3,4,5→5)
            for j in range(5):
                if player[self.player_index].seeing_board.prov_hand_PO[self.player_index][i][j].number!=0:
                    provmax[i]=player[self.player_index].seeing_board.prov_hand_PO[self.player_index][i][j].number       
        colorkeeper='_'
        numberkeeper=0
        for i in range(HANDNUM):#色を一つに絞り込めた場合のみphandに代入
            for j in range(5):
                if player[self.player_index].seeing_board.prov_hand_PO[self.player_index][i][j].color!='_' and colorkeeper=='_':
                    colorkeeper=player[self.player_index].seeing_board.prov_hand_PO[self.player_index][i][j].color
                elif player[self.player_index].seeing_board.prov_hand_PO[self.player_index][i][j].color!='_' and colorkeeper!='_':
                    colorkeeper='_'
                    break
            player[self.player_index].seeing_board.phand[0][self.player_index][i].color=colorkeeper#色を一つに絞り込めた場合のみ代入
            colorkeeper='_' ##色の確定
        for i in range(HANDNUM):#数字を一つに絞り込めた場合のみphandに代入
            for j in range(5):
                if player[self.player_index].seeing_board.prov_hand_PO[self.player_index][i][j].number!=0 and numberkeeper==0:
                    numberkeeper=player[self.player_index].seeing_board.prov_hand_PO[self.player_index][i][j].number
                elif player[self.player_index].seeing_board.prov_hand_PO[self.player_index][i][j].number!=0 and numberkeeper!=0:
                    numberkeeper=0
                    break
            player[self.player_index].seeing_board.phand[0][self.player_index][i].number=numberkeeper
            numberkeeper=0 ##数字の確定
        

        act1flag=0
        self.act_num=5  ##ランダム廃棄 random discard


     





        for i in range(HANDNUM):#相手自身がまだ知らないカードがあったら情報提供、右のカードから優先？
            print(player[self.opponent_index].seeing_board.phand[0][self.opponent_index][i].color, player[self.player_index].seeing_board.phand[0][self.opponent_index][i].color)
            if (player[self.opponent_index].seeing_board.phand[0][self.opponent_index][i].color!=player[self.player_index].seeing_board.phand[0][self.opponent_index][i].color\
            or player[self.opponent_index].seeing_board.phand[0][self.opponent_index][i].number!=player[self.player_index].seeing_board.phand[0][self.opponent_index][i].number)\
            and player[0].seeing_board.blue_token>0:
                self.act_num=4  ##情報提供 inform
                self.act_index=i
  


    
        for i in range(HANDNUM):
            for j in range(5):#場に出せるカードandそのカードの情報（数字or色）を相手がまだ知らなかったらそのカードのヒントを出す
                if player[self.player_index].seeing_board.phand[0][self.opponent_index][i].color==player[0].seeing_board.fireworks[j].color\
                and player[self.player_index].seeing_board.phand[0][self.opponent_index][i].number==player[0].seeing_board.fireworks[j].number+1\
                and (player[self.opponent_index].seeing_board.phand[0][self.opponent_index][i].color!=player[self.player_index].seeing_board.phand[0][self.opponent_index][i].color\
                or player[self.opponent_index].seeing_board.phand[0][self.opponent_index][i].number!=player[self.player_index].seeing_board.phand[0][self.opponent_index][i].number)\
                and player[0].seeing_board.blue_token>0:
                    print(player[self.opponent_index].seeing_board.phand[0][self.opponent_index][i].color,player[self.player_index].seeing_board.phand[0][self.opponent_index][i].color)
                    self.act_num=3  ##プレイ可能カードの情報提供 inform playable card
                    self.act_index=i

        for i in range(HANDNUM):
            for j in range(5):
                if player[self.player_index].seeing_board.phand[0][self.player_index][i].color==player[0].seeing_board.fireworks[j].color\
                and ((player[0].seeing_board.fireworks[j].number==5)\
                ##同色の花火が完成しているなら廃棄可能カード
                or(player[self.player_index].seeing_board.phand[0][self.player_index][i].number!=0\
                and player[self.player_index].seeing_board.phand[0][self.player_index][i].number<=player[0].seeing_board.fireworks[j].number)):
                ##そのカードと同色でより大きい数字が盤面に出ているなら廃棄可能カード
                    self.act_num=2  ##廃棄可能カードの廃棄 discard discardable card
                    self.act_index=i
        for i in range(HANDNUM):##12/27追加
            for j in player[0].seeing_board.alldiscarded_list:
                if  j.color == player[self.player_index].seeing_board.phand[0][self.player_index][i].color\
                and j.number < player[self.player_index].seeing_board.phand[0][self.player_index][i].number:##そのカードと同じ色で数字の小さいカードが全廃棄されているなら廃棄可能カード。
                    self.act_num=2  ##廃棄可能カードの廃棄 discard discardable card
                    self.act_index=i

        for i in range(HANDNUM):##12/27追加
            for j in range(5):
                for k in player[0].seeing_board.alldiscarded_list:
                    if  player[self.player_index].seeing_board.phand[0][self.player_index][i].color == player[0].seeing_board.fireworks[j].color\
                    and k.color==player[self.player_index].seeing_board.phand[0][self.player_index][i].color\
                    and k.number==player[self.player_index].seeing_board.phand[0][self.player_index][i].number+1:##花火の盤面の数字+1のカードが全廃棄されていたらその色は廃棄可能
                        self.act_num=2  ##廃棄可能カードの廃棄 discard discardable card
                        self.act_index=i
        for i in range(HANDNUM):#自分の手札で色が分かっていて、その色の場の数字より小さいことが確定したら捨てる
            for j in range(5):#5:len(colorlist)
                if player[self.player_index].seeing_board.prov_hand_PO[self.player_index][i][j].color!='_'\
                and provmax[i]>player[0].seeing_board.fireworks[j].number:
                    act2flag=1
                    break
                act2flag=0
            if act2flag==0:
                self.act_num=2  ##盤面から判断できる廃棄可能カードのプレイ play playable card
                print("盤面から廃棄可能と判断")
                self.act_index=i
           


        for i in range(HANDNUM):
            for j in range(5):
                if player[self.player_index].seeing_board.phand[0][self.player_index][i].color==player[0].seeing_board.fireworks[j].color and player[self.player_index].seeing_board.phand[0][self.player_index][i].number==player[0].seeing_board.fireworks[j].number+1:
                    self.act_num=1  ##情報が確定しているプレイ可能カードのプレイ play playable card
                    self.act_index=i
                    print("確定カードのプレイ")

                elif player[self.player_index].seeing_board.phand[0][self.player_index][i].number==player[0].seeing_board.fireworks[j].number+1:#場が1,1,1,1,1で2のヒントもらったらプレイ
                    for k in range(5):     
                        if player[self.player_index].seeing_board.prov_hand_PO[self.player_index][i][k].color!='_'\
                        and player[0].seeing_board.fireworks[k].number!=player[0].seeing_board.fireworks[j].number:
                            print('k', 'j', player[0].seeing_board.fireworks[k].number, player[0].seeing_board.fireworks[j].number)
                            act1flag=1
                            break
                        act1flag=0
                    if act1flag==0:    
                        self.act_num=1  ##盤面から判断できるプレイ可能カードのプレイ play playable card
                        print("盤面からプレイ可能と判断")
                        self.act_index=i


        if self.act_num == 1:##play playable card
            player[0].seeing_board.played_card = player[self.player_index].pick_card(self.act_index+1)
            player[0].seeing_board.play_processing()
            print("play",player[0].seeing_board.played_card.color,player[0].seeing_board.played_card.number,"act is",self.act_num)
            player[0].visible_hands_update()
            
            return 'p' + player[0].seeing_board.played_card.color + str(player[0].seeing_board.played_card.number)+str(self.act_index+1)
            
        elif self.act_num == 4:

            pi_to_tell_info = self.opponent_index
            if player[self.opponent_index].seeing_board.phand[0][self.opponent_index][self.act_index].number!=player[self.player_index].seeing_board.phand[0][self.opponent_index][self.act_index].number:
                info_to_tell = 1
            else:
                info_to_tell = 2
            if info_to_tell == 1:
                player[self.player_index].tell_number(player[0].seeing_board.phand[0][self.opponent_index][self.act_index].number,pi_to_tell_info)
                print(self.act_index,"act is",self.act_num)
                return 't' + str(pi_to_tell_info) + str(player[0].seeing_board.phand[0][self.opponent_index][self.act_index].number)
            elif info_to_tell == 2:
                player[self.player_index].tell_color(player[0].seeing_board.phand[0][self.opponent_index][self.act_index].color,pi_to_tell_info)
                print(self.act_index,"act is",self.act_num)
                return 't' + str(pi_to_tell_info) + player[0].seeing_board.phand[0][self.opponent_index][self.act_index].color

        elif self.act_num == 3:
            pi_to_tell_info = self.opponent_index
            if player[self.opponent_index].seeing_board.phand[0][self.opponent_index][self.act_index].number!=player[self.player_index].seeing_board.phand[0][self.opponent_index][self.act_index].number:
                info_to_tell = 1
            else:
                info_to_tell = 2
            if info_to_tell == 1:
                player[self.player_index].tell_number(player[0].seeing_board.phand[0][self.opponent_index][self.act_index].number,pi_to_tell_info)
                print(self.act_index,"act is",self.act_num)
                return 't' + str(pi_to_tell_info) + str(player[0].seeing_board.phand[0][self.opponent_index][self.act_index].number)
            elif info_to_tell == 2:
                player[self.player_index].tell_color(player[0].seeing_board.phand[0][self.opponent_index][self.act_index].color,pi_to_tell_info)
                print(self.act_index,"act is",self.act_num)
                return 't' + str(pi_to_tell_info) + player[0].seeing_board.phand[0][self.opponent_index][self.act_index].color

        elif self.act_num == 2:##discard discardable card
            player[0].seeing_board.discarded_card = player[self.player_index].pick_card(self.act_index+1)
            player[0].seeing_board.discard_processing()
            print("discard",player[0].seeing_board.discarded_card.color,player[0].seeing_board.discarded_card.number,"act is",self.act_num)
            player[0].visible_hands_update()  

            return 'd' + player[0].seeing_board.discarded_card.color + str(player[0].seeing_board.discarded_card.number)+ str(self.act_index+1)

        elif self.act_num == 5:   ##random discard
            discard_index = random.choice(hand_index)
            player[0].seeing_board.discarded_card = player[self.player_index].pick_card(discard_index)
            player[0].seeing_board.discard_processing()
            print("discard",player[0].seeing_board.discarded_card.color,player[0].seeing_board.discarded_card.number,"act is",self.act_num)
            player[0].visible_hands_update()
            return 'd' + player[0].seeing_board.discarded_card.color + str(player[0].seeing_board.discarded_card.number) + str(discard_index)
            
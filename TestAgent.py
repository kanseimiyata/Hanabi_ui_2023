import random
import PlayerClass
from PlayerClass import Player
from BoardClass import Board
from CardClass import Card
from macro import color_list
from macro import player
from macro import PLAYERNUMBER
from macro import HANDNUM
from macro import hand_index
from macro import color_to_tell_list
from OtherMethods import get_color_index





class TestAgent(Player):
    def __init__(self,player_index,is_agent):
        super().__init__(player_index, is_agent)
        self.opponent_index = 0
        self.act_index = 0
        self.risk_aversion:float = 1

    
    def choice_act(self):
        if self.player_index==1:##opponentの設定
            self.opponent_index=2
        elif self.player_index==2:
            self.opponent_index=1
        act1flag=0
        act_num=5  ##ランダム廃棄 random discard

        for i in range(HANDNUM):
            if player[self.opponent_index].seeing_board.phand[0][self.opponent_index][i]!=player[self.player_index].seeing_board.phand[0][self.opponent_index][i] and player[0].seeing_board.blue_token>0:
                act_num=4  ##情報提供 inform 
                self.act_index=i

    
        for i in range(HANDNUM):
            for j in range(5):
                if player[self.player_index].seeing_board.phand[0][self.opponent_index][i].color==player[0].seeing_board.fireworks[j].color\
                and player[self.player_index].seeing_board.phand[0][self.opponent_index][i].number==player[0].seeing_board.fireworks[j].number+1\
                and player[self.opponent_index].seeing_board.phand[0][self.opponent_index][i]!=player[self.player_index].seeing_board.phand[0][self.opponent_index][i]\
                and player[0].seeing_board.blue_token>0:
                    act_num=3  ##プレイ可能カードの情報提供 inform playable card
                    self.act_index=i
     

        for i in range(HANDNUM):
            for j in range(5):
                if player[self.player_index].seeing_board.phand[0][self.player_index][i].color==player[0].seeing_board.fireworks[j].color\
                and ((player[0].seeing_board.fireworks[j].number==5)\
                ##同色の花火が完成しているなら廃棄可能カード
                or(player[self.player_index].seeing_board.phand[0][self.player_index][i].number!=0\
                and player[self.player_index].seeing_board.phand[0][self.player_index][i].number<=player[0].seeing_board.fireworks[j].number)):
                ##そのカードと同色でより大きい数字が盤面に出ているなら廃棄可能カード
                    act_num=2  ##廃棄可能カードの廃棄 discard discardable card
                    self.act_index=i

        for i in range(HANDNUM):
            for j in range(5):
                if player[self.player_index].seeing_board.phand[0][self.player_index][i].color==player[0].seeing_board.fireworks[j].color and player[self.player_index].seeing_board.phand[0][self.player_index][i].number==player[0].seeing_board.fireworks[j].number+1:
                    act_num=1  ##情報が確定しているプレイ可能カードのプレイ play playable card
                    self.act_index=i

        for i in range(HANDNUM):
            for j in range(5):
                if player[self.player_index].seeing_board.phand[0][self.player_index][i].number==player[0].seeing_board.fireworks[j].number+1:
                    for k in range(5):     
                        if player[0].seeing_board.prov_hand_PO[self.player_index][i][k].color!='_'\
                        and player[0].seeing_board.fireworks[k].number!=player[self.player_index].seeing_board.prov_hand_PO[self.player_index][i][j].number-1:
                            act1flag=1
                            break
                        act1flag=0
                    if act1flag==0:     
                        act_num=1  ##盤面から判断できるプレイ可能カードのプレイ play playable card
                        self.act_index=i


        if act_num == 1:##play playable card
            player[0].seeing_board.played_card = player[self.player_index].pick_card(self.act_index+1)
            player[0].seeing_board.play_processing()
            print("play",player[0].seeing_board.played_card.color,player[0].seeing_board.played_card.number,"act is",act_num)
            player[0].visible_hands_update()
            
            return 'p' + player[0].seeing_board.played_card.color + str(player[0].seeing_board.played_card.number) + str(self.act_index + 1)


        elif act_num == 2:##discard discardable card
            player[0].seeing_board.discarded_card = player[self.player_index].pick_card(self.act_index+1)
            player[0].seeing_board.discard_processing()
            print("discard",player[0].seeing_board.discarded_card.color,player[0].seeing_board.discarded_card.number,"act is",act_num)
            player[0].visible_hands_update()  

            return 'd' + player[0].seeing_board.discarded_card.color + str(player[0].seeing_board.discarded_card.number) + str(self.act_index + 1)

            
        elif act_num == 3:

            pi_to_tell_info = self.opponent_index
            if player[self.opponent_index].seeing_board.phand[0][self.opponent_index][self.act_index].number!=player[self.player_index].seeing_board.phand[0][self.opponent_index][self.act_index].number:
                info_to_tell = 1
            else:
                info_to_tell = 2
            if info_to_tell == 1:
                player[self.player_index].tell_number(player[0].seeing_board.phand[0][self.opponent_index][self.act_index].number,pi_to_tell_info)
                print(self.act_index,"act is",act_num)
                return 't' + str(pi_to_tell_info) + str(player[0].seeing_board.phand[0][self.opponent_index][self.act_index].number)
            elif info_to_tell == 2:
                player[self.player_index].tell_color(player[0].seeing_board.phand[0][self.opponent_index][self.act_index].color,pi_to_tell_info)
                print(self.act_index,"act is",act_num)
                return 't' + str(pi_to_tell_info) + player[0].seeing_board.phand[0][self.opponent_index][self.act_index].color
        elif act_num == 4:
            pi_to_tell_info = self.opponent_index
            if player[self.opponent_index].seeing_board.phand[0][self.opponent_index][self.act_index].number!=player[self.player_index].seeing_board.phand[0][self.opponent_index][self.act_index].number:
                info_to_tell = 1
            else:
                info_to_tell = 2
            if info_to_tell == 1:
                player[self.player_index].tell_number(player[0].seeing_board.phand[0][self.opponent_index][self.act_index].number,pi_to_tell_info)
                print(self.act_index,"act is",act_num)
                return 't' + str(pi_to_tell_info) + str(player[0].seeing_board.phand[0][self.opponent_index][self.act_index].number)
            elif info_to_tell == 2:
                player[self.player_index].tell_color(player[0].seeing_board.phand[0][self.opponent_index][self.act_index].color,pi_to_tell_info)
                print(self.act_index,"act is",act_num)
                return 't' + str(pi_to_tell_info) + player[0].seeing_board.phand[0][self.opponent_index][self.act_index].color
        elif act_num == 5:   ##random discard
            player[0].seeing_board.discarded_card = player[self.player_index].pick_card(random.choice(hand_index))
            player[0].seeing_board.discard_processing()
            print("discard",player[0].seeing_board.discarded_card.color,player[0].seeing_board.discarded_card.number,"act is",act_num)
            player[0].visible_hands_update()
            return 'd' + player[0].seeing_board.discarded_card.color + str(player[0].seeing_board.discarded_card.number) + str(self.act_index + 1)
        elif act_num == 6:
            player[0].seeing_board.played_card = player[self.player_index].pick_card(self.act_index + 1)
            player[0].seeing_board.play_processing()
            print('play',player[0].seeing_board.played_card.color,str(player[0].seeing_board.played_card.number))
            player[0].visible_hands_update()
            return 'p' + player[0].seeing_board.played_card.color + str(player[0].seeing_board.played_card.number) + str(self.act_index + 1)







    def can_take_riskyact(self):
        global act_num
        playable_cards = []
        ##discardable_cards = []
        hands_PO_set = [[]for i in range(5)]
         
        for i in range(len(color_to_tell_list)):
            if(player[0].seeing_board.fireworks[i].number + 1) <= 5:
                playable_cards.append(color_list[i] + str(player[0].seeing_board.fireworks[i].number + 1))
        print(playable_cards)
        playable_PO_value = [[] for i in range(len(playable_cards))]
        for h_i in range(HANDNUM):
            for i in range(5):
                if self.seeing_board.prov_hand_PO[self.player_index][h_i][i].number != 0:
                    for j in range(5):
                        if self.seeing_board.prov_hand_PO[self.player_index][h_i][j].color != '_':
                            for _k in range(self.seeing_board.visible_cards_set[j][i]):
                                hands_PO_set[h_i].append(color_list[j] + str(i + 1))
        for i in range(len(playable_cards)):
            for h_i in range(HANDNUM):
                if playable_cards[i] in hands_PO_set[h_i] :
                    v = (1/len(hands_PO_set[h_i])) * self.seeing_board.visible_cards_set[get_color_index(playable_cards[i][0])][int(playable_cards[i][1]) - 1]
                    playable_PO_value[i].append(v)
                else :
                    playable_PO_value[i].append(0)
        
        max_playable_PO = 0
        for i in range(len(playable_cards)):
            for j in range(HANDNUM):
                if max_playable_PO < playable_PO_value[i][j]:
                    max_playable_PO = playable_PO_value[i][j]
                    ##max_PO_clr_index = i
                    max_playable_PO_h_index = j

        if max_playable_PO >= self.risk_aversion:
            self.act_index = max_playable_PO_h_index
            act_num =  6

        ### discard possibly discardable
        discardable_PO_value = [0 for i in range(HANDNUM)]
        for h_i in range(HANDNUM):
            numerator = 0
            for i in range(len(color_list) - 1):
                for j in range(player[0].seeing_board.fireworks[i].number):
                    print(hands_PO_set[h_i])
                    if (color_list[i] + str(j + 1)) in hands_PO_set[h_i]:
                        print(color_list[i], str(j + 1))
                        numerator += 1
            discardable_PO_value[h_i] = numerator / len(hands_PO_set[h_i])
            print("v",discardable_PO_value[h_i])
        
        max_discardable_PO = 0
        for i in range(HANDNUM):
            if max_discardable_PO < discardable_PO_value[i]:
                max_discardable_PO = discardable_PO_value[i]
                max_discardable_PO_h_index = i + 1
                print("PO value :",max_discardable_PO," hand index :",max_discardable_PO_h_index)

        

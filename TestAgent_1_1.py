import random
import copy
import sys
import PlayerClass
from PlayerClass import Player
from BoardClass import Board
from OtherMethods import get_color_index
from macro import color_list
from macro import player
from macro import PLAYERNUMBER
from macro import HANDNUM
from macro import hand_index
from macro import color_to_tell_list


class TestAgent_1_1(Player):

    def __init__(self,player_index,is_bot,risk_aversion):
        super().__init__(player_index,is_bot)
        self.opponent_index = 0
        self.act_index = 0
        self.risk_aversion = risk_aversion
        self.act_num = 5
        
        

        




    def choice_act(self):
        self.playable_cards = []
        self.would_playable_cards = [[] for i in range(5)]
        self.hands_PO_set = [[]for i in range(5)]
        self.max_playable_PO = 0
        self.max_playable_PO_h_index = -1
        self.calculate_actable_PO()

        if self.player_index==1:##opponentの設定
            self.opponent_index=2
        elif self.player_index==2:
            self.opponent_index=1
        act1flag=0
        self.act_num=5  ##ランダム廃棄 random discard

        for i in range(HANDNUM):
            if player[self.opponent_index].seeing_board.phand[0][self.opponent_index][i]!=player[self.player_index].seeing_board.phand[0][self.opponent_index][i] and player[0].seeing_board.blue_token>0:
                self.act_num=4  ##情報提供 inform 
  

        self.can_take_risky_Play()    

        for i in range(HANDNUM):
            for j in range(5):
                if player[self.player_index].seeing_board.phand[0][self.opponent_index][i].color==player[0].seeing_board.fireworks[j].color\
                and player[self.player_index].seeing_board.phand[0][self.opponent_index][i].number==player[0].seeing_board.fireworks[j].number+1\
                and player[self.opponent_index].seeing_board.phand[0][self.opponent_index][i]!=player[self.player_index].seeing_board.phand[0][self.opponent_index][i]\
                and player[0].seeing_board.blue_token>0:
                    self.act_num=3  ##プレイ可能カードの情報提供 inform playable card
                    self.act_index=i

        self.can_take_risky_Discard()    

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

        for i in range(HANDNUM):
            for j in range(5):
                if player[self.player_index].seeing_board.phand[0][self.player_index][i].color==player[0].seeing_board.fireworks[j].color and player[self.player_index].seeing_board.phand[0][self.player_index][i].number==player[0].seeing_board.fireworks[j].number+1:
                    self.act_num=1  ##情報が確定しているプレイ可能カードのプレイ play playable card
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
                        self.act_num=1  ##盤面から判断できるプレイ可能カードのプレイ play playable card
                        self.act_index=i


        if self.act_num == 1:##play playable card
            player[0].seeing_board.played_card = player[self.player_index].pick_card(self.act_index+1)
            player[0].seeing_board.play_processing()
            print("play",player[0].seeing_board.played_card.color,player[0].seeing_board.played_card.number,"act is",self.act_num)
            player[0].visible_hands_update()
            
            return 'p' + player[0].seeing_board.played_card.color + str(player[0].seeing_board.played_card.number) + str(self.act_index + 1)


        elif self.act_num == 2:##discard discardable card
            player[0].seeing_board.discarded_card = player[self.player_index].pick_card(self.act_index+1)
            player[0].seeing_board.discard_processing()
            print("discard",player[0].seeing_board.discarded_card.color,player[0].seeing_board.discarded_card.number,"act is",self.act_num)
            player[0].visible_hands_update()  

            return 'd' + player[0].seeing_board.discarded_card.color + str(player[0].seeing_board.discarded_card.number) + str(self.act_index + 1)

            
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

        elif self.act_num == 4:
            pi_to_tell_info = self.opponent_index
            info_to_tell=0    
            while info_to_tell ==0:
                self.act_index=random.randint(0,HANDNUM-1)
                if player[self.opponent_index].seeing_board.phand[0][self.opponent_index][self.act_index].number!=player[self.player_index].seeing_board.phand[0][self.opponent_index][self.act_index].number\
                and player[self.opponent_index].seeing_board.phand[0][self.opponent_index][self.act_index].color!=player[self.player_index].seeing_board.phand[0][self.opponent_index][self.act_index].color:
                    info_to_tell = random.randint(1,2)
                elif player[self.opponent_index].seeing_board.phand[0][self.opponent_index][self.act_index].number!=player[self.player_index].seeing_board.phand[0][self.opponent_index][self.act_index].number:
                    info_to_tell = 1
                elif player[self.opponent_index].seeing_board.phand[0][self.opponent_index][self.act_index].color!=player[self.player_index].seeing_board.phand[0][self.opponent_index][self.act_index].color: 
                    info_to_tell = 2
                    
                    
            if info_to_tell == 1:
                player[self.player_index].tell_number(player[0].seeing_board.phand[0][self.opponent_index][self.act_index].number,pi_to_tell_info)
                print(self.act_index,"act is",self.act_num)
                return 't' + str(pi_to_tell_info) + str(player[0].seeing_board.phand[0][self.opponent_index][self.act_index].number)
            elif info_to_tell == 2:
                player[self.player_index].tell_color(player[0].seeing_board.phand[0][self.opponent_index][self.act_index].color,pi_to_tell_info)
                print(self.act_index,"act is",self.act_num)
                return 't' + str(pi_to_tell_info) + player[0].seeing_board.phand[0][self.opponent_index][self.act_index].color


        elif self.act_num == 5:   ##random discard
            discard_index = random.choice(hand_index)
            player[0].seeing_board.discarded_card = player[self.player_index].pick_card(discard_index)
            player[0].seeing_board.discard_processing()
            print("discard",player[0].seeing_board.discarded_card.color,player[0].seeing_board.discarded_card.number,"act is",self.act_num)
            player[0].visible_hands_update()
            return 'd' + player[0].seeing_board.discarded_card.color + str(player[0].seeing_board.discarded_card.number) + str(discard_index)
        
        elif self.act_num == 6:
            player[0].seeing_board.played_card = player[self.player_index].pick_card(self.act_index + 1)
            player[0].seeing_board.play_processing()
            print('play',player[0].seeing_board.played_card.color,str(player[0].seeing_board.played_card.number))
            player[0].visible_hands_update()
            print("agent take risky play")
            return 'p' + player[0].seeing_board.played_card.color + str(player[0].seeing_board.played_card.number) + str(self.act_index + 1)

        elif self.act_num == 7:
            player[0].seeing_board.discarded_card = player[self.player_index].pick_card(self.act_index+1)
            player[0].seeing_board.discard_processing()
            print("discard",player[0].seeing_board.discarded_card.color,player[0].seeing_board.discarded_card.number,"act is",self.act_num)
            player[0].visible_hands_update()
            print("agent take risky discard")
            return 'd' + player[0].seeing_board.discarded_card.color + str(player[0].seeing_board.discarded_card.number) + str(self.act_index + 1)





    def gen_playable_cards(self):
        self.playable_cards = []
        for i in range(len(color_to_tell_list)):
            if(player[0].seeing_board.fireworks[i].number + 1) <= 5:
                self.playable_cards.append(color_list[i] + str(player[0].seeing_board.fireworks[i].number + 1))
            else:
                self.playable_cards.append("_0")
        print("playable cards: ",self.playable_cards)


    def gen_would_playable_cards(self):
        self.would_playable_cards = [[] for i in range(5)]
        for i in range(len(color_to_tell_list)):
            if(player[0].seeing_board.fireworks[i].number + 1) <= 5:
                for j in range(player[0].seeing_board.fireworks[i].number + 1,5 + 1):
                    self.would_playable_cards[i].append(color_list[i] + str(j))
            else:
                self.would_playable_cards[i].append("_0")
        print("would playable cards: ",self.would_playable_cards)

    
    def gen_hands_PO_sets(self):
        for h_i in range(HANDNUM):
            for i in range(5):
                if self.seeing_board.prov_hand_PO[self.player_index][h_i][i].number != 0:
                    for j in range(5):
                        if self.seeing_board.prov_hand_PO[self.player_index][h_i][j].color != '_':
                            for _k in range(self.seeing_board.visible_cards_set[j][i]):
                                self.hands_PO_set[h_i].append(color_list[j] + str(i + 1))

    def calculate_actable_PO(self):

        self.gen_playable_cards()
        self.gen_hands_PO_sets()
        self.gen_would_playable_cards()
    
        playable_PO_value = [[] for i in range(HANDNUM)]
        ##would_playable_PO_value = [[] for i in range(HANDNUM)]
        ##discardable_PO_value = [[] for i in range(HANDNUM)]
        would_playable_PO_of_hand = [0 for i in range(HANDNUM)]
        playable_PO_value_of_hand = [0 for i in range(HANDNUM)]
        for i in range(len(self.playable_cards)):
            for h_i in range(HANDNUM):
                if self.playable_cards[i] in self.hands_PO_set[h_i] :
                    v = (1/len(self.hands_PO_set[h_i])) \
                        * self.seeing_board.visible_cards_set[get_color_index(self.playable_cards[i][0])][int(self.playable_cards[i][1]) - 1]
                    playable_PO_value[i].append(v)
                else :
                    playable_PO_value[i].append(0)        
        for i in range(HANDNUM):
            for j in range(len(self.playable_cards)):
               playable_PO_value_of_hand[i] += playable_PO_value[j][i]
            ##print(playable_PO_value_of_hand[i])    

        self.max_playable_PO = 0
        self.max_playable_PO_h_index = -1
        for i in range(HANDNUM):
            if self.max_playable_PO <= playable_PO_value_of_hand[i]:
                self.max_playable_PO = copy.deepcopy(playable_PO_value_of_hand[i])
                self.max_playable_PO_h_index = copy.deepcopy(i)
        print("hand number ",self.max_playable_PO_h_index + 1,"is max playable value :", self.max_playable_PO)

        for h_i in range(HANDNUM):
            for i in range(len(color_to_tell_list)):
                for j in range(len(self.would_playable_cards[i])):
                    if self.would_playable_cards[i][j] in self.hands_PO_set[h_i]:
                        would_playable_PO_of_hand[h_i] += (1/len(self.hands_PO_set[h_i])) ##\
                            ##* self.seeing_board.visible_cards_set[get_color_index(self.playable_cards[i][0])][int(self.playable_cards[i][1]) - 1]
            ##print(would_playable_PO_of_hand[h_i])
        
        self.max_discardable_PO = 0
        self.max_discardable_PO_h_index = -1
        for i in range(HANDNUM):
            if self.max_discardable_PO <= 1 - would_playable_PO_of_hand[i]:
                self.max_discardable_PO = copy.deepcopy(1 - would_playable_PO_of_hand[i])
                self.max_discardable_PO_h_index = copy.deepcopy(i)
        print("hand number ",self.max_discardable_PO_h_index + 1,"is max discardable value :", self.max_discardable_PO)

    def can_take_risky_Play(self):
        p_tmp_weight = 0.5 + 0.25 * ( 2 - player[0].seeing_board.red_token )
        if (self.max_playable_PO * p_tmp_weight) >= self.risk_aversion :
            self.act_index = copy.deepcopy(self.max_playable_PO_h_index)
            self.act_num =  6

    def can_take_risky_Discard(self):
        d_tmp_weight = 0.5
        if d_tmp_weight > random.random():
            return
        if self.max_discardable_PO >= self.risk_aversion and player[0].seeing_board.blue_token <= 2:
            self.act_index = copy.deepcopy(self.max_discardable_PO_h_index)
            self.act_num = 7
    """


    def can_take_risky_Play(self):
        playable_cards = []
        ##discardable_cards = []
        
         
        for i in range(len(color_to_tell_list)):
            if(player[0].seeing_board.fireworks[i].number + 1) <= 5:
                playable_cards.append(color_list[i] + str(player[0].seeing_board.fireworks[i].number + 1))
            else:
                playable_cards.append("_0")
        print(playable_cards)
        playable_PO_value = [[] for i in range(len(playable_cards))]
        for h_i in range(HANDNUM):
            for i in range(5):
                if self.seeing_board.prov_hand_PO[self.player_index][h_i][i].number != 0:
                    for j in range(5):
                        if self.seeing_board.prov_hand_PO[self.player_index][h_i][j].color != '_':
                            for _k in range(self.seeing_board.visible_cards_set[j][i]):
                                self.hands_PO_set[h_i].append(color_list[j] + str(i + 1))
        for i in range(len(playable_cards)):
            for h_i in range(HANDNUM):
                if playable_cards[i] in self.hands_PO_set[h_i] :
                    v = (1/len(self.hands_PO_set[h_i])) * self.seeing_board.visible_cards_set[get_color_index(playable_cards[i][0])][int(playable_cards[i][1]) - 1]
                    playable_PO_value[i].append(v)
                else :
                    playable_PO_value[i].append(0)
        
        max_playable_PO = 0
        max_playable_PO_h_index = -1
        playable_PO_value_of_hand = [0 for i in range(HANDNUM)]
        for i in range(HANDNUM):
            for j in range(len(playable_cards)):
               playable_PO_value_of_hand[i] += playable_PO_value[j][i]
            print(playable_PO_value_of_hand[i])
            
            if max_playable_PO < playable_PO_value_of_hand[i]:
                max_playable_PO = copy.deepcopy(playable_PO_value_of_hand[i])
                max_playable_PO_h_index = copy.deepcopy(i)

        print(max_playable_PO_h_index,"is max playable value :", max_playable_PO)
        if max_playable_PO >= self.risk_aversion and player[0].seeing_board.red_token < 2:
            self.act_index = copy.deepcopy(max_playable_PO_h_index)
            self.act_num =  6



    def can_take_risky_Discard(self):
        ### discard possibly discardable
        ##discard_PO = 1.0 - self.risk_aversion
        discard_PO = 1 - copy.deepcopy(self.risk_aversion)
        if player[0].seeing_board.blue_token <= 4 :
            if discard_PO > random.random() or player[0].seeing_board.blue_token == 0: 
                ##print("risky discard?")
                self.act_num = 7
                max_num_handPOset = 0
                for h_i in range(HANDNUM):
                    ##print(self.hands_PO_set[h_i])
                    if max_num_handPOset <= len(self.hands_PO_set[h_i]) :
                        print(max_num_handPOset)
                        
                        max_num_handPOset = copy.deepcopy(len(self.hands_PO_set[h_i]))
                        print(len(self.hands_PO_set[h_i]))
                        self.act_index = h_i
        ##print("return  ctrD")
        return

    """
    
        

       
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

class MiyataAgent(Player):

    def __init__(self,player_index,is_bot):
        super().__init__(player_index,is_bot)
        self.opponent_index=0
        self.act_index=0




    def choice_act(self, message, PORT):
        opp_act = message[0]
        discard_add_opp_hand = player[0].seeing_board.phand[0][1] + player[0].seeing_board.discarded_set
        my_hand = []
        for card in player[0].seeing_board.phand[0][1]:
            my_hand.append(card.color+str(card.number))
        print(my_hand)
        not_my_hand = []
        for card in discard_add_opp_hand:
            not_my_hand.append(card.color+str(card.number))
        if opp_act == 't':
            received_hint = message[4]
            if received_hint.isdigit():
                received_hint = int(received_hint)
        if self.player_index==1:##opponentの設定
            self.opponent_index=2
        elif self.player_index==2:
            self.opponent_index=1
        provmax=[5] * HANDNUM
        prov = [[]] * HANDNUM
        discard_list={'W':[], 'R':[], 'B':[], 'Y':[], 'G':[]}
        for j in player[0].seeing_board.alldiscarded_list:
            discard_list[j.color].append(j.number)
        for i in range(HANDNUM):##各手札の最大値の確定(0,2,3,4,5→5)
            for j in range(5):
                if player[self.player_index].seeing_board.prov_hand_PO[self.player_index][i][j].number!=0:
                    prov[i].append(player[self.player_index].seeing_board.prov_hand_PO[self.player_index][i][j].number)
                    provmax[i]=player[self.player_index].seeing_board.prov_hand_PO[self.player_index][i][j].number
        print('prov', prov)
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
        self.act_num=7  ##ランダム廃棄 random discard


     




        num_col_dic={}
        num_col_dic[1],num_col_dic[2],num_col_dic[3],num_col_dic[4],num_col_dic[5]=0,0,0,0,0
        num_col_dic['W'], num_col_dic['R'], num_col_dic['B'], num_col_dic['Y'], num_col_dic['G']=0,0,0,0,0
        if player[0].seeing_board.blue_token>2:
            for i in range(HANDNUM):#相手自身がまだ知らないカードがあったら情報提供、左のカードから優先
                if player[self.opponent_index].seeing_board.phand[0][self.opponent_index][i].color!=player[self.player_index].seeing_board.phand[0][self.opponent_index][i].color:
                    num_col_dic[player[self.player_index].seeing_board.phand[0][self.opponent_index][i].color] += 1
                if player[self.opponent_index].seeing_board.phand[0][self.opponent_index][i].number!=player[self.player_index].seeing_board.phand[0][self.opponent_index][i].number:
                    num_col_dic[player[self.player_index].seeing_board.phand[0][self.opponent_index][i].number] += 1
            max_key = max(num_col_dic, key=num_col_dic.get)
            self.act_num=6  ##情報提供 inform
            if isinstance(max_key,int):
                tell_info='num'
            else:
                tell_info='color'
            for i in range(HANDNUM):
                if player[self.player_index].seeing_board.phand[0][self.opponent_index][i].color == max_key or player[self.player_index].seeing_board.phand[0][self.opponent_index][i].number == max_key:
                    self.act_index = i
                    break

            
        
        
        #古いカードを捨てる 色or数字の判明数が2,3,4,5,1の順で捨てる　青トークンが4以下
        if player[0].seeing_board.blue_token<=2:
            x_value=8
            for i in range(HANDNUM):
                num_x_count=0
                color_x_count=0
                for j in range(5):
                    if player[self.player_index].seeing_board.prov_hand_PO[self.player_index][i][j].number != 0:
                        num_x_count+=1
                    if player[self.player_index].seeing_board.prov_hand_PO[self.player_index][i][j].color != '_':
                        color_x_count+=1
                if (num_x_count-2)%5+(color_x_count-2)%5 < x_value:
                    x_value = (num_x_count-2)%5+(color_x_count-2)%5
                    self.act_num=5
                    self.act_index=i
                

        # print(2)
        for i in range(HANDNUM):
            for j in range(5):
                if player[self.player_index].seeing_board.phand[0][self.player_index][i].color==player[0].seeing_board.fireworks[j].color\
                and ((player[0].seeing_board.fireworks[j].number==5)\
                ##同色の花火が完成しているなら廃棄可能カード
                or(player[self.player_index].seeing_board.phand[0][self.player_index][i].number!=0\
                and player[self.player_index].seeing_board.phand[0][self.player_index][i].number<=player[0].seeing_board.fireworks[j].number)):
                ##そのカードと同色でより大きい数字が盤面に出ているなら廃棄可能カード
                    self.act_num=4  ##廃棄可能カードの廃棄 discard discardable card
                    self.act_index=i
                    break
        # print(3)
        for i in range(HANDNUM):##12/27追加
            for j in player[0].seeing_board.alldiscarded_list:
                if  j.color == player[self.player_index].seeing_board.phand[0][self.player_index][i].color\
                and j.number < player[self.player_index].seeing_board.phand[0][self.player_index][i].number:##そのカードと同じ色で数字の小さいカードが全廃棄されているなら廃棄可能カード。
                    self.act_num=4  ##廃棄可能カードの廃棄 discard discardable card
                    self.act_index=i
                    break

        # print(4)
        for i in range(HANDNUM):##12/27追加
            for j in range(5):
                for k in player[0].seeing_board.alldiscarded_list:
                    if  player[self.player_index].seeing_board.phand[0][self.player_index][i].color == player[0].seeing_board.fireworks[j].color\
                    and k.color==player[self.player_index].seeing_board.phand[0][self.player_index][i].color\
                    and k.number==player[self.player_index].seeing_board.phand[0][self.player_index][i].number+1:##花火の盤面の数字+1のカードが全廃棄されていたらその色は廃棄可能
                        self.act_num=4  ##廃棄可能カードの廃棄 discard discardable card
                        self.act_index=i
                        break

        # print(5)
        for i in range(HANDNUM):#自分の手札で色が分かっていて、その色の場の数字より小さいことが確定したら捨てる
            for j in range(5):#5:len(colorlist)
                if player[self.player_index].seeing_board.prov_hand_PO[self.player_index][i][j].color!='_'\
                and provmax[i]>player[0].seeing_board.fireworks[j].number:
                    act2flag=1
                    break
                act2flag=0
            if act2flag==0:
                self.act_num=4  ##盤面から判断できる廃棄可能カードのプレイ play playable card
                print("盤面から廃棄可能と判断")
                self.act_index=i
                break


  


        # print(1)
        for i in range(HANDNUM):
            for j in range(5):#場に出せるカードandそのカードの情報（数字or色）を相手がまだ知らなかったらそのカードのヒントを出す
                if player[self.player_index].seeing_board.phand[0][self.opponent_index][i].color==player[0].seeing_board.fireworks[j].color\
                and player[self.player_index].seeing_board.phand[0][self.opponent_index][i].number==player[0].seeing_board.fireworks[j].number+1\
                and (player[self.opponent_index].seeing_board.phand[0][self.opponent_index][i].color!=player[self.player_index].seeing_board.phand[0][self.opponent_index][i].color\
                or player[self.opponent_index].seeing_board.phand[0][self.opponent_index][i].number!=player[self.player_index].seeing_board.phand[0][self.opponent_index][i].number)\
                and player[0].seeing_board.blue_token>0:
                    self.act_num=3  ##プレイ可能カードの情報提供 inform playable card
                    self.act_index=i
                    break
        
            
        
        #相手に場に出せるカードand単独のヒント出せるなら出す
        can_play_num = []
        for i in range(HANDNUM):
            if self.act_num==2:break
            for j in range(5):
                if player[self.player_index].seeing_board.phand[0][self.opponent_index][i].color==player[0].seeing_board.fireworks[j].color\
                and player[self.player_index].seeing_board.phand[0][self.opponent_index][i].number==player[0].seeing_board.fireworks[j].number+1\
                and player[0].seeing_board.blue_token>0:#青トークンある+場に出せるカードが相手の手札にある
                    if player[self.opponent_index].seeing_board.phand[0][self.opponent_index][i].color!=player[self.player_index].seeing_board.phand[0][self.opponent_index][i].color\
                    and player[self.opponent_index].seeing_board.phand[0][self.opponent_index][i].number==player[self.player_index].seeing_board.phand[0][self.opponent_index][i].number:
                        self.act_num=2
                        self.act_index=i
                        tell_info='color'
                        print('確定カードのヒント(color)')
                        break
                    if player[self.opponent_index].seeing_board.phand[0][self.opponent_index][i].number!=player[self.player_index].seeing_board.phand[0][self.opponent_index][i].number\
                    and player[self.opponent_index].seeing_board.phand[0][self.opponent_index][i].color==player[self.player_index].seeing_board.phand[0][self.opponent_index][i].color:
                        self.act_num=2
                        self.act_index=i
                        tell_info='num'
                        print('確定カードのヒント(num)')
                        break
                    if player[self.opponent_index].seeing_board.phand[0][self.opponent_index][i].number!=player[self.player_index].seeing_board.phand[0][self.opponent_index][i].number:
                        can_play_num.append(player[self.player_index].seeing_board.phand[0][self.opponent_index][i].number)
                    if len(can_play_num) != len(set(can_play_num)):
                        self.act_num=2
                        self.act_index=i
                        tell_info='num'
                        print('複数の出せるカードのヒントを相手に出す')
                        break
                    #相手が色と数字のどちらかの情報が無い
                    if player[self.opponent_index].seeing_board.phand[0][self.opponent_index][i].number!=player[self.player_index].seeing_board.phand[0][self.opponent_index][i].number:
                        dup_count=0
                        for k in range(5):
                            if player[self.player_index].seeing_board.phand[0][self.opponent_index][k].number == player[self.player_index].seeing_board.phand[0][self.opponent_index][i].number:
                                dup_count+=1
                        if dup_count==1:
                            self.act_num=2  ##プレイ可能カードの情報提供 inform playable card
                            self.act_index=i
                            tell_info='num'
                            print("単独and出せるカードのヒントを出す(num)")
                            break
                    if player[self.opponent_index].seeing_board.phand[0][self.opponent_index][i].color!=player[self.player_index].seeing_board.phand[0][self.opponent_index][i].color:
                        dup_count=0
                        for k in range(5):
                            if player[self.player_index].seeing_board.phand[0][self.opponent_index][k].color == player[self.player_index].seeing_board.phand[0][self.opponent_index][i].color:
                                dup_count+=1
                        if dup_count==1:
                            self.act_num=2  ##プレイ可能カードの情報提供 inform playable card
                            self.act_index=i
                            tell_info='color'
                            print("単独and出せるカードのヒントを出す(color)")
                            break
           

        # print(6)
        for i in range(HANDNUM):
            if self.act_num==0:break
            for j in range(5):
                #単独のヒント出されたらプレイ（数字）
                if opp_act == 't'\
                and (player[self.opponent_index].seeing_board.phand[0][self.player_index][i].color!=player[self.player_index].seeing_board.phand[0][self.player_index][i].color\
                or player[self.opponent_index].seeing_board.phand[0][self.player_index][i].number!=player[self.player_index].seeing_board.phand[0][self.player_index][i].number):
                    if player[self.player_index].seeing_board.phand[0][self.player_index][i].number == received_hint:
                        if received_hint == player[0].seeing_board.fireworks[j].number+1:
                            if 2 != not_my_hand.count(player[0].seeing_board.fireworks[j].color+str(player[0].seeing_board.fireworks[j].number+1)):
                                dup_count = 0
                                for k in range(5):
                                    if player[self.player_index].seeing_board.phand[0][self.player_index][k].number == received_hint:
                                        dup_count+=1
                                if dup_count==1:
                                    self.act_num=1  ##盤面から判断できるプレイ可能カードのプレイ play playable card
                                    print("相手の意図をくみ取りプレイ(num)")
                                    self.act_index=i
                    #単独のヒント出されたらプレイ（色）
                    elif player[self.player_index].seeing_board.phand[0][self.player_index][i].color == received_hint:
                        print('color_num',player[0].seeing_board.fireworks[color_list.index(received_hint)].number)
                        print(discard_list[received_hint])
                        if provmax[i] > player[0].seeing_board.fireworks[color_list.index(received_hint)].number:
                            if len(discard_list[received_hint])!=0:
                                if min(discard_list[received_hint]) == player[0].seeing_board.fireworks[color_list.index(received_hint)].number+1:
                                    continue
                            if (player[0].seeing_board.fireworks[color_list.index(received_hint)].number+1) in prov[i]:
                                if 2 != not_my_hand.count(player[0].seeing_board.fireworks[i].color+str(player[0].seeing_board.fireworks[i].number+1)):
                                    dup_count = 0
                                    for k in range(5):
                                        if player[self.player_index].seeing_board.phand[0][self.player_index][k].color == received_hint:
                                            dup_count+=1
                                    if dup_count==1:
                                        self.act_num=1  ##盤面から判断できるプレイ可能カードのプレイ play playable card
                                        print("相手の意図をくみ取りプレイ(color)")
                                        self.act_index=i

                if player[self.player_index].seeing_board.phand[0][self.player_index][i].color==player[0].seeing_board.fireworks[j].color and player[self.player_index].seeing_board.phand[0][self.player_index][i].number==player[0].seeing_board.fireworks[j].number+1:
                    self.act_num=0  ##情報が確定しているプレイ可能カードのプレイ play playable card
                    self.act_index=i
                    print("確定カードのプレイ")
                    break

                elif player[self.player_index].seeing_board.phand[0][self.player_index][i].number==player[0].seeing_board.fireworks[j].number+1:#場が1,1,1,1,1で2のヒントもらったらプレイ
                    for k in range(5):     
                        if player[self.player_index].seeing_board.prov_hand_PO[self.player_index][i][k].color!='_'\
                        and player[0].seeing_board.fireworks[k].number!=player[0].seeing_board.fireworks[j].number:
                            act1flag=1
                            break
                        act1flag=0
                    if act1flag==0:    
                        self.act_num=0  ##盤面から判断できるプレイ可能カードのプレイ play playable card
                        print("盤面からプレイ可能と判断")
                        self.act_index=i
                        break
                   
                    


        if self.act_num == 0 or self.act_num == 1:##play playable card
            player[0].seeing_board.played_card = player[self.player_index].pick_card(self.act_index+1)
            player[0].seeing_board.play_processing()
            print("play",player[0].seeing_board.played_card.color,player[0].seeing_board.played_card.number,"act is",self.act_num)
            print('')
            player[0].visible_hands_update()
            
            return 'p' + player[0].seeing_board.played_card.color + str(player[0].seeing_board.played_card.number)+str(self.act_index+1)
        
        elif self.act_num == 3:
            pi_to_tell_info = self.opponent_index
            if player[self.opponent_index].seeing_board.phand[0][self.opponent_index][self.act_index].number!=player[self.player_index].seeing_board.phand[0][self.opponent_index][self.act_index].number:
                info_to_tell = 1
            else:
                info_to_tell = 2
            if info_to_tell == 1:
                player[self.player_index].tell_number(player[0].seeing_board.phand[0][self.opponent_index][self.act_index].number,pi_to_tell_info,PORT)
                print(self.act_index+1,"act is",self.act_num)
                print('')
                return 't' + str(pi_to_tell_info) + str(player[0].seeing_board.phand[0][self.opponent_index][self.act_index].number)
            elif info_to_tell == 2:
                player[self.player_index].tell_color(player[0].seeing_board.phand[0][self.opponent_index][self.act_index].color,pi_to_tell_info,PORT)
                print(self.act_index+1,"act is",self.act_num)
                print('')
                return 't' + str(pi_to_tell_info) + player[0].seeing_board.phand[0][self.opponent_index][self.act_index].color
        
        elif self.act_num == 4 or self.act_num == 5:##discard discardable card or oldcard discard
            player[0].seeing_board.discarded_card = player[self.player_index].pick_card(self.act_index+1)
            player[0].seeing_board.discard_processing()
            print("discard",player[0].seeing_board.discarded_card.color,player[0].seeing_board.discarded_card.number,"act is",self.act_num)
            print('')
            player[0].visible_hands_update()  

            return 'd' + player[0].seeing_board.discarded_card.color + str(player[0].seeing_board.discarded_card.number)+ str(self.act_index+1)

                    
        # elif self.act_num == 4:

        #     pi_to_tell_info = self.opponent_index
        #     if player[self.opponent_index].seeing_board.phand[0][self.opponent_index][self.act_index].number!=player[self.player_index].seeing_board.phand[0][self.opponent_index][self.act_index].number:
        #         info_to_tell = 1
        #     else:
        #         info_to_tell = 2
        #     if info_to_tell == 1:
        #         player[self.player_index].tell_number(player[0].seeing_board.phand[0][self.opponent_index][self.act_index].number,pi_to_tell_info)
        #         print(self.act_index,"act is",self.act_num)
        #         return 't' + str(pi_to_tell_info) + str(player[0].seeing_board.phand[0][self.opponent_index][self.act_index].number)
        #     elif info_to_tell == 2:
        #         player[self.player_index].tell_color(player[0].seeing_board.phand[0][self.opponent_index][self.act_index].color,pi_to_tell_info)
        #         print(self.act_index,"act is",self.act_num)
        #         return 't' + str(pi_to_tell_info) + player[0].seeing_board.phand[0][self.opponent_index][self.act_index].color

        
        elif self.act_num == 7:   ##random discard
            discard_index = random.choice(hand_index)
            player[0].seeing_board.discarded_card = player[self.player_index].pick_card(discard_index)
            player[0].seeing_board.discard_processing()
            print("discard",player[0].seeing_board.discarded_card.color,player[0].seeing_board.discarded_card.number,"act is",self.act_num)
            player[0].visible_hands_update()
            print('')
            return 'd' + player[0].seeing_board.discarded_card.color + str(player[0].seeing_board.discarded_card.number) + str(discard_index)
        
        
        elif self.act_num == 2 or self.act_num == 6:
            pi_to_tell_info = self.opponent_index
            if tell_info == 'num':
                player[self.player_index].tell_number(player[0].seeing_board.phand[0][self.opponent_index][self.act_index].number,pi_to_tell_info,PORT)
                print(self.act_index+1,"act is",self.act_num)
                print('')
                return 't' + str(pi_to_tell_info) + str(player[0].seeing_board.phand[0][self.opponent_index][self.act_index].number)
            else:
                player[self.player_index].tell_color(player[0].seeing_board.phand[0][self.opponent_index][self.act_index].color,pi_to_tell_info, PORT)
                print(self.act_index+1,"act is",self.act_num)
                print('')
                return 't' + str(pi_to_tell_info) + player[0].seeing_board.phand[0][self.opponent_index][self.act_index].color
        
        
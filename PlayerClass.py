##### PlayerClass.py
##### 

import copy
from BoardClass import Board
from CardClass import Card
from macro import PLAYERNUMBER
from macro import HANDNUM
from macro import color_list
from macro import player

class Player:
    
    def __init__(self,player_index,is_agent):## constructor
        """
        Args:
            player_index <int>:
                プレイヤーオブジェクトのindex，ただし0は全員の手札が見えるゲームマスター的なオブジェクト

            is_agent <boolean>:
                プレイヤーが人間ならばFalse，エージェントならばTrue
        """
        self.player_index = player_index
        self.is_agent       = is_agent
        self.seeing_board = Board()
        self.act_num = -1
        self.thinking_time:float = 0.0
    
    
    def hands_init(self):##initialization hand
        count = 0
        for i in range(PLAYERNUMBER):
                for j in range(HANDNUM):
                    self.seeing_board.phand[0][i + 1][j] = copy.deepcopy(self.seeing_board.deck[count])
                    count+=1
        for i in range(PLAYERNUMBER * HANDNUM):
            self.seeing_board.deck.pop(0)
            
        return 
    

    def hands_print(self,player_index):## show hand
        """
        Args:
            player_index <int>:        
        """
        for i in range(HANDNUM):
            self.seeing_board.phand[0][player_index][i].print_card()
        print("")
        return



    def print_hands_PO(self,player_index):
        """
        Args:
            player_index <int>:
        """
        for i in range(HANDNUM):
            for j in range(len(color_list) - 1):### len(color_list) is 5
                self.seeing_board.prov_hand_PO[player_index][i][j].print_card()
            print("")
        return

    def print_visible_cards_set(self):
        for i in range(len(color_list) - 1):
            for j in range(5):
                print(self.seeing_board.visible_cards_set[i][j], end=" ")
            print("")



    def visible_hands_update(self): ## hands each players view are updated. only player[0] can use this method
        for i in range(PLAYERNUMBER):
                for j in range(PLAYERNUMBER):
                    if i != j :
                        for k in range(HANDNUM):
                            player[i + 1].seeing_board.phand[0][j + 1][k] = copy.deepcopy(player[0].seeing_board.phand[0][j + 1][k])
        return
        
    def pick_card(self, hand_index):
        """
        Args:
            hand_index <int>:
                主にphandなどの手札配列を参照するためのindex
        
        Returns:
            tmp <Card>(object of Card class)
        """
        tmp = copy.deepcopy(player[0].seeing_board.phand[0][self.player_index][hand_index - 1])
        self.seeing_board.phand[0][self.player_index][hand_index - 1].set_contents(0, color_list[5])
        for i in range(HANDNUM):
            for j in range(1,PLAYERNUMBER + 1):
                player[j].seeing_board.prov_hand_PO[self.player_index][hand_index - 1][i].set_contents(i + 1,color_list[i])
        if len(player[0].seeing_board.deck) > 0 :
            drawn_card = copy.deepcopy(player[0].seeing_board.deck[0])
            player[0].seeing_board.phand[0][self.player_index][hand_index - 1] = copy.deepcopy(player[0].seeing_board.deck[0])
            player[0].seeing_board.deck.pop(0)
            for j in range(len(color_list) - 1):
                if color_list[j] == drawn_card.color:
                    clr_index = j
            for j in range(1,PLAYERNUMBER + 1):
                if j != self.player_index:
                    player[j].seeing_board.visible_cards_set[clr_index][drawn_card.number - 1] -= 1
        
        else :
            player[0].seeing_board.phand[0][self.player_index][hand_index - 1].color = '_'
            player[0].seeing_board.phand[0][self.player_index][hand_index - 1].number = 0


        for i in range(len(color_list) - 1):
            if color_list[i] == tmp.color:
                clr_index = i
        self.seeing_board.visible_cards_set[clr_index][tmp.number - 1] -= 1

        return tmp
    
    
    def tell_number(self, num, recv_index, PORT):
        """
        Args:
            num <int>:
                Hanabiに使用される1~5までの数字

            recv_index <int> :
                教えてもらった情報を受け取るプレイヤーのindex
        """
        print('player', self.player_index,' tell number ', num , ' to player' ,recv_index)
        with open('play_log'+str(PORT)+'.txt', mode='a') as f:
            f.write('player')
            f.write(str(self.player_index))
            f.write(' tell number ')
            f.write(str(num))
            f.write('\n')

        for i in range(HANDNUM):
            if self.seeing_board.phand[0][recv_index][i].number == num:
                player[recv_index].seeing_board.phand[0][recv_index][i].set_number(num)
                for card_index in range(5):
                    if card_index != (num - 1):
                        ##player[0].seeing_board.prov_hand_PO[recv_index][i][card_index].number = 0
                        for j in range(1,PLAYERNUMBER + 1):
                            player[j].seeing_board.prov_hand_PO[recv_index][i][card_index].number = 0
            else:
                ##player[0].seeing_board.prov_hand_PO[recv_index][i][num - 1].number = 0
                for j in range(1,PLAYERNUMBER + 1):
                    player[j].seeing_board.prov_hand_PO[recv_index][i][num - 1].number = 0
        player[0].seeing_board.blue_token -= 1
        return
    
    def tell_color(self, clr, recv_index, PORT):
        """
        Args:
            clr <char>:
                Hanabiに使用される5色("W","R","B","Y","G")
                
            recv_index <int> :
                教えてもらった情報を受け取るプレイヤーのindex
        """
        print('player', self.player_index, ' tell color ', clr , ' to player' ,recv_index)
        with open('play_log'+str(PORT)+'.txt', mode='a') as f:
            f.write('player')
            f.write(str(self.player_index))
            f.write(' tell color ')
            f.write(str(clr))
            f.write('\n')
        for i in range(len(color_list) - 1):
            if color_list[i] == clr:
                clr_index = i

        for i in range(HANDNUM):
            if self.seeing_board.phand[0][recv_index][i].color == clr:
                player[recv_index].seeing_board.phand[0][recv_index][i].color = clr
                for card_index in range(5):
                    if card_index != clr_index:
                        for j in range(1,PLAYERNUMBER + 1):
                            player[j].seeing_board.prov_hand_PO[recv_index][i][card_index].color = '_'
                        ##player[0].seeing_board.prov_hand_PO[recv_index][i][card_index].color = '_'
            else:
                ##player[0].seeing_board.prov_hand_PO[recv_index][i][clr_index].color = "_"
                for j in range(1,PLAYERNUMBER + 1):
                    player[j].seeing_board.prov_hand_PO[recv_index][i][clr_index].color = "_"

        player[0].seeing_board.blue_token -= 1
        return     
        
    def hands_PO_update(self):
        
        for i in range(HANDNUM):
            numlist_in_PO = []
            for j in range(5):
                if self.seeing_board.prov_hand_PO[self.player_index][i][j].number != 0:
                    numlist_in_PO.append(j + 1)
            
            for j in range(len(color_list) - 1):
                confirmable_flag = 0
                for k in range(len(numlist_in_PO)):
                    if self.seeing_board.visible_cards_set[j][numlist_in_PO[k] -1] > 0:
                        confirmable_flag = -1
                if confirmable_flag == 0:
                    self.seeing_board.prov_hand_PO[self.player_index][i][j].color = "_"
       
                        



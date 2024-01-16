import random
import PlayerClass
from PlayerClass import Player
from BoardClass import Board
from macro import player
from macro import PLAYERNUMBER
from macro import HANDNUM
from macro import hand_index
from macro import color_to_tell_list

class RandomAgent(Player):

    def __init__(self,player_index,is_bot):
        super().__init__(player_index,is_bot)

    def choice_act(self):
        act_num = random.choice([1,2,3])
        
        ##play card
        if act_num == 1:
            h_i = random.choice(hand_index)
            player[0].seeing_board.played_card = player[self.player_index].pick_card(h_i)
            player[0].seeing_board.play_processing()
            player[0].visible_hands_update()

            return 'p' + player[0].seeing_board.played_card.color + str(player[0].seeing_board.played_card.number)

        ##discard

        elif act_num == 2:
            h_i = random.choice(hand_index)
            player[0].seeing_board.discarded_card = player[self.player_index].pick_card(h_i)
            player[0].seeing_board.discard_processing()
            player[0].visible_hands_update()
            return 'd' + player[0].seeing_board.played_card.color + str(player[0].seeing_board.played_card.number)

        elif act_num == 3:
            p_num_list = []
            for i in range(PLAYERNUMBER):
                p_num_list.append(i + 1)
            pi_to_tell_info = random.choice(p_num_list)
            info_to_tell = random.choice([1,2])
            if info_to_tell == 1:
                num = random.choice([1,2,3,4,5])
                player[self.player_index].tell_number(num,pi_to_tell_info)
                return 't' + str(pi_to_tell_info) + str(num)
            elif info_to_tell == 2:
                char = random.choice(color_to_tell_list)
                player[self.player_index].tell_color(char,pi_to_tell_info)
                return 't' + str(pi_to_tell_info) + char

        
        
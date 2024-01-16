### hanabi ecosystem
### main.py
### kitanakute suman.......


import macro
import copy
import random
import csv
from macro import PLAYERNUMBER
from macro import HANDNUM
from macro import color_list
from macro import player
from macro import color_to_tell_list
import CardClass
import BoardClass
from PlayerClass import Player
from RandomAgent import RandomAgent

############################################
"""
pre play part
"""

##generate players
#for i in range (PLAYERNUMBER + 1):
#    player.append(Player(i, False))

player.append(Player(0,False))
player.append(RandomAgent(1,True))
player.append(RandomAgent(2,True))

player[0].seeing_board.deck_init()

#random.seed(SEED)
random.shuffle(player[0].seeing_board.deck)

## Hand out
player[0].hands_init()
player[0].visible_hands_update()

##variable init
act_num = 0
card_index = 0
pi_to_tell_info = 0
info_to_tell = 0
num_totell = 0
exit_flag = 0
remaining_turn = 255 
char_to_tell = "_"

#############################################

player[1].print_hands_PO(1)
"""
play part (roop)
"""
with open('sample.csv', 'w') as f:
    ##writer = csv.##writer(f)
    while(True):

        for i in range(1,PLAYERNUMBER+1):

            ####################################################
            """
            check exit condition
            """
            if remaining_turn == 0:
                break
            elif player[0].seeing_board.red_token == 3:
                break
            ####################################################

            print("player", i ,"'s turn")
            ##writer.##writerow("player", i ,"'s turn")
            for j in range(len(player[0].seeing_board.fireworks)):
                player[0].seeing_board.fireworks[j].print_card()

            print("")
                    
            print(player[0].seeing_board.blue_token, " blue tokens remaining")
            print("having ", player[0].seeing_board.red_token, " red tokens")

                
            print("player",i,"'s hand :", end = "")
            player[i].hands_print(i)

            print("player",i,"'s hand possibility :")
            player[i].print_hands_PO(i)

            for j in range(1,PLAYERNUMBER+1):
                if i != j:
                    print("player", j,"'s hand :", end = "")
                    player[i].hands_print(j)

            
            if player[i].is_agent is True:
                player[i].choice_act()

            #######################################################################3
            elif player[i].is_agent is False:
                """
                player who is human use this part 
                """

                while(True):
                    print("choose action number below")
                    print("1. play card")
                    print("2. discard")
                    print("3. tell information to someone")
                    act_num = int(input())
                    if act_num < 1 or 3 < act_num:
                        print('that is invalid number')
                    else :
                        break

                if act_num == 1:##play card
                    while(True):
                        print('choose play card number index in 1 to 5')
                        card_index = int(input())
                        if card_index < 1 or 5< card_index:
                            print('that is invalid number')
                        else :
                            break

                    player[0].seeing_board.played_card = player[i].pick_card(card_index)
                    player[0].seeing_board.play_processing()
                    player[0].visible_hands_update()

                if act_num == 2:##discard
                    while(True):
                        print('choose discard number index in 1 to 5')
                        card_index = int(input())
                        if card_index < 1 or 5 < card_index:
                            print('that is invalid number')
                        else :
                            break
                    player[0].seeing_board.discarded_card = player[i].pick_card(card_index)
                    player[0].seeing_board.discard_processing()
                    player[0].visible_hands_update()


                if act_num == 3:##tell information
                    while(True):
                        print("choose player index to tell information")
                        pi_to_tell_info = int(input())
                        if pi_to_tell_info < 1 or PLAYERNUMBER < pi_to_tell_info:
                            print('that is invalid number')
                        elif pi_to_tell_info == i:
                            print('the index is yourself!!!')
                        else :
                            break

                    while(True):
                        print("1.number or 2.color?")
                        info_to_tell = int(input())
                        if info_to_tell < 1 or 2 < info_to_tell:
                            print('that is invalid number')
                        else :
                            break

                    if info_to_tell == 1:
                        while(True):
                            print("input a number to tell")
                            num_totell = int(input())
                            if num_totell < 1 or 5 < num_totell:
                                print('that is invalid number')
                            else :
                                break

                        player[i].tell_number(num_totell, pi_to_tell_info)

                    if info_to_tell == 2:
                        while(True):
                            print("input a color to tell")
                            char_to_tell = input()
                            if char_to_tell in color_to_tell_list:
                                break
                            else :
                                print("that is invalid color")

                        player[i].tell_color(char_to_tell, pi_to_tell_info)
            #################################################################
                
            remaining_turn -= 1

            """
            check exit trigger
            """
            if exit_flag == 0:
                if len(player[0].seeing_board.deck) == 0:
                    exit_flag = 1
                    remaining_turn = PLAYERNUMBER

        ###################################################
        """
        check exit condition
        """
        if remaining_turn == 0:
            break
        elif player[0].seeing_board.red_token == 3:
            break
        ####################################################


    #############################################################################
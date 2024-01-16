from websocket_server import WebsocketServer
import macro
import copy
import random
import sys
import pathlib
import time
from macro import PLAYERNUMBER
from macro import HANDNUM
from macro import color_list
from macro import player
from macro import color_to_tell_list
import CardClass
import BoardClass
from PlayerClass import Player
from RandomAgent import RandomAgent
from DecideAgent import DecideAgent
from TestAgent   import TestAgent
from TestAgent_1_1 import TestAgent_1_1
from TestAgent_A import TestAgent_A
from TestAgent_B import TestAgent_B
from OtherMethods import visible_cards_init


str_list = []
private_ip_addr = '192.168.1.21'

PORT=9000
server = WebsocketServer(PORT,host='localhost')


############################################
"""
pre play part
"""

args = sys.argv


if len(args) == 1:
    player.append(Player(0,False))
    player.append(Player(1,False))
    player.append(TestAgent(2,False))
  

if len(args) == 2:
    player.append(Player(0,False))
    player.append(Player(1,False))
    ##player.append(TestAgent_1_1(2,True,float(args[1])))
    player.append(TestAgent(2,False))

elif len(args) == 3:
    random.seed(int(args[2]))
    player.append(Player(0,False))
    player.append(Player(1,False))
    ##player.append(TestAgent_1_1(2,True,float(args[1])))
    player.append(TestAgent_1_1(2,True,float(args[1])))

elif len(args) == 5:
    participant_id = int(args[3])
    random.seed(int(args[2]))
    player.append(Player(0,False))
    player.append(Player(1,False))
    player.append(TestAgent_1_1(2,True,float(args[1])))
    ##log_path = r'C:\Users\AtsushiKawagoe\Documents\about_lab\hanabi_web\dev\tmp_log\log_id_'  + str(participant_id) + '.txt'
    log_path = r'\\192.168.1.251\share\experiment_data_kawagoe\playlog\log_id_' + args[3] + '_' + args[4] + '.txt'
    try:
        with open(log_path,'a') as log_file:
            log_file.write('participant id: ' + str(args[3]) + ' attempt number: ' + str(args[4]))
            log_file.write('risk aversion: ' + str(args[1]))
            log_file.write('random seed:' + str(args[2]) + '\n')
            log_file.close()    
    except:
        print("initialized file open error")
        print("could not open:",log_path)
    

else:
    print('argument error')
    sys.exit(1)


player[0].seeing_board.deck_init()

random.shuffle(player[0].seeing_board.deck)

## Hand out
player[0].hands_init()
player[0].visible_hands_update()
visible_cards_init()

##variable init
act_num = 0
card_index = 0
pi_to_tell_info = 0
info_to_tell = 0
num_totell = 0
exit_flag = 0
remaining_turn = 2
char_to_tell = "_"
message_to_send = ''
num_of_clients = 0
start_time = 0
#############################################

def gen_and_send_message(acting_player_i, message_to_send, act):

    """
    this method is generally called to generate message when any players have action.
    After that, generated message is send to all players 

    args:
        acting_player_i <int>:
            行動をしたプレイヤー
        message_to_send <string>:
            クライアント側に送るメッセージをためる変数
        act <string> : 
            playerのactionを放り込む
            クライアント側のlogのために使われる
    """
    for client in WebsocketServer.clients:
        message_to_send = str(client['id'])
        ### message_to_send[0]

        for i in range(5):
            message_to_send += str(player[0].seeing_board.fireworks[i].number)
            ### copied fireworks
        ### message_to_send[1] ~ [5]

        message_to_send += str(player[0].seeing_board.blue_token)
        message_to_send += str(player[0].seeing_board.red_token)
        ### copied tokens
        ### message_to_send[6] ~ [7]

        if len(player[0].seeing_board.deck) < 10 :
            message_to_send += '0'
            message_to_send += str(len(player[0].seeing_board.deck))
        else :
            message_to_send += str(len(player[0].seeing_board.deck))
        ### copied the number of remaining decks
        ### message_to_send[8] ~ [9]

        for i in range(1,PLAYERNUMBER + 1):
            for j in range(HANDNUM):
                message_to_send += player[0].seeing_board.phand[0][i][j].color
                message_to_send += str(player[0].seeing_board.phand[0][i][j].number)
        ### copied player hands 
        ### message_to_send[10] ~ [29]

        for i in range(1, PLAYERNUMBER + 1):
            for j in range(HANDNUM):
                for k in range(5):
                    message_to_send += player[client['id']].seeing_board.prov_hand_PO[i][j][k].color
                    message_to_send += str(player[client['id']].seeing_board.prov_hand_PO[i][j][k].number)
        ### message_to_send[30] ~ [129]

        message_to_send += str(acting_player_i)
        ### message_to_send[130]
        message_to_send += act
        ### message_to_send[131] ~ [133] + [134]()
        if len(args) == 5:
            try:
                with open(log_path,mode='a') as log_file:
                    log_file.write(message_to_send + '\n') 
                    log_file.write("action number of player " + str(acting_player_i) + " is " + str(player[acting_player_i].act_num) + '\n')
                    log_file.write("thinking time: " + str(player[acting_player_i].thinking_time) + '\n')
                    log_file.close()
            except:
                print("file open error")

        

        server.send_message(client,message_to_send)



def generate_message(acting_player_i, message_to_send, act):



    message_to_send = str(acting_player_i)
    ### message_to_send[0]

    for i in range(5):
        message_to_send += str(player[0].seeing_board.fireworks[i].number)
        ### copied fireworks
    ### message_to_send[1] ~ [5]

    message_to_send += str(player[0].seeing_board.blue_token)
    message_to_send += str(player[0].seeing_board.red_token)
    ### copied tokens
    ### message_to_send[6] ~ [7]

    if len(player[0].seeing_board.deck) < 10 :
        message_to_send += '0'
        message_to_send += str(len(player[0].seeing_board.deck))
    else :
        message_to_send += str(len(player[0].seeing_board.deck))
    ### copied the number of remaining decks
    ### message_to_send[8] ~ [9]

    for i in range(1,PLAYERNUMBER + 1):
        for j in range(HANDNUM):
            message_to_send += player[0].seeing_board.phand[0][i][j].color
            message_to_send += str(player[0].seeing_board.phand[0][i][j].number)
    ### copied player hands 
    ### message_to_send[10] ~ [29]

    for i in range(1, PLAYERNUMBER + 1):
        for j in range(HANDNUM):
            for k in range(5):
                message_to_send += player[0].seeing_board.prov_hand_PO[i][j][k].color
                message_to_send += str(player[0].seeing_board.prov_hand_PO[i][j][k].number)
    ### message_to_send[30] ~ [129]


    message_to_send += str(acting_player_i)
    ### message_to_send[130]
    message_to_send += act
    ### message_to_send[131] ~ [133]
    return message_to_send


def show_situation(player_index, is_agent):
    print("")
    if is_agent == True:
        print("player", player_index,"'s turn (Agent)")
    else:
        print("player", player_index,"'s turn (Human)")

    print("fireworks :", end="")
    for j in range(len(player[0].seeing_board.fireworks)):
        player[0].seeing_board.fireworks[j].print_card()

    print("")
            
    print("blue tokens : ", player[0].seeing_board.blue_token)
    print("red tokens", player[0].seeing_board.red_token)

    for i in range(1,PLAYERNUMBER + 1):
        print("player",i,"'s hand :", end = "")
        player[0].hands_print(i)
        
    for i in range(1, PLAYERNUMBER + 1):
        print("player",i,"'s hand possibility :")
        player[player_index].print_hands_PO(i)


    player[player_index].print_visible_cards_set()
    
    print("")


def check_exit(acting_player_i, message_to_send):
    global remaining_turn
    
    if remaining_turn == 0:
        print("exit")
        gen_and_send_message(acting_player_i,message_to_send,"end")
        
    elif len(player[0].seeing_board.deck) == 0:
        remaining_turn -= 1



# Called for every client connecting (after handshake)
def new_client(client, server):
    global num_of_clients
    num_of_clients += 1
    
    message_to_send = ''
    print("New client connected and was given id %d" % client['id'])
    ##message_to_send = generate_message(client['id'], message_to_send ,"")
    ##server.send_message(client,message_to_send)

    gen_and_send_message(client['id'], message_to_send, "")


# Called for every client disconnecting
def client_left(client, server):
    global num_of_clients
    print("Client(" + str(client['id']) + ") disconnected")
    num_of_clients -= 1
    print("the number of clients is ",num_of_clients)
    server.shutdown()
    sys.exit("server exit")


# Called when a client sends a message
def message_received(client, server, message):
    global start_time
    print(message)
    message_to_send = ''
    act = ''
    ##print("Client(%d) said: %s" % (client['id'], message))
    show_situation(client['id'], False)

    if player[client['id']].is_agent is False:
        
        if message[0] == 'p':
            player[client['id']].act_num = 1
            card_index = int(message[2])
            act = 'p' + player[0].seeing_board.phand[0][client['id']][card_index - 1].color + str(player[0].seeing_board.phand[0][client['id']][card_index - 1].number) + str(card_index)
            player[0].seeing_board.played_card = player[client['id']].pick_card(card_index)
            player[0].seeing_board.play_processing()
            player[0].visible_hands_update()
            print('player1 played ',player[0].seeing_board.played_card.color,player[0].seeing_board.played_card.number)
        

        elif message[0] == 'd':
            card_index = int(message[2])
            player[client['id']].act_num = 2
            act = 'd' + player[0].seeing_board.phand[0][client['id']][card_index - 1].color + str(player[0].seeing_board.phand[0][client['id']][card_index - 1].number) + str(card_index) 
            player[0].seeing_board.discarded_card = player[client['id']].pick_card(card_index)
            player[0].seeing_board.discard_processing()
            player[0].visible_hands_update()
            print('player1 discarded ',player[0].seeing_board.discarded_card.color,player[0].seeing_board.discarded_card.number)

        elif message[0] == 't':
            player[client['id']].act_num = 3
            p_index = int(message[2])
            if message[4] in ['1','2','3','4','5']:
                num_totell = int(message[4])
                act = 't' + str(p_index) + str(num_totell)
                player[client['id']].tell_number(num_totell,p_index)
                ##print('tellnum')
            elif message[4] in color_to_tell_list:
                char_to_tell = message[4]
                act = 't' + str(p_index) + char_to_tell
                player[client['id']].tell_color(char_to_tell,p_index)
                ##print('tellcolor')

        player[client['id']].thinking_time = time.time() - start_time
    player[client['id']].hands_PO_update()
    gen_and_send_message(client['id'], message_to_send, act)

    

    time.sleep(4.5)
    sleep_time = 0
    if player[2].is_agent == True:

        check_exit(2,message_to_send)
        show_situation(2,True)
        act = player[2].choice_act()
  

        if player[2].act_num == 3:
            sleep_time = 2
        elif player[2].act_num == 4:
            sleep_time = 2
        elif player[2].act_num == 5:
            sleep_time = 4
        elif player[2].act_num == 6:
            sleep_time = 5
        elif player[2].act_num == 7:
            sleep_time = 5

        time.sleep(sleep_time)
        player[2].hands_PO_update()
        gen_and_send_message(2, message_to_send, act)

    check_exit(client['id'],message_to_send)
    start_time = time.time()

def main():
    server.set_fn_new_client(new_client)
    server.set_fn_client_left(client_left)
    server.set_fn_message_received(message_received)
    server.run_forever()



if __name__ == "__main__":
    main()


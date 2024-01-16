# -*- coding: utf-8 -*-
from websocket_server import WebsocketServer
import macro
import copy
import random
import sys
import time
import pathlib
import time
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
from Miyata_Agent import MiyataAgent
from DecideAgent_ver1 import DecideAgent
from TestAgent   import TestAgent
from TestAgent_1_1 import TestAgent_1_1
from TestAgent_A import TestAgent_A
from TestAgent_B import TestAgent_B
from OtherMethods import visible_cards_init
from tkinter import messagebox
from contextlib import redirect_stdout
import datetime

now = datetime.datetime.now()
today = now.strftime('%m_%d')
print(today)


print('実験番号を入力してください(1~10)')
x = input()
print('何回目ですか？(1~4)')
y = input()

# x,y=str(4),str(0)


vs_agent = False
str_list = []
private_ip_addr = '192.168.1.21'
agentmode=0


if y=='4':
    vs_agent=True
    print('ポートを入力してください(1 or 2)')
    z = input()
    if z == '1':
        PORT=8000
    else:
        PORT=9000
else:
    PORT=9000

with open('play_log'+str(PORT)+'.txt', mode='a') as f:
    f.write('\n')
    f.write(today)
    f.write(' team_')
    f.write(x)
    f.write(' time_')
    f.write(y)
    f.write('\n')

server = WebsocketServer(PORT,host='localhost')



############################################
"""
pre play part
"""
##with open('sample.txt', 'w',newline="") as f, redirect_stdout(f):
    ####writer = csv.##writer(f)
args = sys.argv


seed=int(x)+int(y)
if int(seed) == 0:
    random.seed(1000)
else:
    random.seed(int(seed)%4)
print('seed:', int(seed)%4)
print("実験を始めます")
print("この画面を消さずにclient.htmlを開いてください")
sys.stdout=open('csv/'+x+'組目'+y+'回目_'+today+'_'+str(PORT)+'.csv', 'w',newline="") #debug時はコメントアウト




player.append(Player(0,False))
player.append(Player(1,False))

if vs_agent==True:
    player.append(MiyataAgent(2,True))
else:
    player.append(Player(2,False))
# これをTrueにすると、is_agentがTureになり、エージェント扱い
# ここでAgent名を決めることができる
    

print('random seed:' + str(int(seed)%4))
print('agentmode '+str(agentmode)+' start') 
##sys.stdout=open(args[3]+'.csv', 'w',newline="")
##sys.stdout=open('sample.csv', 'w',newline="")   



player[0].seeing_board.deck_init() #deckリストにカードを入れる

random.shuffle(player[0].seeing_board.deck) #deckリストの中身をシャッフル

## Hand out
player[0].hands_init() #デッキから手札にカードを配る()５枚ずつ 、配った分だけデッキから削除、player1[0]にはお互いの手札の情報が入る
player[0].visible_hands_update() #表示する相手の手札を格納、player[1]にはplayer1から見える情報が入る、player[2]にはplayer2から見える情報が入る
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
    
    if 'order_mode' in message_to_send :
        hint_place = (message_to_send[10:]+'0000')[:5]
        #相手の手札の情報
        dup_place, code='',''
        for j in range(HANDNUM):
            if str(j+1) in hint_place:continue
            if act == player[0].seeing_board.phand[0][3-acting_player_i][j].color:
                dup_place+=str(j+1)
                code = 'C'
            if act == str(player[0].seeing_board.phand[0][3-acting_player_i][j].number):
                dup_place+=str(j+1)
                code = 'N'
        message_to_send = 'O' + str(acting_player_i) + act + hint_place + code + dup_place
        for client in WebsocketServer.clients:
            server.send_message(client,message_to_send)
        if dup_place != '':
            return True
        return False



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
    for client in WebsocketServer.clients:#websocketserverのクライアントにそれぞれメッセージ(e.data)を送る
        message_to_send = str(client['id']) #1or2
        ### message_to_send[0]

        for i in range(5):
            message_to_send += str(player[0].seeing_board.fireworks[i].number)#最初は0が5回入る（fireworks:場の状況）
            ### copied fireworks
        ### message_to_send[1] ~ [5]

        message_to_send += str(player[0].seeing_board.blue_token)
        message_to_send += str(player[0].seeing_board.red_token)
        ### copied tokens
        ### message_to_send[6] ~ [7]

        if len(player[0].seeing_board.deck) < 10 :#残りデッキの枚数
            message_to_send += '0'
            message_to_send += str(len(player[0].seeing_board.deck))
        else :
            message_to_send += str(len(player[0].seeing_board.deck))
        ### copied the number of remaining decks
        ### message_to_send[8] ~ [9]

        for i in range(1,PLAYERNUMBER + 1):#自分の手札と相手の手札の情報
            for j in range(HANDNUM):
                message_to_send += player[0].seeing_board.phand[0][i][j].color
                message_to_send += str(player[0].seeing_board.phand[0][i][j].number)
        ### copied player hands 
        ### message_to_send[10] ~ [29]

        for i in range(1, PLAYERNUMBER + 1):#自分の手札と相手の手札の分かっている情報
            for j in range(HANDNUM):
                for k in range(5):
                    message_to_send += player[client['id']].seeing_board.prov_hand_PO[i][j][k].color
                    message_to_send += str(player[client['id']].seeing_board.prov_hand_PO[i][j][k].number)
        ### message_to_send[30] ~ [129]

        message_to_send += str(acting_player_i)#そのターン行動したプレイヤー
        ### message_to_send[130]
        message_to_send += act#(p or d or t) + 行動した数字
        ### message_to_send[131] ~ [133] + [134]()
        if len(args) == 5:
            try:
                with open("test.csv",mode='a') as log_file:
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
        ##writer.##writerow('a')
    else:
        print("player", player_index,"'s turn (Human)")
        ##writer.##writerow("b")
    print("fireworks :", end="")
    for j in range(len(player[0].seeing_board.fireworks)):#場の状況をprint
        player[0].seeing_board.fireworks[j].print_card()

    print("")
            
    print("blue tokens : ", player[0].seeing_board.blue_token)
    ##f.write("blue tokens : ", player[0].seeing_board.blue_token,'\n')
    print("red tokens", player[0].seeing_board.red_token)
    ##f.write("red tokens : ", player[0].seeing_board.red_token,'\n')

    for i in range(1,PLAYERNUMBER + 1):
        print("player",i,"'s hand :")#change
        # print("player",i,"'s hand :", end = "")
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

    gen_and_send_message(client['id'], message_to_send, "")#client['id]=1or2or..


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
    # print('message', message)# そのターンプレイヤーがなにをしたか't2W'→プレイヤー2に白のヒントを教えた
    if message[0] == 'D':
        print('difficult!')
        server.send_message(WebsocketServer.clients[2-int(message[1])],message)
        return
    
    
    if message[0] == 'T':
        message_to_send = 'order_mode' + message[6:]
        dup = gen_and_send_message(client['id'], message_to_send, message[4])
        if len(message_to_send) == 11:
            show_situation(client['id'], False)
        if dup == True:
            return
        print('message', message)

    message_to_send = ''
    
    act = ''
    ##print("Client(%d) said: %s" % (client['id'], message))
    if message[0] != 'T':
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
            with open('play_log'+str(PORT)+'.txt', mode='a') as f:
                f.write('player')
                f.write(str(client['id']))
                f.write(' played ')
                f.write(player[0].seeing_board.played_card.color)
                f.write(str(player[0].seeing_board.played_card.number))
                f.write('\n')
        

        elif message[0] == 'd':
            card_index = int(message[2])
            player[client['id']].act_num = 2
            act = 'd' + player[0].seeing_board.phand[0][client['id']][card_index - 1].color + str(player[0].seeing_board.phand[0][client['id']][card_index - 1].number) + str(card_index) 
            player[0].seeing_board.discarded_card = player[client['id']].pick_card(card_index)
            player[0].seeing_board.discard_processing()
            player[0].visible_hands_update()
            print('player1 discarded ',player[0].seeing_board.discarded_card.color,player[0].seeing_board.discarded_card.number)
            with open('play_log'+str(PORT)+'.txt', mode='a') as f:
                f.write('player')
                f.write(str(client['id']))
                f.write(' discarded ')
                f.write(player[0].seeing_board.discarded_card.color)
                f.write(str(player[0].seeing_board.discarded_card.number))
                f.write('\n')
            

        elif message[0] == 't' or message[0] == 'T':
            player[client['id']].act_num = 3
            p_index = int(message[2])
            if message[4] in ['1','2','3','4','5']:
                num_totell = int(message[4])
                act = 't' + str(p_index) + str(num_totell)
                player[client['id']].tell_number(num_totell,p_index, PORT)
                ##print('tellnum')
            elif message[4] in color_to_tell_list:
                char_to_tell = message[4]
                act = 't' + str(p_index) + char_to_tell
                player[client['id']].tell_color(char_to_tell,p_index, PORT)
                ##print('tellcolor')


        player[client['id']].thinking_time = time.time() - start_time
        print('Player thinking time is ',player[client['id']].thinking_time)
        print('')
        print('')
    player[client['id']].hands_PO_update()
    gen_and_send_message(client['id'], message_to_send, act)

    time.sleep(2.0)
    if player[2].is_agent == True:

        check_exit(2,message_to_send)
        show_situation(2,True)
        act = player[2].choice_act(message, PORT)
        with open('play_log'+str(PORT)+'.txt', mode='a') as f:
            if act[0] == 'p':
                f.write('player2 played ')
                f.write(act[1:3])
                f.write('\n')
            elif act[0] == 'd':
                f.write('player2 discarded ')
                f.write(act[1:3])
                f.write('\n')
        player[2].hands_PO_update()
        # if agentmode==1:
        #     if player[2].act_num==4:
        #         time.sleep(4.0)
        #         print('long long think')
        #     if player[2].act_num==5:
        #         time.sleep(6.0)
        #         print('long long long think')
        # if agentmode==2:
        #     if player[2].act_num==4:
        #         time.sleep(4.0)
        #         print('long think')
        #     if player[2].act_num==5:
        #         time.sleep(6.0)
        #         print('long long think')
        # if agentmode==3:
        #     t=random.random()
        #     print(t)
        #     if t>=0.72:
        #         time.sleep(6.0)
        #         print('random long long think')
        #     elif t>=0.59:
        #         time.sleep(4.0)
        #         print('random long think')                
                
        gen_and_send_message(2, message_to_send, act)

    check_exit(client['id'],message_to_send)
    start_time = time.time()

def main():
    server.set_fn_new_client(new_client) #クライアント接続時にnew_client関数を起動
    server.set_fn_client_left(client_left) #クライアント切断時にclient_left関数を起動
    server.set_fn_message_received(message_received) #クライアントからメッセージを受信したときにmessage_received関数を起動
    server.run_forever() #クライアント起動



if __name__ == "__main__":
    main()


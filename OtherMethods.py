import macro
from macro import PLAYERNUMBER
from macro import HANDNUM
from macro import color_list
from macro import player
import CardClass
import BoardClass
from PlayerClass import Player


def get_color_index(color):
    for color_index in range(len(color_list) - 1):
        if color == color_list[color_index]:
            return color_index

def visible_cards_init():
    for i in range(1, PLAYERNUMBER + 1):
        for j in range(HANDNUM):
            card = player[0].seeing_board.phand[0][i][j]
            for k in range(1,PLAYERNUMBER + 1):
                if i != k:
                    player[k].seeing_board.visible_cards_set[get_color_index(card.color)][card.number - 1] -= 1
    return


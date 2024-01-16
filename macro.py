### macro.py
### use like as macro...

import copy

SEARCHDEPTH = 0
PLAYERNUMBER = 2 
color_list = ["W","R","B","Y","G","_"]
color_to_tell_list = ["W","R","B","Y","G"]
player = []
turn = 2
if PLAYERNUMBER == 2 or PLAYERNUMBER == 3:
    HANDNUM = 5
else :
    HANDNUM = 4

hand_index = []
for i in range(HANDNUM):
    hand_index.append(i + 1)
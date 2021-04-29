# Matan Antebi
# 12.04.19
# ver 5.2

import socket, time, threading
import pygame as py

"""
==============================
CONSTANTS
==============================
"""
global my_deck
TURN = False
LEFT = 1
WIDTH = 800
HEIGHT = 800
SIZE = (WIDTH, HEIGHT)
WHITE = (255, 255, 255)
LEFT = 1
my_deck = []
# CARDS DEFINE
yaniv_on = py.image.load('yaniv-on.png')
yaniv_off = py.image.load('yaniv-off.png')

yaniv_on = py.transform.scale(yaniv_on, (96, 60))
yaniv_off = py.transform.scale(yaniv_off, (96, 60))

D1 = py.image.load('AD.png')
D2 = py.image.load('2D.png')
D3 = py.image.load('3D.png')
D4 = py.image.load('4D.png')
D5 = py.image.load('5D.png')
D6 = py.image.load('6D.png')
D7 = py.image.load('7D.png')
D8 = py.image.load('8D.png')
D9 = py.image.load('9D.png')
D10 = py.image.load('10D.png')
D11 = py.image.load('JD.png')
D12 = py.image.load('QD.png')
D13 = py.image.load('KD.png')

S1 = py.image.load('AS.png')
S2 = py.image.load('2S.png')
S3 = py.image.load('3S.png')
S4 = py.image.load('4S.png')
S5 = py.image.load('5S.png')
S6 = py.image.load('6S.png')
S7 = py.image.load('7S.png')
S8 = py.image.load('8S.png')
S9 = py.image.load('9S.png')
S10 = py.image.load('10S.png')
S11 = py.image.load('JS.png')
S12 = py.image.load('QS.png')
S13 = py.image.load('KS.png')

H1 = py.image.load('AH.png')
H2 = py.image.load('2H.png')
H3 = py.image.load('3H.png')
H4 = py.image.load('4H.png')
H5 = py.image.load('5H.png')
H6 = py.image.load('6H.png')
H7 = py.image.load('7H.png')
H8 = py.image.load('8H.png')
H9 = py.image.load('9H.png')
H10 = py.image.load('10H.png')
H11 = py.image.load('JH.png')
H12 = py.image.load('QH.png')
H13 = py.image.load('KH.png')

C1 = py.image.load('AC.png')
C2 = py.image.load('2C.png')
C3 = py.image.load('3C.png')
C4 = py.image.load('4C.png')
C5 = py.image.load('5C.png')
C6 = py.image.load('6C.png')
C7 = py.image.load('7C.png')
C8 = py.image.load('8C.png')
C9 = py.image.load('9C.png')
C10 = py.image.load('10C.png')
C11 = py.image.load('JC.png')
C12 = py.image.load('QC.png')
C13 = py.image.load('KC.png')

CARDS_5 = py.image.load('5cards.png')
CARDS_4 = py.image.load('4cards.png')
CARDS_3 = py.image.load('3cards.png')
CARDS_2 = py.image.load('2cards.png')
CARDS_1 = py.image.load('1card.png')

CARDS_5 = py.transform.scale(CARDS_5, (258, 180))
CARDS_4 = py.transform.scale(CARDS_4, (258, 180))
CARDS_3 = py.transform.scale(CARDS_3, (258, 180))
CARDS_2 = py.transform.scale(CARDS_2, (258, 180))
CARDS_1 = py.transform.scale(CARDS_1, (258, 180))

CARDS_5 = py.transform.rotate(CARDS_5, 180)
CARDS_4 = py.transform.rotate(CARDS_4, 180)
CARDS_3 = py.transform.rotate(CARDS_3, 180)
CARDS_2 = py.transform.rotate(CARDS_2, 180)
CARDS_1 = py.transform.rotate(CARDS_1, 180)

PICKED_CARD = py.image.load('PICKED_CARD.png')
CARD_BACK = py.image.load('blue_back.png')

CARDS_IMG = [D1, D2, D3, D4, D5, D6, D7, D8, D9, D10, D11, D12, D13,
             S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, S12,
             S13, H1, H2, H3, H4, H5, H6, H7, H8, H9, H10, H11, H12, H13,
             C1, C2, C3, C4, C5, C6, C7, C8, C9, C10, C11, C12, C13]

CARDS_IMG1 = [D1, D2, D3, D4, D5, D6, D7, D8, D9, D10, D11, D12, D13,
              S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, S12,
              S13, H1, H2, H3, H4, H5, H6, H7, H8, H9, H10, H11, H12, H13,
              C1, C2, C3, C4, C5, C6, C7, C8, C9, C10, C11, C12, C13]

print("len ", len(CARDS_IMG))

for i in range(len(CARDS_IMG)):
    CARDS_IMG[i] = py.transform.scale(CARDS_IMG[i], (115, 176))
    CARDS_IMG1[i] = py.transform.scale(CARDS_IMG1[i], (86, 132))
    CARDS_IMG1[i] = py.transform.rotate(CARDS_IMG1[i], 90)

PICKED_CARD = py.transform.scale(PICKED_CARD, (115, 176))
CARD_BACK = py.transform.scale(CARD_BACK, (103, 158))
CARD_BACK = py.transform.rotate(CARD_BACK, 90)
"""
==============================
Client
==============================
"""
my_socket = socket.socket()
port = 9999
host = '127.0.0.1'
my_socket.connect((host, port))
print("Connected !")
"""
==============================
Define Images
==============================
"""

def SendCardsCheck(cardlist):
    print("THE CHECK IS: ****", cardlist)
    is_samecard = True
    is_sequence = True
    # single card sending
    if len(cardlist) is 1:
        return True
    # same cards sending
    if len(cardlist) is not 1:
        tempcard = cardlist[0]
        for i in range(len(cardlist) - 1):
            if cardlist[i + 1][:-1] != tempcard[:-1]:
                print("FALSE BECAUSE ", cardlist[i + 1][:-1], "IS NOT ", tempcard[:-1])
                is_samecard = False
    # cards sequence sending
    if len(cardlist) > 2:
        print(cardlist)
        tempcard = cardlist[0]
        newlist = []
        for i in range(len(cardlist) - 1):
            if cardlist[i + 1][-1] is not tempcard[-1]:
                is_sequence = False
        for i in range(len(cardlist)):
            newlist.append(int(cardlist[i][:-1]))
        print(newlist)
        mini = min(newlist)
        newlist.remove(mini)
        print(newlist)
        for i in range(len(newlist)):
            print("min: ", mini)
            if min(newlist) != (mini + 1):
                is_sequence = False
            else:
                mini = min(newlist)
                newlist.remove(mini)
    else:
        is_sequence = False
    if is_sequence or is_samecard:
        return True
    return False


def Display_Deck(deck, numofplayers, lastKupa, can_yaniv):
    print("yaniv: ", can_yaniv)
    screen = py.display.set_mode(SIZE)
    bg = py.image.load('bg.jpg')
    bg = py.transform.scale(bg, (800, 800))
    screen.blit(bg, (0, 0))
    x = 115
    y = 800 - 176
    print("numofplayers: ", numofplayers)
    if numofplayers == 2:
        screen.blit(CARDS_5, (271, 0))
    if numofplayers == 3:
        tcard = py.transform.rotate(CARDS_5, 90)
        screen.blit(tcard, (0, 271))
        screen.blit(CARDS_5, (271, 0))
    if numofplayers == 4:
        tcard = py.transform.rotate(CARDS_5, 90)
        tcard2 = py.transform.rotate(CARDS_5, 270)
        screen.blit(tcard, (0, 271))
        screen.blit(CARDS_5, (271, 0))
        screen.blit(tcard2, (620, 271))

    if can_yaniv:
        screen.blit(yaniv_on, (697, y))
    else:
        screen.blit(yaniv_off, (697, y))

    for i in range(len(deck)):
        if "1D" == deck[i]:
            screen.blit(CARDS_IMG[0], (x, y))
            x += 115
        if "2D" == deck[i]:
            screen.blit(CARDS_IMG[1], (x, y))
            x += 115
        if "3D" == deck[i]:
            screen.blit(CARDS_IMG[2], (x, y))
            x += 115
        if "4D" == deck[i]:
            screen.blit(CARDS_IMG[3], (x, y))
            x += 115
        if "5D" == deck[i]:
            screen.blit(CARDS_IMG[4], (x, y))
            x += 115
        if "6D" == deck[i]:
            screen.blit(CARDS_IMG[5], (x, y))
            x += 115
        if "7D" == deck[i]:
            screen.blit(CARDS_IMG[6], (x, y))
            x += 115
        if "8D" == deck[i]:
            screen.blit(CARDS_IMG[7], (x, y))
            x += 115
        if "9D" == deck[i]:
            screen.blit(CARDS_IMG[8], (x, y))
            x += 115
        if "10D" == deck[i]:
            screen.blit(CARDS_IMG[9], (x, y))
            x += 115
        if "11D" == deck[i]:
            screen.blit(CARDS_IMG[10], (x, y))
            x += 115
        if "12D" == deck[i]:
            screen.blit(CARDS_IMG[11], (x, y))
            x += 115
        if "13D" == deck[i]:
            screen.blit(CARDS_IMG[12], (x, y))
            x += 115
        if "1S" == deck[i]:
            screen.blit(CARDS_IMG[13], (x, y))
            x += 115
        if "2S" == deck[i]:
            screen.blit(CARDS_IMG[14], (x, y))
            x += 115
        if "3S" == deck[i]:
            screen.blit(CARDS_IMG[15], (x, y))
            x += 115
        if "4S" == deck[i]:
            screen.blit(CARDS_IMG[16], (x, y))
            x += 115
        if "5S" == deck[i]:
            screen.blit(CARDS_IMG[17], (x, y))
            x += 115
        if "6S" == deck[i]:
            screen.blit(CARDS_IMG[18], (x, y))
            x += 115
        if "7S" == deck[i]:
            screen.blit(CARDS_IMG[19], (x, y))
            x += 115
        if "8S" == deck[i]:
            screen.blit(CARDS_IMG[20], (x, y))
            x += 115
        if "9S" == deck[i]:
            screen.blit(CARDS_IMG[21], (x, y))
            x += 115
        if "10S" == deck[i]:
            screen.blit(CARDS_IMG[22], (x, y))
            x += 115
        if "11S" == deck[i]:
            screen.blit(CARDS_IMG[23], (x, y))
            x += 115
        if "12S" == deck[i]:
            screen.blit(CARDS_IMG[24], (x, y))
            x += 115
        if "13S" == deck[i]:
            screen.blit(CARDS_IMG[25], (x, y))
            x += 115
        if "1H" == deck[i]:
            screen.blit(CARDS_IMG[26], (x, y))
            x += 115
        if "2H" == deck[i]:
            screen.blit(CARDS_IMG[27], (x, y))
            x += 115
        if "3H" == deck[i]:
            screen.blit(CARDS_IMG[28], (x, y))
            x += 115
        if "4H" == deck[i]:
            screen.blit(CARDS_IMG[29], (x, y))
            x += 115
        if "5H" == deck[i]:
            screen.blit(CARDS_IMG[30], (x, y))
            x += 115
        if "6H" == deck[i]:
            screen.blit(CARDS_IMG[31], (x, y))
            x += 115
        if "7H" == deck[i]:
            screen.blit(CARDS_IMG[32], (x, y))
            x += 115
        if "8H" == deck[i]:
            screen.blit(CARDS_IMG[33], (x, y))
            x += 115
        if "9H" == deck[i]:
            screen.blit(CARDS_IMG[34], (x, y))
            x += 115
        if "10H" == deck[i]:
            screen.blit(CARDS_IMG[35], (x, y))
            x += 115
        if "11H" == deck[i]:
            screen.blit(CARDS_IMG[36], (x, y))
            x += 115
        if "12H" == deck[i]:
            screen.blit(CARDS_IMG[37], (x, y))
            x += 115
        if "13H" == deck[i]:
            screen.blit(CARDS_IMG[38], (x, y))
            x += 115
        if "1C" == deck[i]:
            screen.blit(CARDS_IMG[39], (x, y))
            x += 115
        if "2C" == deck[i]:
            screen.blit(CARDS_IMG[40], (x, y))
            x += 115
        if "3C" == deck[i]:
            screen.blit(CARDS_IMG[41], (x, y))
            x += 115
        if "4C" == deck[i]:
            screen.blit(CARDS_IMG[42], (x, y))
            x += 115
        if "5C" == deck[i]:
            screen.blit(CARDS_IMG[43], (x, y))
            x += 115
        if "6C" == deck[i]:
            screen.blit(CARDS_IMG[44], (x, y))
            x += 115
        if "7C" == deck[i]:
            screen.blit(CARDS_IMG[45], (x, y))
            x += 115
        if "8C" == deck[i]:
            screen.blit(CARDS_IMG[46], (x, y))
            x += 115
        if "9C" == deck[i]:
            screen.blit(CARDS_IMG[47], (x, y))
            x += 115
        if "10C" == deck[i]:
            screen.blit(CARDS_IMG[48], (x, y))
            x += 115
        if "11C" == deck[i]:
            screen.blit(CARDS_IMG[49], (x, y))
            x += 115
        if "12C" == deck[i]:
            screen.blit(CARDS_IMG[50], (x, y))
            x += 115
        if "13C" == deck[i]:
            screen.blit(CARDS_IMG[51], (x, y))
            x += 115

    x2 = 290
    y2 = 350
    TempKupa = lastKupa
    for i in range(len(TempKupa)):
        if "1D" == TempKupa[i]:
            screen.blit(CARDS_IMG1[0], (x2, y2))
            x2 += 132
        if "2D" == TempKupa[i]:
            screen.blit(CARDS_IMG1[1], (x2, y2))
            x2 += 132
        if "3D" == TempKupa[i]:
            screen.blit(CARDS_IMG1[2], (x2, y2))
            x2 += 132
        if "4D" == TempKupa[i]:
            screen.blit(CARDS_IMG1[3], (x2, y2))
            x2 += 132
        if "5D" == TempKupa[i]:
            screen.blit(CARDS_IMG1[4], (x2, y2))
            x2 += 132
        if "6D" == TempKupa[i]:
            screen.blit(CARDS_IMG1[5], (x2, y2))
            x2 += 132
        if "7D" == TempKupa[i]:
            screen.blit(CARDS_IMG1[6], (x2, y2))
            x2 += 132
        if "8D" == TempKupa[i]:
            screen.blit(CARDS_IMG1[7], (x2, y2))
            x2 += 132
        if "9D" == TempKupa[i]:
            screen.blit(CARDS_IMG1[8], (x2, y2))
            x2 += 132
        if "10D" == TempKupa[i]:
            screen.blit(CARDS_IMG1[9], (x2, y2))
            x2 += 132
        if "11D" == TempKupa[i]:
            screen.blit(CARDS_IMG1[10], (x2, y2))
            x2 += 132
        if "12D" == TempKupa[i]:
            screen.blit(CARDS_IMG1[11], (x2, y2))
            x2 += 132
        if "13D" == TempKupa[i]:
            screen.blit(CARDS_IMG1[12], (x2, y2))
            x2 += 132
        if "1S" == TempKupa[i]:
            screen.blit(CARDS_IMG1[13], (x2, y2))
            x2 += 132
        if "2S" == TempKupa[i]:
            screen.blit(CARDS_IMG1[14], (x2, y2))
            x2 += 132
        if "3S" == TempKupa[i]:
            screen.blit(CARDS_IMG1[15], (x2, y2))
            x2 += 132
        if "4S" == TempKupa[i]:
            screen.blit(CARDS_IMG1[16], (x2, y2))
            x2 += 132
        if "5S" == TempKupa[i]:
            screen.blit(CARDS_IMG1[17], (x2, y2))
            x2 += 132
        if "6S" == TempKupa[i]:
            screen.blit(CARDS_IMG1[18], (x2, y2))
            x2 += 132
        if "7S" == TempKupa[i]:
            screen.blit(CARDS_IMG1[19], (x2, y2))
            x2 += 132
        if "8S" == TempKupa[i]:
            screen.blit(CARDS_IMG1[20], (x2, y2))
            x2 += 132
        if "9S" == TempKupa[i]:
            screen.blit(CARDS_IMG1[21], (x2, y2))
            x2 += 132
        if "10S" == TempKupa[i]:
            screen.blit(CARDS_IMG1[22], (x2, y2))
            x2 += 132
        if "11S" == TempKupa[i]:
            screen.blit(CARDS_IMG1[23], (x2, y2))
            x2 += 132
        if "12S" == TempKupa[i]:
            screen.blit(CARDS_IMG1[24], (x2, y2))
            x2 += 132
        if "13S" == TempKupa[i]:
            screen.blit(CARDS_IMG1[25], (x2, y2))
            x2 += 132
        if "1H" == TempKupa[i]:
            screen.blit(CARDS_IMG1[26], (x2, y2))
            x2 += 132
        if "2H" == TempKupa[i]:
            screen.blit(CARDS_IMG1[27], (x2, y2))
            x2 += 132
        if "3H" == TempKupa[i]:
            screen.blit(CARDS_IMG1[28], (x2, y2))
            x2 += 132
        if "4H" == TempKupa[i]:
            screen.blit(CARDS_IMG1[29], (x2, y2))
            x2 += 132
        if "5H" == TempKupa[i]:
            screen.blit(CARDS_IMG1[30], (x2, y2))
            x2 += 132
        if "6H" == TempKupa[i]:
            screen.blit(CARDS_IMG1[31], (x2, y2))
            x2 += 132
        if "7H" == TempKupa[i]:
            screen.blit(CARDS_IMG1[32], (x2, y2))
            x2 += 132
        if "8H" == TempKupa[i]:
            screen.blit(CARDS_IMG1[33], (x2, y2))
            x2 += 132
        if "9H" == TempKupa[i]:
            screen.blit(CARDS_IMG1[34], (x2, y2))
            x2 += 132
        if "10H" == TempKupa[i]:
            screen.blit(CARDS_IMG1[35], (x2, y2))
            x2 += 132
        if "11H" == TempKupa[i]:
            screen.blit(CARDS_IMG1[36], (x2, y2))
            x2 += 132
        if "12H" == TempKupa[i]:
            screen.blit(CARDS_IMG1[37], (x2, y2))
            x2 += 132
        if "13H" == TempKupa[i]:
            screen.blit(CARDS_IMG1[38], (x2, y2))
            x2 += 132
        if "1C" == TempKupa[i]:
            screen.blit(CARDS_IMG1[39], (x2, y2))
            x2 += 132
        if "2C" == TempKupa[i]:
            screen.blit(CARDS_IMG1[40], (x2, y2))
            x2 += 132
        if "3C" == TempKupa[i]:
            screen.blit(CARDS_IMG1[41], (x2, y2))
            x2 += 132
        if "4C" == TempKupa[i]:
            screen.blit(CARDS_IMG1[42], (x2, y2))
            x2 += 132
        if "5C" == TempKupa[i]:
            screen.blit(CARDS_IMG1[43], (x2, y2))
            x2 += 132
        if "6C" == TempKupa[i]:
            screen.blit(CARDS_IMG1[44], (x2, y2))
            x2 += 132
        if "7C" == TempKupa[i]:
            screen.blit(CARDS_IMG1[45], (x2, y2))
            x2 += 132
        if "8C" == TempKupa[i]:
            screen.blit(CARDS_IMG1[46], (x2, y2))
            x2 += 132
        if "9C" == TempKupa[i]:
            screen.blit(CARDS_IMG1[47], (x2, y2))
            x2 += 132
        if "10C" == TempKupa[i]:
            screen.blit(CARDS_IMG1[48], (x2, y2))
            x2 += 132
        if "11C" == TempKupa[i]:
            screen.blit(CARDS_IMG1[49], (x2, y2))
            x2 += 132
        if "12C" == TempKupa[i]:
            screen.blit(CARDS_IMG1[50], (x2, y2))
            x2 += 132
        if "13C" == TempKupa[i]:
            screen.blit(CARDS_IMG1[51], (x2, y2))
            x2 += 132

    screen.blit(CARD_BACK, (321, 230))
    py.display.flip()
    print(x)


def StartCards():
    # StartCards
    my_socket.send(bytes("StartCards", 'utf-8'))
    pack = my_socket.recv(1024).decode('utf-8')
    my_deck = pack.split()
    print(my_deck)
    return my_deck


def PickCard(x, y, screen, my_deck, TempCardsPick, lastKupa, is_yaniv):
    print(x, y)
    print(my_deck)
    Choice = ""
    deck_length = len(my_deck)
    print("LENGTH: ", deck_length)
    if (deck_length > 0) and (115 < x < 230) and ((800 - 176) < y < 800) and (my_deck[0] not in TempCardsPick):
        screen.blit(PICKED_CARD, (115, 800 - 176))
        TempCardsPick.append(my_deck[0])
    if (deck_length > 1) and (115 * 2 < x < 230 + 115) and ((800 - 176) < y < 800) and (
            my_deck[1] not in TempCardsPick):
        screen.blit(PICKED_CARD, (115 * 2, 800 - 176))
        TempCardsPick.append(my_deck[1])
    if (deck_length > 2) and (115 * 3 < x < 230 + 115 * 2) and ((800 - 176) < y < 800) and (
            my_deck[2] not in TempCardsPick):
        screen.blit(PICKED_CARD, (115 * 3, 800 - 176))
        TempCardsPick.append(my_deck[2])
    if (deck_length > 3) and (115 * 4 < x < 230 + 115 * 3) and ((800 - 176) < y < 800) and (
            my_deck[3] not in TempCardsPick):
        screen.blit(PICKED_CARD, (115 * 4, 800 - 176))
        TempCardsPick.append(my_deck[3])
    if (deck_length > 4) and (115 * 5 < x < 230 + 115 * 4) and ((800 - 176) < y < 800) and (
            my_deck[4] not in TempCardsPick):
        screen.blit(PICKED_CARD, (115 * 5, 800 - 176))
        TempCardsPick.append(my_deck[4])
    if (321 < x < 321 + 158) and (230 < y < 230 + 103) and len(TempCardsPick) != 0:
        Choice = "KUPA"
    if (697 < x < 697 + 96) and (624 < y < 624 + 60) and is_yaniv:
        Choice = "YANIV"
    if len(lastKupa) == 1:
        if (290 < x < 290 + 132) and (350 < y < 350 + 86):
            Choice = "LASTCARD 0"
    if len(lastKupa) == 2:
        if (290 < x < 290 + 132) and (350 < y < 350 + 86):
            Choice = "LASTCARD 0"
        elif (290 + 132 < x < 290 + 132 * 2) and (350 < y < 350 + 86):
            Choice = "LASTCARD 1"
    if len(lastKupa) == 3:
        if (290 < x < 290 + 132) and (350 < y < 350 + 86):
            Choice = "LASTCARD 0"
        elif (290 + 132 < x < 290 + 132 * 2) and (350 < y < 350 + 86):
            Choice = "LASTCARD 1"
        elif (290 + 132 * 2 < x < 290 + 132 * 3) and (350 < y < 350 + 86):
            Choice = "LASTCARD 2"
    if len(lastKupa) == 4:
        if (290 < x < 290 + 132) and (350 < y < 350 + 86):
            Choice = "LASTCARD 0"
        elif (290 + 132 < x < 290 + 132 * 2) and (350 < y < 350 + 86):
            Choice = "LASTCARD 1"
        elif (290 + 132 * 2 < x < 290 + 132 * 3) and (350 < y < 350 + 86):
            Choice = "LASTCARD 2"
        elif (290 + 132 * 3 < x < 290 + 132 * 4) and (350 < y < 350 + 86):
            Choice = "LASTCARD 3"
    if len(lastKupa) == 5:
        if (290 < x < 290 + 132) and (350 < y < 350 + 86):
            Choice = "LASTCARD 0"
        elif (290 + 132 < x < 290 + 132 * 2) and (350 < y < 350 + 86):
            Choice = "LASTCARD 1"
        elif (290 + 132 * 2 < x < 290 + 132 * 3) and (350 < y < 350 + 86):
            Choice = "LASTCARD 2"
        elif (290 + 132 * 3 < x < 290 + 132 * 4) and (350 < y < 350 + 86):
            Choice = "LASTCARD 3"
        elif (290 + 132 * 4 < x < 290 + 132 * 5) and (350 < y < 350 + 86):
            Choice = "LASTCARD 4"

    py.display.flip()
    return TempCardsPick, Choice


def ListToString(list):
    str = ""
    for i in range(len(list)):
        str += list[i] + " "
    return str

def SumCards(my_deck):
    sum = 0
    for i in range(len(my_deck)):
        sum += int(my_deck[i][:-1])
    return sum

def You_Win():
    print("WINNERRRRRRRRRRR")

def Asaf():
    print("ASAF!")

def Game(myIndex, numofplayers, lastKupa):
    can_yaniv = False
    print("ipasti kupa")
    myTurn = False
    screen = py.display.set_mode(SIZE)
    bg = py.image.load('bg.jpg')
    bg = py.transform.scale(bg, (800, 800))
    screen.blit(bg, (0, 0))
    py.display.flip()
    fin = False
    my_deck = StartCards()
    Display_Deck(my_deck, numofplayers, lastKupa, can_yaniv)
    TempCardsPick = []
    if myIndex == 0:
        myTurn = True
    while not fin:
        for event in py.event.get():
            if event.type == py.QUIT:
                fin = True
            if (event.type == py.MOUSEBUTTONDOWN) and myTurn:
                if event.button == LEFT:
                    mouse_point = py.mouse.get_pos()
                    x, y = mouse_point
                    TempCardsPick, Choice = PickCard(x, y, screen, my_deck, TempCardsPick, lastKupa, can_yaniv)
                    if Choice == "KUPA":
                        print("the pick >>>", TempCardsPick)
                        if SendCardsCheck(TempCardsPick) is True:
                            lastKupa = TempCardsPick
                            str = "Kupa " + ListToString(TempCardsPick)
                            my_socket.send(bytes(str, 'utf-8'))
                            card = my_socket.recv(1024).decode('utf-8')
                            print("NEW CARD FROM KUPA IS: ", card)
                            for i in range(len(TempCardsPick)):
                                if TempCardsPick[i] in my_deck:
                                    my_deck.remove(TempCardsPick[i])
                                    print("new deck", my_deck)
                            my_deck.append(card)
                            Display_Deck(my_deck, numofplayers, lastKupa, can_yaniv)
                            TempCardsPick.clear()
                            decktosend = "mydeck "
                            decktosend += ListToString(my_deck)
                            my_socket.send(bytes(decktosend, 'utf-8'))
                            my_socket.send(bytes("finished", 'utf-8'))
                            myTurn = False
                        else:
                            print("WRONG PICK!")
                            Display_Deck(my_deck, numofplayers, lastKupa, can_yaniv)
                            TempCardsPick.clear()
                    if "LASTCARD" in Choice:
                        if SendCardsCheck(TempCardsPick) is True:
                            str = "Last " + ListToString(TempCardsPick) + " " + lastKupa[int(Choice[-1])]
                            my_socket.send(bytes(str, 'utf-8'))
                            card = my_socket.recv(1024).decode('utf-8')
                            print("NEW CARD FROM KUPA IS: ", card)
                            for i in range(len(TempCardsPick)):
                                if TempCardsPick[i] in my_deck:
                                    my_deck.remove(TempCardsPick[i])
                                    print("new deck", my_deck)
                            my_deck.append(card)
                            lastKupa = TempCardsPick
                            Display_Deck(my_deck, numofplayers, lastKupa, can_yaniv)
                            TempCardsPick.clear()
                            decktosend = "mydeck "
                            decktosend += ListToString(my_deck)
                            my_socket.send(bytes(decktosend, 'utf-8'))
                            my_socket.send(bytes("finished", 'utf-8'))
                            myTurn = False
                        else:
                            print("WRONG PICK!")
                            Display_Deck(my_deck, numofplayers, lastKupa, can_yaniv)
                            TempCardsPick.clear()
                    if Choice == "YANIV":
                        decktosend = "mydeck "
                        decktosend += ListToString(my_deck)
                        my_socket.send(bytes(decktosend, 'utf-8'))
                        my_socket.send(bytes("YANIV", 'utf-8'))
                        result = my_socket.recv(1024).decode('utf-8')
                        if result == "win":
                            You_Win()
                        elif result == "asaf":
                            Asaf()

            if not myTurn:
                try:
                    my_socket.settimeout(0.5)
                    data = my_socket.recv(1024).decode('utf-8')
                    print("now i am ready ", data)
                    tempush = data.split()
                    turn = tempush[0]
                    del tempush[0]
                    if turn == "yourturn":
                        if SumCards(my_deck) < 8:
                            can_yaniv = True
                        else:
                            can_yaniv = False
                        lastKupa = tempush
                        Display_Deck(my_deck, numofplayers, lastKupa, can_yaniv)
                        myTurn = True
                        print("sum deck: ", SumCards(my_deck))
                    if turn == "notturn":
                        lastKupa = tempush
                        Display_Deck(my_deck, numofplayers, lastKupa, can_yaniv)
                except socket.timeout:
                    continue


def main():
    myIndex = int(my_socket.recv(1024).decode('utf-8'))
    print("my index: ", myIndex)
    numofplayers = int(my_socket.recv(1024).decode('utf-8'))
    print("timeout: ", my_socket.gettimeout())
    lastKupa = my_socket.recv(1024).decode('utf-8')
    print("LASTTTFRTYGRGIU4HIUH5UI ", lastKupa)
    lastKupa = lastKupa.split()
    py.init()
    Game(myIndex, numofplayers, lastKupa)


"""
Open rules page and wait for mouse input 
"""
if __name__ == '__main__':
    main()



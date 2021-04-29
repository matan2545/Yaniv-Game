# Matan Antebi
# 12.04.19
# ver 5.2

import socket, time, threading
import pygame as py
from tkinter import *
import sqlite3

"""
==============================
CONSTANTS
==============================
"""
global my_user
global LoggedIn
LoggedIn = False
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

YANIV = py.image.load('YANIV.png')
ASAF = py.image.load('ASAF.png')

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
#print("Connected !")
"""
==============================
Define Images
==============================
"""


class Users:
    def add_user(self, username, password):
        tosend = "register " + username + " " + password
        my_socket.send(bytes(tosend, 'utf-8'))
        answer = my_socket.recv(1024).decode('utf-8')
        #print("1111111111111111111  ", answer)
        return answer

    def login_user(self, username, password):
        tosend = "login " + username + " " + password
        my_socket.send(bytes(tosend, 'utf-8'))
        answer = my_socket.recv(1024).decode('utf-8')
        #print("1111111111111111111  ", answer)
        return answer

    def update_score(self, username, toadd):
        tosend = "score " + username + " " + str(toadd)
        my_socket.send(bytes(tosend, 'utf-8'))
        answer = my_socket.recv(1024).decode('utf-8')
        new_caption = username + " correct score: " + answer
        py.display.set_caption(new_caption)


class LoginFrame(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.label_username = Label(self, text="Username")
        self.label_password = Label(self, text="Password")

        self.entry_username = Entry(self)
        self.entry_password = Entry(self, show="*")

        self.label_username.grid(row=0, sticky=E)
        self.label_password.grid(row=1, sticky=E)
        self.entry_username.grid(row=0, column=1)
        self.entry_password.grid(row=1, column=1)
        self.puki = Label(self, text="")
        self.puki.grid(columnspan=2)

        self.logbtn = Button(self, text="Login", command=self._login_btn_clicked)
        self.logbtn.grid(columnspan=2)

        self.logbtn = Button(self, text="Register", command=self._register_btn_clicked)
        self.logbtn.grid(columnspan=2)

        self.pack()

    def _login_btn_clicked(self):
        # #print("Clicked")
        username = self.entry_username.get()
        password = self.entry_password.get()

        #print(username, password)
        answer = Users.login_user(username, username, password)
        if answer == "True":
            #print("logging in")
            global LoggedIn
            global my_user
            #print("log", LoggedIn)
            LoggedIn = True
            my_user = username
            self.quit()
        elif answer == "False":
            self.puki['text'] = "Incorrect password"
            #print("Incorrect password")
        else:
            #print("Try again")
            self.puki['text'] = "Please try again"
        #print("login", username, password)

    def _register_btn_clicked(self):
        # #print("Clicked")
        username = self.entry_username.get()
        password = self.entry_password.get()

        # #print(username, password)
        answer = Users.add_user(username, username, password)
        self.puki['text'] = answer


def SendCardsCheck(cardlist):
    #print("THE CHECK IS: ****", cardlist)
    try:
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
                    #print("FALSE BECAUSE ", cardlist[i + 1][:-1], "IS NOT ", tempcard[:-1])
                    is_samecard = False
        # cards sequence sending
        if len(cardlist) > 2:
            #print(cardlist)
            tempcard = cardlist[0]
            newlist = []
            for i in range(len(cardlist) - 1):
                if cardlist[i + 1][-1] is not tempcard[-1]:
                    is_sequence = False
            for i in range(len(cardlist)):
                newlist.append(int(cardlist[i][:-1]))
            #print(newlist)
            mini = min(newlist)
            newlist.remove(mini)
            #print(newlist)
            for i in range(len(newlist)):
                #print("min: ", mini)
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
    except:
        return False

def Display_Deck(deck, numofplayers, lastKupa, can_yaniv, sums=[], myindex=0):
    #print("yaniv: ", can_yaniv)
    screen = py.display.set_mode(SIZE)
    bg = py.image.load('bg.jpg')
    bg = py.transform.scale(bg, (800, 800))
    screen.blit(bg, (0, 0))
    x = 115
    y = 800 - 176
    #print("numofplayers: ", numofplayers)
    if len(sums) != 0:
        if numofplayers == 2:
            py.font.init()
            myfont = py.font.SysFont('Comic Sans MS', 30)
            if myindex == 0:
                textsurface = myfont.render(str(sums[0]), False, (0, 0, 0))
                screen.blit(textsurface, (380, 560))
                textsurface = myfont.render(str(sums[1]), False, (0, 0, 0))
                screen.blit(textsurface, (380, 180))
            elif myindex == 1:
                textsurface = myfont.render(str(sums[1]), False, (0, 0, 0))
                screen.blit(textsurface, (380, 560))
                textsurface = myfont.render(str(sums[0]), False, (0, 0, 0))
                screen.blit(textsurface, (380, 180))
        elif numofplayers == 3:
            py.font.init()
            myfont = py.font.SysFont('Comic Sans MS', 30)
            if myindex == 0:
                textsurface = myfont.render(str(sums[0]), False, (0, 0, 0))
                screen.blit(textsurface, (380, 560))
                textsurface = myfont.render(str(sums[1]), False, (0, 0, 0))
                screen.blit(textsurface, (380, 180))
                textsurface = myfont.render(str(sums[2]), False, (0, 0, 0))
                screen.blit(textsurface, (200, 400))
            elif myindex == 1:
                textsurface = myfont.render(str(sums[1]), False, (0, 0, 0))
                screen.blit(textsurface, (380, 560))
                textsurface = myfont.render(str(sums[2]), False, (0, 0, 0))
                screen.blit(textsurface, (380, 180))
                textsurface = myfont.render(str(sums[0]), False, (0, 0, 0))
                screen.blit(textsurface, (200, 400))
            elif myindex == 2:
                textsurface = myfont.render(str(sums[2]), False, (0, 0, 0))
                screen.blit(textsurface, (380, 560))
                textsurface = myfont.render(str(sums[0]), False, (0, 0, 0))
                screen.blit(textsurface, (380, 180))
                textsurface = myfont.render(str(sums[1]), False, (0, 0, 0))
                screen.blit(textsurface, (200, 400))
        elif numofplayers == 4:
            py.font.init()
            myfont = py.font.SysFont('Comic Sans MS', 30)
            if myindex == 0:
                textsurface = myfont.render(str(sums[0]), False, (0, 0, 0))
                screen.blit(textsurface, (380, 560))
                textsurface = myfont.render(str(sums[1]), False, (0, 0, 0))
                screen.blit(textsurface, (690, 400))
                textsurface = myfont.render(str(sums[2]), False, (0, 0, 0))
                screen.blit(textsurface, (380, 180))
                textsurface = myfont.render(str(sums[3]), False, (0, 0, 0))
                screen.blit(textsurface, (200, 400))
            elif myindex == 1:
                textsurface = myfont.render(str(sums[1]), False, (0, 0, 0))
                screen.blit(textsurface, (380, 560))
                textsurface = myfont.render(str(sums[2]), False, (0, 0, 0))
                screen.blit(textsurface, (690, 400))
                textsurface = myfont.render(str(sums[3]), False, (0, 0, 0))
                screen.blit(textsurface, (380, 180))
                textsurface = myfont.render(str(sums[0]), False, (0, 0, 0))
                screen.blit(textsurface, (200, 400))
            elif myindex == 2:
                textsurface = myfont.render(str(sums[2]), False, (0, 0, 0))
                screen.blit(textsurface, (380, 560))
                textsurface = myfont.render(str(sums[3]), False, (0, 0, 0))
                screen.blit(textsurface, (690, 400))
                textsurface = myfont.render(str(sums[0]), False, (0, 0, 0))
                screen.blit(textsurface, (380, 180))
                textsurface = myfont.render(str(sums[1]), False, (0, 0, 0))
                screen.blit(textsurface, (200, 400))
            elif myindex == 3:
                textsurface = myfont.render(str(sums[3]), False, (0, 0, 0))
                screen.blit(textsurface, (380, 560))
                textsurface = myfont.render(str(sums[0]), False, (0, 0, 0))
                screen.blit(textsurface, (690, 400))
                textsurface = myfont.render(str(sums[1]), False, (0, 0, 0))
                screen.blit(textsurface, (380, 180))
                textsurface = myfont.render(str(sums[2]), False, (0, 0, 0))
                screen.blit(textsurface, (200, 400))
    if numofplayers == 2:
        my_socket.send(bytes("NUMCARDS2", 'utf-8'))
        numtemp = int(my_socket.recv(4).decode('utf-8'))
        if numtemp == 5:
            screen.blit(CARDS_5, (271, 0))
        elif numtemp == 4:
            screen.blit(CARDS_4, (271, 0))
        elif numtemp == 3:
            screen.blit(CARDS_3, (271, 0))
        elif numtemp == 2:
            screen.blit(CARDS_2, (271, 0))
        elif numtemp == 1:
            screen.blit(CARDS_1, (271, 0))
    if numofplayers == 3:
        my_socket.send(bytes("NUMCARDS3", 'utf-8'))
        numtemp1 = int(my_socket.recv(4).decode('utf-8'))
        numtemp2 = int(my_socket.recv(4).decode('utf-8'))
        if numtemp1 == 5:
            tcard = py.transform.rotate(CARDS_5, 90)
            screen.blit(tcard, (0, 271))
        elif numtemp1 == 4:
            tcard = py.transform.rotate(CARDS_4, 90)
            screen.blit(tcard, (0, 271))
        elif numtemp1 == 3:
            tcard = py.transform.rotate(CARDS_3, 90)
            screen.blit(tcard, (0, 271))
        elif numtemp1 == 2:
            tcard = py.transform.rotate(CARDS_2, 90)
            screen.blit(tcard, (0, 271))
        elif numtemp1 == 1:
            tcard = py.transform.rotate(CARDS_1, 90)
            screen.blit(tcard, (0, 271))

        if numtemp2 == 5:
            screen.blit(CARDS_5, (271, 0))
        elif numtemp2 == 4:
            screen.blit(CARDS_4, (271, 0))
        elif numtemp2 == 3:
            screen.blit(CARDS_3, (271, 0))
        elif numtemp2 == 2:
            screen.blit(CARDS_2, (271, 0))
        elif numtemp2 == 1:
            screen.blit(CARDS_1, (271, 0))

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
        tempstr = deck[i] + ".png"
        tmp = py.image.load(tempstr)
        tmp = py.transform.scale(tmp, (115, 176))
        screen.blit(tmp, (x, y))
        x += 115

    x2 = 290
    y2 = 350
    TempKupa = lastKupa

    for i in range(len(TempKupa)):
        tempstr = TempKupa[i] + ".png"
        tmp = py.image.load(tempstr)
        tmp = py.transform.scale(tmp, (86, 132))
        tmp = py.transform.rotate(tmp, 90)
        screen.blit(tmp, (x2, y2))
        x2 += 132

    screen.blit(CARD_BACK, (321, 230))
    py.display.flip()
    #print(x)


def StartCards():
    # StartCards
    my_socket.send(bytes("StartCards", 'utf-8'))
    pack = my_socket.recv(1024).decode('utf-8')
    my_deck = pack.split()
    #print(my_deck)
    return my_deck


def PickCard(x, y, screen, my_deck, TempCardsPick, lastKupa, is_yaniv):
    #print(x, y)
    #print(my_deck)
    Choice = ""
    deck_length = len(my_deck)
    #print("LENGTH: ", deck_length)
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
    py.display.set_caption('YOU WON!')
    Users.update_score(my_user, my_user, 1)
    #print("WINNERRRRRRRRRRR")


def Asaf():
    py.display.set_caption('ASAF!')
    Users.update_score(my_user, my_user, -1)
    #print("ASAF!")


def get_sums():
    #print("before<<<<<<<<<<<<<<<<<")
    data = my_socket.recv(2048).decode('utf-8')
    #print("after<<<<<<<<<<<<<<<<<")
    str_sum = data.split()
    #print("the sums are: ", str_sum)
    return str_sum


def end_game():
    time.sleep(3)
    my_socket.send(bytes("exit", 'utf-8'))
    py.quit()
    my_socket.close()


def Game(myIndex, numofplayers, lastKupa):
    can_yaniv = False
    winner_yaniv = False
    winner_asaf = False
    #print("ipasti kupa")
    myTurn = False
    cap = my_user + " WAITING FOR YOUR TURN . . ."
    cap2 = my_user + " YOUR TURN!"
    cap3 = my_user + " You Lost!"
    py.display.set_caption(cap)
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
        py.display.set_caption(cap2)
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
                        #print("the pick >>>", TempCardsPick)
                        if SendCardsCheck(TempCardsPick) is True:
                            lastKupa = TempCardsPick
                            str = "Kupa " + ListToString(TempCardsPick)
                            my_socket.send(bytes(str, 'utf-8'))
                            card = my_socket.recv(1024).decode('utf-8')
                            #print("NEW CARD FROM KUPA IS: ", card)
                            for i in range(len(TempCardsPick)):
                                if TempCardsPick[i] in my_deck:
                                    my_deck.remove(TempCardsPick[i])
                                    #print("new deck", my_deck)
                            my_deck.append(card)
                            Display_Deck(my_deck, numofplayers, lastKupa, can_yaniv)
                            TempCardsPick.clear()
                            decktosend = "mydeck "
                            decktosend += ListToString(my_deck)
                            my_socket.send(bytes(decktosend, 'utf-8'))
                            my_socket.send(bytes("finished", 'utf-8'))
                            myTurn = False
                            py.display.set_caption(cap)
                        else:
                            #print("WRONG PICK!")
                            Display_Deck(my_deck, numofplayers, lastKupa, can_yaniv)
                            TempCardsPick.clear()
                    if "LASTCARD" in Choice:
                        if SendCardsCheck(TempCardsPick) is True:
                            str = "Last " + ListToString(TempCardsPick) + " " + lastKupa[int(Choice[-1])]
                            my_socket.send(bytes(str, 'utf-8'))
                            card = my_socket.recv(1024).decode('utf-8')
                            #print("NEW CARD FROM KUPA IS: ", card)
                            for i in range(len(TempCardsPick)):
                                if TempCardsPick[i] in my_deck:
                                    my_deck.remove(TempCardsPick[i])
                                    #print("new deck", my_deck)
                            my_deck.append(card)
                            lastKupa = TempCardsPick
                            Display_Deck(my_deck, numofplayers, lastKupa, can_yaniv)
                            TempCardsPick.clear()
                            decktosend = "mydeck "
                            decktosend += ListToString(my_deck)
                            my_socket.send(bytes(decktosend, 'utf-8'))
                            my_socket.send(bytes("finished", 'utf-8'))
                            myTurn = False
                            py.display.set_caption(cap)
                        else:
                            #print("WRONG PICK!")
                            Display_Deck(my_deck, numofplayers, lastKupa, can_yaniv)
                            TempCardsPick.clear()
                    if Choice == "YANIV":
                        decktosend = "mydeck "
                        decktosend += ListToString(my_deck)
                        my_socket.send(bytes(decktosend, 'utf-8'))
                        my_socket.send(bytes("YANIV", 'utf-8'))
                        result = my_socket.recv(1024).decode('utf-8')
                        if result == "win":
                            my_socket.recv(1024).decode('utf-8')
                            sums = get_sums()
                            Display_Deck(my_deck, numofplayers, lastKupa, can_yaniv, sums, myIndex)
                            You_Win()
                            fin = True
                            break
                        elif result == "asaf":
                            py.display.set_caption('ASAF!')
                            my_socket.recv(1024).decode('utf-8')
                            sums = get_sums()
                            Display_Deck(my_deck, numofplayers, lastKupa, can_yaniv, sums, myIndex)
                            Asaf()
                            fin = True
                            break

                        myTurn = False

            if not myTurn:
                py.display.set_caption(cap)
                try:
                    #print("waiting")
                    my_socket.settimeout(0.5)
                    data = my_socket.recv(1024).decode('utf-8')
                    #print("now i am ready ", data)
                    tempush = data.split()
                    turn = tempush[0]
                    del tempush[0]
                    if data == "finish_decks":
                        sums = get_sums()
                        Display_Deck(my_deck, numofplayers, lastKupa, can_yaniv, sums, myIndex)
                        if winner_asaf:
                            Asaf()
                        elif winner_yaniv:
                            You_Win()
                        else:
                            py.display.set_caption(cap3)
                        fin = True
                    if turn == "yourturn":
                        if SumCards(my_deck) < 8:
                            can_yaniv = True
                        else:
                            can_yaniv = False
                        lastKupa = tempush
                        Display_Deck(my_deck, numofplayers, lastKupa, can_yaniv)
                        myTurn = True
                        py.display.set_caption(cap2)
                        #print("sum deck: ", SumCards(my_deck))
                    if turn == "notturn":
                        lastKupa = tempush
                        Display_Deck(my_deck, numofplayers, lastKupa, can_yaniv)
                except socket.timeout:
                    continue
    end_game()


def main():
    myIndex = int(my_socket.recv(1024).decode('utf-8'))
    #print("my index: ", myIndex)
    numofplayers = int(my_socket.recv(1024).decode('utf-8'))
    #print("timeout: ", my_socket.gettimeout())
    lastKupa = my_socket.recv(1024).decode('utf-8')
    #print("LASTTTFRTYGRGIU4HIUH5UI ", lastKupa)
    lastKupa = lastKupa.split()
    while not LoggedIn:
        root = Tk()
        lf = LoginFrame(root)
        root.mainloop()
    root.destroy()
    py.init()
    Game(myIndex, numofplayers, lastKupa)


"""
Open rules page and wait for mouse input 
"""
if __name__ == '__main__':
    main()
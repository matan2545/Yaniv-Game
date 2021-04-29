# Matan Antebi
# 12.04.19
# ver 5.2

import socket, random, threading, sqlite3

"""
==============================
CONSTANTS
==============================
"""
PACK = []
KUPA_D = ["1D", "2D", "3D", "4D", "5D", "6D", "7D", "8D", "9D", "10D", "11D", "12D", "13D"]
KUPA_C = ["1C", "2C", "3C", "4C", "5C", "6C", "7C", "8C", "9C", "10C", "11C", "12C", "13C"]
KUPA_H = ["1H", "2H", "3H", "4H", "5H", "6H", "7H", "8H", "9H", "10H", "11H", "12H", "13H"]
KUPA_S = ["1S", "2S", "3S", "4S", "5S", "6S", "7S", "8S", "9S", "10S", "11S", "12S", "13S"]
KUPA = [KUPA_D, KUPA_C, KUPA_H, KUPA_S]
TEMP_KUPA =[]
LEFT = 1
all_decks = []
all_connections = []
all_addresses = []
global my_username
global connected
connected = []
connected.append("admin")
# the function receives variable "x" - number of cards requested ,and variable "conn" - the client who will receive
# the list the, sends the card list to the client and returns updated pack.
class Users:
    def add_user(self, username, password):
        sqlconn = sqlite3.connect('users.db')
        cursor = sqlconn.cursor()
        check = "SELECT * FROM users WHERE username = " + '"' + username + '"'
        #print(check, "dudi")
        cursor.execute(check)
        selected_player = cursor.fetchone()
        if selected_player:
            return "user already exist"
        try:
            cursor.execute("INSERT INTO users VALUES (:username, :password, :score)",
                           {'username': username, 'password': password, 'score': 0})
            sqlconn.commit()
            sqlconn.close()
            #print("Record created successfully")
            return "Record created successfully"
        except:
            return "error"

    def login_user(self, username, password):
        try:
            global connected
            if username in connected:
                return "user has already connected"
            sqlconn = sqlite3.connect('users.db')
            cursor = sqlconn.cursor()
            str1 = "SELECT * FROM users WHERE username = " + '"' + username + '"'
            #print(str1)
            cursor.execute(str1)
            selected_player = cursor.fetchone()
            #print("pass: ", selected_player[1])
            #print(selected_player, "ff")
            sqlconn.commit()
            sqlconn.close()
            #print("Record created successfully", selected_player)
            #print("selected: ", password, selected_player)
            global my_username
            my_username = username
            connected.append(username)
            #print("global ", my_username)
            return password == selected_player[1]
        except:
            return "Not found"

    def update_score(self, username, toadd):
        try:
            sqlconn = sqlite3.connect('users.db')
            cursor = sqlconn.cursor()
            str1 = "SELECT * FROM users WHERE username = " + '"' + username + '"'
            #print(str1)
            cursor.execute(str1)
            selected_player = cursor.fetchone()
            cursor.execute('''UPDATE users SET score = ? WHERE username = ?''', ((int(selected_player[2])+int(toadd)), username))
            cursor.execute(str1)
            selected_player_new = cursor.fetchone()
            #print("new score: ", str(selected_player_new[2]))
            sqlconn.commit()
            sqlconn.close()
            return selected_player_new[2]
        except:
            return "Not found"


class Players:
    def insert_player(self,conn, index = 999, deck= "",score = "0"):
        sqlconn = sqlite3.connect('yaniv.db')
        cursor = sqlconn.cursor()
        cursor.execute("INSERT INTO yaniv VALUES (:conn, :deck, :score, :index)", {'conn': conn, 'deck': deck, 'score': score, 'index': index})
        sqlconn.commit()
        sqlconn.close()
        #print("Record created successfully")

    def select_player_by_conn(self, conn):
        sqlconn = sqlite3.connect('yaniv.db')
        cursor = sqlconn.cursor()
        str1 = "SELECT * FROM decks WHERE conn = " + "" + conn + ""
        cursor.execute(str1)
        selected_player = cursor.fetchone()
        sqlconn.commit()
        sqlconn.close()
        #print("Record created successfully")
        return selected_player

    def select_player_by_index(self, index):
        sqlconn = sqlite3.connect('yaniv.db')
        cursor = sqlconn.cursor()
        cursor.execute("SELECT * FROM yaniv WHERE ind = :index", {'index': index})
        selected_player = cursor.fetchone()
        sqlconn.commit()
        sqlconn.close()
        #print("Record created successfully")
        return selected_player

    def update_deck(self, conn, deck):
        sqlconn = sqlite3.connect('yaniv.db')
        cursor = sqlconn.cursor()
        cursor.execute("""UPDATE yaniv SET deck = :deck
                         WHERE conn = :conn""",
                       {'deck' : ListToString(deck), 'conn' : str(conn)})
        sqlconn.commit()
        sqlconn.close()

    def add_score(self, index, score):
        sqlconn = sqlite3.connect('yaniv.db')
        cursor = sqlconn.cursor()
        temp_score = self.select_player_by_index(index)
        #print(temp_score.fatchall())
        score += temp_score.fatchall()[3]
        cursor.execute("""UPDATE yaniv SET score = :score
                                 WHERE index = :index""",
                       {'deck': score, 'index': index})
        sqlconn.commit()
        sqlconn.close()

def RandomStartCards(x, conn):
    PACK = []
    #print(x)
    decktosend = ""
    while x > 0:
        shape = random.randint(0, 3)
        number = random.randint(0, 12)
        try:
            TempCard = KUPA[shape][number]
            #print("temp ", TempCard)
            KUPA[shape].remove(TempCard)
            PACK.append(TempCard)
            decktosend += (TempCard + " ")
            #print("num: ", number, " shape: ", shape)
            x =  x - 1
        except:
            continue
        if len(PACK) is 5:
            #print("pack: ", PACK)
            #print(KUPA)
            #print(decktosend)
            conn.send(bytes(decktosend, 'utf-8'))
            all_decks.append(PACK)
            #print(PACK)
    #print("len kupa ", len(KUPA[0]+KUPA[1]+KUPA[2]+KUPA[3]), "len pack: ", len(PACK))
    players_class.update_deck(conn, decktosend)
    return PACK

# The function receives a list and add it to the game pack.
def AddToPack(list):
    #print("KUPA BEFORCE CHANGES ", KUPA)
    for i in range(len(list)):
        number = list[i][:-1]
        shape = list[i][-1]
        if shape is 'D':
            shapeindex = 0
        elif shape is 'C':
            shapeindex = 1
        elif shape is 'H':
            shapeindex = 2
        elif shape is 'S':
            shapeindex = 3
        KUPA[shapeindex].append(list[i])
    #print("KUPA AFTER CHANGES ", KUPA)

# The function receives a connection and sends him a random card from the game pack.
def TakeFromPack(conn):
    x = 1
    while x > 0:
        shape = random.randint(0, 3)
        number = random.randint(0, 12)
        try:
            TempCard = KUPA[shape][number]
            #print("temp ", TempCard)
            KUPA[shape].remove(TempCard)
            #print("num: ", number, " shape: ", shape)
            x = x - 1
        except:
            continue
    conn.send(bytes(TempCard, 'utf-8'))

def RandomStartLastKupa():
    x = 1
    while x > 0:
        shape = random.randint(0, 3)
        number = random.randint(0, 12)
        try:
            TempCard = KUPA[shape][number]
            #print("temp ", TempCard)
            KUPA[shape].remove(TempCard)
            #print("num: ", number, " shape: ", shape)
            x = x - 1
        except:
            continue
    return TempCard
# The function receives a list, convert it to a string and return it.
def ListToString(list):
    str = ""
    for i in range(len(list)):
        str += list[i]+" "
    return str

def TakeSpecificCardFromPack(conn, cardtosend):
    number = cardtosend[:-1]
    shape = cardtosend[-1]
    if shape is 'D':
        shapeindex = 0
    elif shape is 'C':
        shapeindex = 1
    elif shape is 'H':
        shapeindex = 2
    elif shape is 'S':
        shapeindex = 3
        #print("kupa check 343: ", KUPA, "shapeindex: ", shapeindex, "[",shape,"]")
    try:
        KUPA[shapeindex].remove(cardtosend)
    except:
        pass
    #print("KUPA AFTER SPECIFIC CHANGES ", KUPA)
    conn.send(bytes(cardtosend, 'utf-8'))

def SumCards(my_deck):
    sum = 0
    for i in range(len(my_deck)):
        sum += int(my_deck[i][:-1])
    return sum

def Check_if_yaniv(all_decks, checkdeck, my_index):
    sum_my_deck = SumCards(checkdeck)
    for i in range(len(all_decks)):
        if SumCards(all_decks[i]) <= sum_my_deck and i != my_index:
            return "asaf"
    return "win"

def win_function(result, my_index):
    if result == "win":
        for i in range(len(all_decks)):
            if i is not my_index:
                players_class.add_score(i, SumCards(all_decks[i]))
    elif result == "asaf":
        all_scores = 0
        for i in range(len(all_decks)):
            if i is not my_index:
                players_class.add_score(i, SumCards(all_decks[i]))
                all_scores += SumCards(all_decks[i])
        all_scores += SumCards(all_decks[my_index])
        players_class.add_score(my_index, all_scores)

# The function receives a connection, address and the index in all_connections,
# the function works in a thread for each client connected.
def Handle_Client(conn, address, index):
    my_deck = []
    lastKupa = []
    while True:
        data = conn.recv(1024).decode('utf-8')
        #print("DATA IS:" , data)
        if "login" in data:
            splitted = data.split()
            try:
                answer = Users.login_user(splitted[1], splitted[1], splitted[2])
                #print("answer: ", answer)
                conn.send(bytes(str(answer), 'utf-8'))
            except:
                conn.send(bytes(str("error"), 'utf-8'))
        if "register" in data:
            splitted = data.split()
            answer = Users.add_user(splitted[1], splitted[1], splitted[2])
            #print("answer: ", answer)
            conn.send(bytes(str(answer), 'utf-8'))
        if "score" in data:
            splitted = data.split()
            answer = Users.update_score(splitted[1], splitted[1], splitted[2])
            #print("answer: ", answer)
            conn.send(bytes(str(answer), 'utf-8'))
        if data == "StartCards":
            my_deck = RandomStartCards(5, conn)
            #print(address[0], " Pack: ", my_deck)
        if data == "NUMCARDS2":
            try:
                if index == 0:
                    #print("we are here!!!! len1: ", all_decks[1], str(len(all_decks[1])))
                    conn.send(bytes(str(len(all_decks[1])), 'utf-8'))
                elif index == 1:
                    #print("we are here!!!! len0: ", all_decks[0], str(len(all_decks[0])))
                    conn.send(bytes(str(len(all_decks[0])), 'utf-8'))
            except:
                if index == 0:
                    #print("we are here!!!! len1: ", all_decks[1], str(len(all_decks[1])))
                    conn.send(bytes(str(5), 'utf-8'))
                elif index == 1:
                    #print("we are here!!!! len0: ", all_decks[0], str(len(all_decks[0])))
                    conn.send(bytes(str(5), 'utf-8'))
        if data == "NUMCARDS3":
            #print("numcards3 for index: ", index, all_decks)
            try:
                if index == 0:
                    conn.send(bytes(str(len(all_decks[1])), 'utf-8'))
                    conn.send(bytes(str(len(all_decks[2])), 'utf-8'))
                elif index == 1:
                    conn.send(bytes(str(len(all_decks[0])), 'utf-8'))
                    conn.send(bytes(str(len(all_decks[2])), 'utf-8'))
                elif index == 2:
                    conn.send(bytes(str(len(all_decks[0])), 'utf-8'))
                    conn.send(bytes(str(len(all_decks[1])), 'utf-8'))
            except:
                if index == 0:
                    conn.send(bytes(str(5), 'utf-8'))
                    conn.send(bytes(str(5), 'utf-8'))
                elif index == 1:
                    conn.send(bytes(str(5), 'utf-8'))
                    conn.send(bytes(str(5), 'utf-8'))
                elif index == 2:
                    conn.send(bytes(str(5), 'utf-8'))
                    conn.send(bytes(str(5), 'utf-8'))
        if "Kupa" in data:
            PickedList = data.split()
            #print("recieved: ", PickedList)
            del PickedList[0]
            #print("new: ", PickedList)
            TakeFromPack(conn)
            lastKupa = PickedList
            TEMP_KUPA = PickedList
            #print("TEMP KUPA: ", TEMP_KUPA)
            AddToPack(PickedList)
        if "Last" in data:
            PickedList = data.split()
            #print("recieved: ", PickedList)
            cardtosend = PickedList[-1]
            del PickedList[-1]
            del PickedList[0]
            #print("tje card to send: ", cardtosend)
            TakeSpecificCardFromPack(conn, cardtosend)
            lastKupa = PickedList
            TEMP_KUPA = PickedList
            AddToPack(PickedList)
        if "mydeck" in data:
            tempdeck = data.split()
            #print("recieved deck: ", tempdeck)
            del tempdeck[0]
            my_deck = tempdeck
            #print("DECK OF <", address[0], "> is: ", my_deck)
            all_decks[index] = my_deck
            #print("all decks: ", all_decks)
            players_class.update_deck(conn, my_deck)
        if data == "finished":
            #print("index: ", index, "lenconnection: ", len(all_connections)-1)
            if index == len(all_connections)-1:
                #print ("its me!! last turn")
                tp = ListToString(lastKupa)
                tp2 = "yourturn " + tp
                #print("gonna send last kupa: ", tp2)
                all_connections[0].send(bytes(tp2, 'utf-8'))
                tp3 = "notturn " + tp
                for i in range(len(all_connections)):
                    if (i != index) and (i != 0):
                        #print("Sending to ", i)
                        all_connections[i].send(bytes(tp3, 'utf-8'))
            else:
                tp = ListToString(lastKupa)
                tp2 = "yourturn " + tp
                #print("gonna send last kupa: ", tp2)
                all_connections[index + 1].send(bytes(tp2, 'utf-8'))
                tp3 = "notturn " + tp
                for i in range(len(all_connections)):
                    if (i != index) and (i != index + 1):
                 #       print("Sending to ", i)
                        all_connections[i].send(bytes(tp3, 'utf-8'))
        if data == "fish":
            conn.send(bytes("fish", 'utf-8'))
        if data == "YANIV":
            result = Check_if_yaniv(all_decks, my_deck, index)
            conn.send(bytes(result, 'utf-8'))
            str_sum = ""
            for x in range(len(all_decks)):
                str_sum += str(SumCards(all_decks[x])) + " "
            for i in range(len(all_connections)):
                all_connections[i].send(bytes("finish_decks", 'utf-8'))
                all_connections[i].send(bytes(str_sum, 'utf-8'))
        if data == "exit":
            break



# The function receives a connection, address and the index in all_connections,
# the function open a thread for each client
def openThread(conn, address, index):
    t = threading.Thread(target=Handle_Client, args=(conn, address, index, ))
    t.start()

# The function receives server socket and accept clients, add each client's info to a list(all_connection,
# all_addresses) and call openThread function.
def accept_clients(server_socket):
    y = int(input("Type number of players > "))
    x = 0
    global all_connections
    while x is not y:
        conn, address = server_socket.accept()
        #print(conn, "connectionffff")
        #print("gonna send: ", str(x))
        conn.send(bytes(str(x), 'utf-8'))
        all_connections.append(conn)
        all_addresses.append(address)
        print(address[0], "Has connected")
        openThread(conn, address, len(all_connections)-1)
        #print("bag")
        x += 1
    numofplayer = str(y)
    startCard = RandomStartLastKupa()
    #print("start cards: ", startCard)
    for i in range(len(all_connections)):
     #   print("sent")
        players_class.insert_player(str(all_connections[i]), i)
        all_connections[i].send(bytes(numofplayer, 'utf-8'))
        all_connections[i].send(bytes(startCard, 'utf-8'))


def Open_server():
    server_socket = socket.socket()
    port = 9999
    host = '0.0.0.0'
    server_socket.bind((host, port))
    server_socket.listen(1)
    print("Waiting For Connection...")
    accept_clients(server_socket)
    #print("gello")

def main():
    global players_class
    players_class = Players()

    Open_server()
    #print("hi")

    # ===============================

if __name__ == '__main__':
    main()


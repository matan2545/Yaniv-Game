from tkinter import *
import sqlite3

class Users:
    def add_user(self, username, password):
        try:
            sqlconn = sqlite3.connect('users.db')
            cursor = sqlconn.cursor()
            cursor.execute("INSERT INTO users VALUES (:username, :password, :score)",
                           {'username': username, 'password': password, 'score': 0})
            sqlconn.commit()
            sqlconn.close()
            print("Record created successfully")
        except:
            return "error"

    def login_user(self, username, password):
        try:
            sqlconn = sqlite3.connect('users.db')
            cursor = sqlconn.cursor()
            str1 = "SELECT * FROM users WHERE username = " + '"' + username + '"'
            print(str1)
            cursor.execute(str1)
            selected_player = cursor.fetchone()
            print("pass: ", selected_player[1])
            print(selected_player, "ff")
            sqlconn.commit()
            sqlconn.close()
            print("Record created successfully", selected_player)
            print("selected: ", password, selected_player)
            return password == selected_player[1]
        except:
            return "Not found"


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
        self.logbtn = Button(self, text="Login", command=self._login_btn_clicked)
        self.logbtn.grid(columnspan=2)

        self.logbtn = Button(self, text="Register", command=self._register_btn_clicked)
        self.logbtn.grid(columnspan=2)

        self.pack()

    def _login_btn_clicked(self):
        # print("Clicked")
        username = self.entry_username.get()
        password = self.entry_password.get()

        print(username, password)
        print(Users.login_user(username, username, password))
        if Users.login_user(username, username, password) is True:
            print("logging in")
        elif Users.login_user(username, username, password) is False:
            print("Incorrect password")
        else:
            print("Try again")
        print("login", username, password)

    def _register_btn_clicked(self):
        # print("Clicked")
        username = self.entry_username.get()
        password = self.entry_password.get()

        # print(username, password)
        Users.add_user(username, username, password)


root = Tk()
lf = LoginFrame(root)
root.mainloop()
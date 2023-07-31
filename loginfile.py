from tkinter import *
import sqlite3
import re
from pvp import PlayerVsPlayer

def main():
  classProfiles = Profiles()
  classProfiles.Layout()

class Profiles:
  def __init__(self):
   self.height = 400
   self.width = 500
   self.finish = False
   self.classMainMenu = MainMenu()
   self.classPlayerVsPlayer = PlayerVsPlayer()

  def createWindow(self):
    #Creates window as main window and the resolution
    self.window = Tk()
    self.window.title("Draughts") 
    screenWidth = self.window.winfo_screenwidth()
    screenHeight = self.window.winfo_screenheight()
    x = (screenWidth/2) - (self.width/2)
    y = (screenHeight/2) - (self.height/2)
    self.window.geometry("%dx%d+%d+%d" % (self.width, self.height, x, y))
    self.window.resizable(0, 0)

    self.top = Frame(self.window, bd=2, relief=RIDGE)
    self.top.pack(side=TOP, fill=X)
    self.form = Frame(self.window, height=200)
    self.form.pack(side=TOP, pady=2)

  def Layout(self):
    self.createWindow()
    #Creating Variables
    self._username = StringVar()
    self._password = StringVar()

    #Making all of the labels
    labelTitle = Label(self.top, text = "Draughts", font=("open sans", 16)).pack(fill=X)
    labelUsername = Label(self.form, text = "Username:", font = ("open sans",16), bd=15).grid(row=0, sticky="e")
    labelPassword = Label(self.form, text = "Password:", font = ("open sans", 16), bd=15).grid(row=1,sticky="e")
    self.labelText = Label(self.form).grid(row=2, columnspan=2)

    #Entry box
    username = Entry(self.form, textvariable=self._username,font=(14)).grid(row=0,column=1)
    password = Entry(self.form, textvariable=self._password, show="*",font=(14)).grid(row=1, column=1)
    
    #Buttons
    buttonLogin = Button(self.form,text=str("Login"),width=45,command= lambda:self.Login()).grid(pady=10,row=3,columnspan=2)
    buttonRegister = Button(self.form,text=str("Register"),width=45,command=lambda: self.RegisterLayout()).grid(pady=10,row=4,columnspan=2)
    buttonGuest = Button(self.form,text=str("Play as a Guest"),width=45,command=lambda: self.menu("guest",None)).grid(pady=10,row=5,columnspan=2)
 
  def Login(self):
    #Database 
    connect = sqlite3.connect("profiles.db")
    cursor = connect.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS user(
      user_id INTEGER NOT NULL PRIMARY KEY, 
      username TEXT, 
      password TEXT,
      FOREIGN KEY (user_id) REFERENCES Rating(rating_id)
    )
      ''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS Rating(
    rating_id INTEGER NOT NULL PRIMARY KEY, 
    wins INTEGER, 
    losses INTEGER)''')
    cursor.execute("SELECT * FROM user WHERE `username` = 'admin' AND `password` = 'admin'")
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO user (username, password) VALUES('admin', 'admin')")
        cursor.execute("INSERT INTO Rating(wins,losses) VALUES(0,0)")
        cursor.execute("INSERT INTO user (username, password) VALUES('test', 'test')")
        cursor.execute("INSERT INTO Rating(wins,losses) VALUES(0,0)")


    #Login
    if self._password.get() == "" or self._username.get() == "":
      self.labelText.config(text="Enter Username and Password", fg="red")
    else:
      cursor.execute("SELECT * FROM user WHERE `username` = ? AND `password` = ?", (self._username.get(), self._password.get()))
      if cursor.fetchone() is not None:
        self.SuccessWindow()
      else:
        self.labelText.config(text="Invalid username or password", fg="red")
        self._username.set("")
        self._password.set("")
     #########################################
    cursor.execute("SELECT * FROM user")
    print(cursor.fetchall())
    cursor.execute("SELECT * FROM Rating")
    print(cursor.fetchall())
    connect.commit()
    cursor.close()
    connect.close()

  def RegisterLayout(self):
    #Creating Variables
    self.destroyWindow()
    self.createWindow()

    self.newusername = StringVar()
    self.newpassword = StringVar()
    
    #Making all of the labels
    self.labelTitle = Label(self.top, text = "Register New Account", font=("open sans", 16))
    self.labelTitle.pack(fill=X)
    self.labelUsername = Label(self.form, text = "Username:", font = ("open sans",16), bd=15)
    self.labelUsername.grid(row=0, sticky="e")
    self.labelPassword = Label(self.form, text = "Password:", font = ("open sans", 16), bd=15)
    self.labelPassword.grid(row=1,sticky="e")
    self.labelText = Label(self.form)
    self.labelText.grid(row=2, columnspan=2)
  
    #Entry Boxes
    username = Entry(self.form, textvariable=self.newusername,font=(14))
    username.grid(row=0,column=1)
    password = Entry(self.form, textvariable=self.newpassword, show="*",font=(14))
    password.grid(row=1, column=1)

    BackText = "Back"
    RegisterText = "Register"
    self.buttonLogin = Button(self.form,text=BackText,width=45,command= lambda:self.RegisterBack(self.window))
    self.buttonLogin.grid(pady=10,row=4,columnspan=2)
    self.buttonRegister = Button(self.form,text=RegisterText,width=45,command=lambda: self.RegisterProcess(Event=None))
    self.buttonRegister.grid(pady=0,row=3,columnspan=2)
  
  def RegisterBack(self,window):
    self.window.destroy()
    self.Layout()

  def RegisterProcess(self,Event=None):
    connect = sqlite3.connect("profiles.db")
    cursor = connect.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS user(username TEXT, password TEXT)")  
    print(self.newusername.get())
    if self.newusername.get() == "" or self.newpassword.get == "":
      self.labelText.config(text="Enter Username and Password", fg="red")
      return
    self.registerUsername = self.newusername.get()
    self.registerPassword = self.newpassword.get()
    cursor.execute("SELECT * FROM user")
    rows = cursor
    for row in rows:
      if self.registerUsername in row:
        self.labelText.config(text="Username already taken",fg="red")
        self.newusername.set("")
        self.newpassword.set("")
        print("Done")
        return
    if (len(self.registerPassword)<8):
      self.labelText.config(text="Password must be 9 or more characters",fg="red")
      return
    elif not re.search("[a-z]", self.registerPassword):
      self.labelText.config(text="Password must have alphabet letters",fg="red")
      return
    elif not re.search("[A-Z]", self.registerPassword):
      self.labelText.config(text="Password must have a capital letter",fg="red")
      return
    elif not re.search("[0-9]", self.registerPassword):
      self.labelText.config(text="Password must have a number",fg="red")
      return
    elif re.search("\s", self.registerPassword):
      self.labelText.config(text="Password must not have any spaces",fg="red")
      return
      cursor.execute("SELECT * FROM user")
    cursor.execute("CREATE TABLE IF NOT EXISTS user(username TEXT, password TEXT)")       
    cursor.execute("INSERT INTO user(username,password) VALUES(?,?)" , (self.registerUsername,self.registerPassword))
    cursor.execute("INSERT INTO Rating(wins,losses) VALUES(0,0)")
    connect.commit()
    cursor.close()
    connect.close()
    self.RegisterSuccess()

  def RegisterSuccess(self):
    self.destroyWindow()
    self.createWindow()
    self.labelSuccess = Label(self.window, text="Successfully Created Account!", font=("open sans", 15)).pack()
    self.buttonBack = Button(self.window, text=str("Next"), command=lambda : self.RegisterEnter()).pack(pady=20,fill=X)

  def RegisterEnter(self):
    self.destroyWindow()
    self.Layout()
  
  def SuccessWindow(self):
    #Creates a new window to notify the user that they've logged in
    self.destroyWindow()
    self.createWindow()
    labelSuccess = Label(self.window, text="Successfully Logged In!", font=("open sans", 15)).pack()
    buttonBack = Button(self.window, text="Continue", command=lambda : self.SuccessBack()).pack(pady=20,fill=X)

  def SuccessBack(self):
    self.menu(str(self._username.get()))
  
  def menu(self,username,username2 = None):
    self.destroyWindow()
    if username == "admin":
      classAdmin = Admin()
      classAdmin.adminMenu()
    if username == "guest":
      classMainMenu = MainMenu()
      classMainMenu.gameMenu("Guest")
    elif username != "admin" and username != "guest":
      classPlayer = Player()
      if username2 is None:
        classPlayer.playerMenu(username,"Player 2")
      else:
        classPlayer.playerMenu(username,username2)

  def destroyWindow(self):
    self.window.deiconify()
    self.window.destroy()
    



class MainMenu(Profiles):
  def __init__(self):
    self.height = 400
    self.width = 500
    self.classPlayerVsPlayer = PlayerVsPlayer()

  def gameMenu(self,username):
    self.user1 = username
    
    super().createWindow()

    #Buttons
    PvP = str(self.user1.title() + " vs Player 2")
    PvAI = str(self.user1.title() + " vs AI")
    labelTitle = Label(self.top, text = str("Welcome " + self.user1.title() ), font=("open sans", 16)).pack(fill=X)
    if username == "Guest":
      buttonPvP = Button(self.form,text=str("Guest vs Guest"),width=45,command= lambda:self.startPvP()).grid(pady=10,row=1,columnspan=2)
    buttonPvAI = Button(self.form,text=PvAI,width=45,command=lambda: self.startPvP()).grid(pady=10,row=2,columnspan=2)
    labelVs = Label(self.form, text = "Red (Player 1) vs White (Player 2)", bd=15).grid(row=100,sticky="e")
    buttonSignOut = Button(self.form,text=str("Log Out"), width=45, command=lambda: self.logOut()).grid(pady=10,row=99,columnspan = 2)

  def logOut(self):
    super().destroyWindow()
    super().Layout()
    


  def viewRating(self,user):
    super().destroyWindow()
    super().createWindow()
    wins, losses, userId = self.getRating(user)

    labelTitle = Label(self.top, text = str("Rating"), font=("open sans", 16)).pack(fill=X)
    labelRating = Label(self.form, text = str("Your rating is " + str(wins - losses)), font = ("open sans",16), bd=15).grid(row=0, sticky="e")
    labelWins = Label(self.form, text = str("You have " + str(wins) + " wins"), font = ("open sans",16), bd=15).grid(row=1, sticky="e")
    labelRating = Label(self.form, text = str("You have " + str(losses) + " losses"), font = ("open sans",16), bd=15).grid(row=2, sticky="e")
    ButtonBack = Button(self.form,text=str("Back"),width=45,command=lambda: self.Back()).grid(pady=10,row=3,
    columnspan=2)

  def Back(self):
    super().menu(self.user1,self.user2)

  

  def getRating(self,user):
    connect = sqlite3.connect("profiles.db")
    cursor = connect.cursor()
    cursor.execute("SELECT user_id FROM user WHERE `username` = ?", (user,))
    sqluserId = (cursor.fetchone())
    userId = sqluserId[0]
    cursor.execute("SELECT wins,losses FROM Rating WHERE `rating_id` = ? ", (userId,))
    wins, losses = (cursor.fetchone())
    cursor.close
    connect.close
    return wins, losses, userId

  def startPvP(self):
    super().destroyWindow()
    self.classPlayerVsPlayer.playGame()

class Admin(MainMenu):
  def adminMenu(self):
    super().gameMenu("admin")
    buttonPvP = Button(self.form,text=str("Admin vs Guest"),width=45,command= lambda:super().startPvP()).grid(pady=10,row=1,columnspan=2)
    buttonClearDatabase = Button(self.form,text=str("Clear Database"),width=45,command = lambda:self.clearDatabase()).grid(pady=10,row=4,columnspan=2)
    buttonviewRating = Button(self.form,text=str("View Rating"),width=45,command = lambda:self.viewRating()).grid(pady=10,row=3,columnspan=2)

  def startPvP(self):
    super().startPvP()
  
  def viewRating(self):
    super().viewRating()

  def clearDatabase(self):
    pass
  
class Player(MainMenu):
  def playerMenu(self,user1,user2):
    self.user1 = user1
    self.user2 = user2
    super().gameMenu(user1)
    buttonPvP = Button(self.form,text=str(self.user1 + " vs " + self.user2),width=45,command= lambda:self.getUser2()).grid(pady=10,row=1,columnspan=2)
    buttonPvG = Button(self.form,text=str(self.user1 + " vs Guest"),width=45,command= lambda:super().startPvP()).grid(pady=10,row=3,columnspan=2)
    buttonviewRating = Button(self.form,text=str("View Rating"),width=45,command = lambda:self.viewRating()).grid(pady=10,row=4,columnspan=2)

  def viewRating(self):
    super().viewRating(self.user1)
  


  def user2Login(self):
    super().destroyWindow()
    super().createWindow()
    #Creating Variables
    self._username = StringVar()
    self._password = StringVar()
    
    #Making all of the labels
    labelTitle = Label(self.top, text = "Draughts", font=("open sans", 16)).pack(fill=X)
    labelUsername = Label(self.form, text = "Username:", font = ("open sans",16), bd=15).grid(row=0, sticky="e")
    labelPassword = Label(self.form, text = "Password:", font = ("open sans", 16), bd=15).grid(row=1,sticky="e")
    self.labelText = Label(self.form).grid(row=2, columnspan=2)

    #Entry box
    self.username = Entry(self.form, textvariable=self._username,font=(14)).grid(row=0,column=1)
    self.password = Entry(self.form, textvariable=self._password, show="*",font=(14)).grid(row=1, column=1)
 
    #Buttons
    buttonLogin = Button(self.form,text=str("Login"),width=45,command= lambda:self.user2LoginProcess()).grid(pady=10,row=3,columnspan=2)
    buttonBack = Button(self.form, text=str("Back"),width=45,command = lambda:self.backToMenu()).grid(pady=10,row=4,columnspan=2)

  def backToMenu(self):
    super().menu(self.user1)
    

  
  def getUser2(self):
    if self.user2 == "Player 2":
      self.user2Login()
    else:
      self.startPvP()

  def startPvP(self):
    # winner = getWinner()
    winner = "Red"
    self.checkWinner(winner)
    self.playerMenu(self.user1,self.user2)

  def checkWinner(self, winner):
    if winner == "Red":
      self.addRating(self.user1,self.user2)
    else:
      self.addRating(self.user2,self.user1)
  
  def addRating(self,winner,loser):
    print("Start!")
    winnerwins, winnerlosses, winnerId = super().getRating(winner)
    loserwins, loserlosses, loserId = super().getRating(loser)
    print(winnerwins,winnerlosses,winnerId)
    winnerwins = winnerwins + 1
    loserlosses = loserlosses + 1
    connect = sqlite3.connect("profiles.db")
    cursor = connect.cursor()
    cursor.execute("UPDATE Rating SET `wins` = ? WHERE `rating_id` = ? ",(winnerwins, winnerId,))
    cursor.execute("UPDATE Rating SET `losses` = ? WHERE `rating_id` = ? ",(loserlosses, loserId,))
    connect.commit()
    cursor.close()
    connect.close()
    
  def user2LoginProcess(self):
    #Database 
    connect = sqlite3.connect("profiles.db")
    cursor = connect.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS user(mem_id INTEGER NOT NULL PRIMARY KEY  AUTOINCREMENT, username TEXT, password TEXT)")
    cursor.execute("SELECT * FROM user WHERE `username` = 'admin' AND `password` = 'admin'")
    #Login
    if self._password.get() == "" or self._username.get() == "":
      self.labelText.config(text="Enter Username and Password", fg="red")
    else:
      cursor.execute("SELECT * FROM user WHERE `username` = ? AND `password` = ?", (self._username.get(), self._password.get()))
      if cursor.fetchone() is not None and not (self._username.get() == self.user1) :
        super().destroyWindow()
        self.playerMenu(self.user1, self._username.get())
      else:
        self.labelText.config(text="Invalid username or password", fg="red")
        self._username.set("")
        self._password.set("")
    cursor.close
    connect.close










if __name__ == "__main__":
  main()

#Two windows doesn't allw for get()
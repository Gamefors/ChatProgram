from Client import Client
from tkinter import *
import time
class MainWindow:

    def __init__(self):
        self.mainWindow = Tk()
        self.mainWindow.title("Client")
        self.mainWindow.geometry("225x300")
        
        usernameLabel = Label(self.mainWindow, text="Username:")
        usernameLabel.pack()
        self.usernameEntry = Entry(self.mainWindow)
        self.usernameEnt ry.pack()
        LoginButton = Button(self.mainWindow, text = "Login", command=self.getUsername)
        LoginButton.pack()
        
        self.mainWindow.mainloop()

    def getUsername(self):
        self.startClient(self.usernameEntry.get())
        

    def startClient(self, username):
        #self.Client = Tk()
        #self.Client.title("Client")
        #self.Client.geometry("225x600")
        #outputVar = ("starting client...") 
        #output = Label(self.Client, text=outputVar)
        #output.pack()
        Client(username)

MainWindow()
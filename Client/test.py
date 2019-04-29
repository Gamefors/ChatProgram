from Client import Client
from tkinter import Tk, Entry, Label
class test:

    def __init__(self):
        username = "Jan"
        

        self.mw = Tk()
        self.input = Entry(self.mw)
        self.input.pack()
        self.output = Label(self.mw)
        self.output.pack()
        
        self.client = Client(username, self.output)
        def func(event):
            self.client.sendInput(str(self.input.get()))
        self.mw.bind('<Return>', func)
        
        self.mw.mainloop()

test()
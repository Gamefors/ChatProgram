from Client import Client

from PyQt5 import QtCore, QtGui, QtWidgets, uic

import sys

CustomDialogUi, _ = uic.loadUiType("Ui/windows/main/CustomDialog.ui")

class CustomDialog(QtWidgets.QDialog, CustomDialogUi):
    def __init__(self):
        super(CustomDialog, self).__init__()
        self.setupUi(self)
        self.RegisterHyperlink().clicked.connect(self.isClicked)
    
    def isClicked(self):
        print('It works')

    def getData(self):
        if self.exec_() == QtWidgets.QDialog.Accepted:
            username = self.username.text()
            password = self.password.text()
            return username + ":" + password
        else:
            return ":"
            
class Main(QtWidgets.QMainWindow):#TODO: use qthread to intialite CLient
    
    def enter(self):
        input = self.mainWindow.input.text()
        self.mainWindow.input.clear()
        self.client.sendInput(input)

    def __init__(self):
        super(Main, self).__init__()
        self.mainWindow = uic.loadUi("Ui/windows/main/MainWindow.ui", self)
        self.mainWindow.input.returnPressed.connect(self.enter)
        data = CustomDialog().getData()
        if data == ":":#TODO: if password empty give notification
            quit()
        else:
            data = data.split(":")
            self.client = Client(data[0], data[1], self.mainWindow)

app = QtWidgets.QApplication(sys.argv)
window = Main()
window.show()
sys.exit(app.exec_())

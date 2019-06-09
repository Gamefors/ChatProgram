from Client import Client

from PyQt5 import QtCore, QtGui, QtWidgets, uic

import sys

class CustomDialog(QtWidgets.QDialog):
    
    def __init__(self):
        super(CustomDialog, self).__init__()
        self.customDialogWindow = uic.loadUi("Ui/windows/main/CustomDialog.ui", self)

    def getData(self):
        if self.customDialogWindow.exec_() == QtWidgets.QDialog.Accepted:
            username = self.customDialogWindow.username.text()
            password = self.customDialogWindow.password.text()
            return username + ":" + password
        else:
            return ":"
            
class Main(QtWidgets.QMainWindow):#TODO: low prio use Qthread to intialite CLient
    
    def __init__(self):
        super(Main, self).__init__()
        self.mainWindow = uic.loadUi("Ui/windows/main/MainWindow.ui", self)
        self.mainWindow.input.returnPressed.connect(self.enter)
        data = CustomDialog().getData()
        if data == ":":
            quit()
        else:
            data = data.split(":")
            self.client = Client(data[0], data[1], self.mainWindow)

    def enter(self):
        input = self.mainWindow.input.text()
        self.client.sendInput(input)
        self.mainWindow.input.clear()

app = QtWidgets.QApplication(sys.argv)
window = Main()
window.show()
sys.exit(app.exec_())

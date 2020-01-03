from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import QThread, pyqtSignal
import sys, os
from Client import Client

class ClientGUILogin(QtWidgets.QMainWindow):

	def loginShow(self):
		self.show()

	def login(self):
		username = self.mainWindow.loginUsername.text()
		password = self.mainWindow.loginPassword.text()
		return (username, password)

	def __init__(self):
		super(ClientGUILogin, self).__init__()
		self.mainWindow = uic.loadUi("ui/LoginWindow.ui", self)

class ClientGUIMain(QtWidgets.QMainWindow):

	def login(self):
		loginParameters = self.loginWindow.login()
		self.client = Client(loginParameters[0],loginParameters[1], (self.mainWindow, self.loginWindow))
		if(self.client.connected):
			self.loginWindow.hide()
			self.show()
		else:
			self.loginWindow.loginUsername.setText("")
			self.loginWindow.loginPassword.setText("")
			QtWidgets.QMessageBox.about(self.oginWindow, "Error", "Could not establish connection to server.")

	def mainHide(self):
		self.hide()



	def __init__(self, loginWindow):
		super(ClientGUIMain, self).__init__()
		self.mainWindow = uic.loadUi("ui/MainWindow.ui", self)
		self.loginWindow = loginWindow
		self.loginWindow.mainWindow.loginButton.clicked.connect(lambda: self.login())


	

app = QtWidgets.QApplication(sys.argv)
loginWindow = ClientGUILogin()
loginWindow.show()
mainWindow = ClientGUIMain(loginWindow)
mainWindow.hide()
sys.exit(app.exec_())
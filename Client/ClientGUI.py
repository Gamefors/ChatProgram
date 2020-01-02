from PyQt5 import QtCore, QtGui, QtWidgets, uic
import sys, os

class ClientGUILogin(QtWidgets.QMainWindow):

	def login(self):
		username = self.mainWindow.loginUsername.text()
		password = self.mainWindow.loginPassword.text()
		return (username, password)

	def __init__(self):
		super(ClientGUILogin, self).__init__()
		self.mainWindow = uic.loadUi("ui/LoginWindow.ui", self)

class ClientGUIMain(QtWidgets.QMainWindow):

	def login(self):
		self.loginParameters = self.loginWindow.login()

	def __init__(self, loginWindow):
		super(ClientGUIMain, self).__init__()
		self.mainWindow = uic.loadUi("ui/MainWindow.ui", self)
		self.loginWindow = loginWindow
		self.loginWindow.mainWindow.loginButton.clicked.connect(lambda: self.test())



app = QtWidgets.QApplication(sys.argv)
loginWindow = ClientGUILogin()
loginWindow.show()
mainWindow = ClientGUIMain(loginWindow)
mainWindow.hide()
sys.exit(app.exec_())
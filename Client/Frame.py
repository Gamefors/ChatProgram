# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\gamef\OneDrive\Desktop\Workspace\Python\Me\Chatprogram\Client\Chris\GUI\untitled.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from Client import Client
import sys
class Ui_MainWindow(object):

    def onClick(self):
        msg = self.userEntry.text()
        self.userEntry.clear()
        self.client.sendInput(msg)
        #print(msg)

    def setupUi(self, MainWindow):
        
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 650)
        MainWindow.setTabletTracking(False)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/newPrefix/icons8-computer-chat-64.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setAcceptDrops(True)
        self.centralwidget.setAutoFillBackground(True)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setEnabled(True)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(160, 580, 691, 22))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.userEntry = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.userEntry.setEnabled(True)
        self.userEntry.setText("")
        self.userEntry.setMaxLength(64)
        self.userEntry.setObjectName("userEntry")
        self.userEntry.returnPressed.connect(self.onClick)
        self.verticalLayout_2.addWidget(self.userEntry)
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_3.setEnabled(True)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(160, 0, 691, 581))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.userOutput = QtWidgets.QTextEdit(self.verticalLayoutWidget_3)
        self.userOutput.setEnabled(True)
        self.userOutput.setReadOnly(True)
        self.userOutput.setObjectName("userOutput")

        self.client = Client("jan", self.userOutput)

        self.verticalLayout_3.addWidget(self.userOutput)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setEnabled(True)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(0, 0, 160, 601))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(self.horizontalLayoutWidget_2)
        self.tabWidget.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setMovable(False)
        self.tabWidget.setObjectName("tabWidget")
        self.rooms = QtWidgets.QWidget()
        self.rooms.setObjectName("rooms")
        self.listWidget = QtWidgets.QListWidget(self.rooms)
        self.listWidget.setEnabled(True)
        self.listWidget.setGeometry(QtCore.QRect(0, 0, 161, 581))
        self.listWidget.setObjectName("listWidget")
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        self.tabWidget.addTab(self.rooms, "")
        self.participants = QtWidgets.QWidget()
        self.participants.setObjectName("participants")
        self.listWidget_2 = QtWidgets.QListWidget(self.participants)
        self.listWidget_2.setGeometry(QtCore.QRect(0, 0, 161, 581))
        self.listWidget_2.setObjectName("listWidget_2")
        item = QtWidgets.QListWidgetItem()
        self.listWidget_2.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_2.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_2.addItem(item)
        self.tabWidget.addTab(self.participants, "")
        self.horizontalLayout_2.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setEnabled(True)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 900, 21))
        self.menubar.setObjectName("menubar")
        self.menu_Create_Account = QtWidgets.QMenu(self.menubar)
        self.menu_Create_Account.setEnabled(True)
        self.menu_Create_Account.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.menu_Create_Account.setTabletTracking(False)
        self.menu_Create_Account.setAutoFillBackground(False)
        self.menu_Create_Account.setInputMethodHints(QtCore.Qt.ImhHiddenText)
        self.menu_Create_Account.setTearOffEnabled(False)
        self.menu_Create_Account.setSeparatorsCollapsible(False)
        self.menu_Create_Account.setObjectName("menu_Create_Account")
        MainWindow.setMenuBar(self.menubar)
        self.actionLogin = QtWidgets.QAction(MainWindow)
        self.actionLogin.setCheckable(False)
        self.actionLogin.setEnabled(True)
        self.actionLogin.setObjectName("actionLogin")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionDisconnect = QtWidgets.QAction(MainWindow)
        self.actionDisconnect.setCheckable(False)
        self.actionDisconnect.setEnabled(False)
        self.actionDisconnect.setObjectName("actionDisconnect")
        self.menu_Create_Account.addAction(self.actionLogin)
        self.menu_Create_Account.addAction(self.actionDisconnect)
        self.menu_Create_Account.addAction(self.actionQuit)
        self.menubar.addAction(self.menu_Create_Account.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Discord 2.0"))
      #  self.userOutput.setPlainText(_translate("MainWindow", "[Server/Info] test\n""\n"" "))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        item = self.listWidget.item(0)
        item.setText(_translate("MainWindow", "Room1"))
        item = self.listWidget.item(1)
        item.setText(_translate("MainWindow", "Room2"))
        item = self.listWidget.item(2)
        item.setText(_translate("MainWindow", "Room3"))
        self.listWidget.setSortingEnabled(__sortingEnabled)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.rooms), _translate("MainWindow", "Räume"))
        __sortingEnabled = self.listWidget_2.isSortingEnabled()
        self.listWidget_2.setSortingEnabled(False)
        item = self.listWidget_2.item(0)
        item.setText(_translate("MainWindow", "user1"))
        item = self.listWidget_2.item(1)
        item.setText(_translate("MainWindow", "user2"))
        item = self.listWidget_2.item(2)
        item.setText(_translate("MainWindow", "user3"))
        self.listWidget_2.setSortingEnabled(__sortingEnabled)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.participants), _translate("MainWindow", "Users"))
        self.menu_Create_Account.setTitle(_translate("MainWindow", "Status: Offline"))
        self.actionLogin.setText(_translate("MainWindow", "Login"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionDisconnect.setText(_translate("MainWindow", "Disconnect"))

#import Icon resource file_rc

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
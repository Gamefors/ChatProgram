# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'T:\ChrisChatprogram\Client\Chris\GUI\LoginFrame\LoginFrame.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Login_Frame(object):
    def setupUi(self, Login_Frame):
        Login_Frame.setObjectName("Login_Frame")
        Login_Frame.resize(540, 209)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/newPrefix/icons8-computer-chat-64.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Login_Frame.setWindowIcon(icon)
        self.buttonBox = QtWidgets.QDialogButtonBox(Login_Frame)
        self.buttonBox.setGeometry(QtCore.QRect(310, 170, 221, 41))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayoutWidget = QtWidgets.QWidget(Login_Frame)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(230, 90, 231, 71))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.Password_Layout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.Password_Layout.setContentsMargins(0, 0, 0, 0)
        self.Password_Layout.setObjectName("Password_Layout")
        self.Password_Line = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.Password_Line.setAccessibleName("")
        self.Password_Line.setText("")
        self.Password_Line.setEchoMode(QtWidgets.QLineEdit.Password)
        self.Password_Line.setDragEnabled(True)
        self.Password_Line.setClearButtonEnabled(False)
        self.Password_Line.setObjectName("Password_Line")
        self.Password_Layout.addWidget(self.Password_Line)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(Login_Frame)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(230, 30, 231, 61))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.User_Layout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.User_Layout.setContentsMargins(0, 0, 0, 0)
        self.User_Layout.setObjectName("User_Layout")
        self.User_line = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.User_line.setDragEnabled(True)
        self.User_line.setObjectName("User_line")
        self.User_Layout.addWidget(self.User_line)
        self.label = QtWidgets.QLabel(Login_Frame)
        self.label.setGeometry(QtCore.QRect(30, 30, 161, 131))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/DefaultUserPic/default-user-profile.jpg"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")

        self.retranslateUi(Login_Frame)
        self.buttonBox.accepted.connect(Login_Frame.accept)
        self.buttonBox.rejected.connect(Login_Frame.reject)
        QtCore.QMetaObject.connectSlotsByName(Login_Frame)

    def retranslateUi(self, Login_Frame):
        _translate = QtCore.QCoreApplication.translate
        Login_Frame.setWindowTitle(_translate("Login_Frame", "Login"))
        self.Password_Line.setPlaceholderText(_translate("Login_Frame", "Password"))
        self.User_line.setPlaceholderText(_translate("Login_Frame", "Username"))

import :/DefaultUserPic_rc
import :/Icon resource file_rc

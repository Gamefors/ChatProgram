import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon

app= QApplication(sys.argv)


w = QWidget()
w.setGeometry(400,100,1000,700)
w.setWindowTitle("Programm")
w.setWindowIcon(QIcon("icons8-discord-logo-48.png"))

w.show()

sys.exit(app.exec_())


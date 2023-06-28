'''
from PyQt6 import QtCore, QtGui, QtWidgets
from serial_port.serial_portPY import scanAvaiableSerialPorts


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(802, 602)
        port = scanAvaiableSerialPorts()
        Dialog.setMinimumSize(QtCore.QSize(802, 602))
        Dialog.setInputMethodHints(QtCore.Qt.InputMethodHint.ImhDigitsOnly)

        self.comboBox.setObjectName('Devices')
        self.comboBox.setGeometry(QtCore.QRect(19, 8, 641, 23))
'''
'''
        self.lineEdit = QtWidgets.QLineEdit(parent=Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(19, 8, 641, 23))
        self.lineEdit.setReadOnly(True)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setText(port[0]) #------------------
'''
'''

        self.pushButton = QtWidgets.QPushButton(parent=Dialog)
        self.pushButton.setGeometry(QtCore.QRect(666, 4, 121, 32))
        self.pushButton.setObjectName("pushButton")
        self.textEdit = QtWidgets.QTextEdit(parent=Dialog)
        self.textEdit.setGeometry(QtCore.QRect(20, 40, 401, 511))
        self.textEdit.setObjectName("textEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(parent=Dialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(615, 40, 166, 21))
        self.lineEdit_2.setInputMethodHints(QtCore.Qt.InputMethodHint.ImhNone)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label = QtWidgets.QLabel(parent=Dialog)
        self.label.setGeometry(QtCore.QRect(430, 40, 60, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(parent=Dialog)
        self.label_2.setGeometry(QtCore.QRect(430, 80, 181, 20))
        self.label_2.setObjectName("label_2")
        self.comboBox = QtWidgets.QComboBox(parent=Dialog)
        self.comboBox.setGeometry(QtCore.QRect(612, 80, 172, 26))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.pushButton_2 = QtWidgets.QPushButton(parent=Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(20, 554, 400, 32))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(parent=Dialog)
        self.pushButton_3.setGeometry(QtCore.QRect(428, 554, 352, 32))
        self.pushButton_3.setObjectName("pushButton_3")

        self.retranslateUi(Dialog)
        Dialog.accepted.connect(self.comboBox.clearEditText)  # type: ignore
        self.lineEdit.editingFinished.connect(self.comboBox.clearEditText)  # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("Dialog", "Подключиться"))
        self.label.setText(_translate("Dialog", "Частота"))
        self.label_2.setText(_translate("Dialog", "Скорость передачи данных"))
        self.comboBox.setItemText(0, _translate("Dialog", "115200"))
        self.comboBox.setItemText(1, _translate("Dialog", "57600"))
        self.comboBox.setItemText(2, _translate("Dialog", "38400"))
        self.comboBox.setItemText(3, _translate("Dialog", "19200"))
        self.comboBox.setItemText(4, _translate("Dialog", "9600"))
        self.comboBox.setItemText(5, _translate("Dialog", "4800"))
        self.pushButton_2.setText(_translate("Dialog", "Запросить телеметрию"))
        self.pushButton_3.setText(_translate("Dialog", "Сохранить"))
'''
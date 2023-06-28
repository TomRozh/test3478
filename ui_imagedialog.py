from PyQt6 import QtCore, QtGui, QtWidgets
from serial_port.serial_portPY import scanAvaiableSerialPorts
from serial_port.serial_portPY import SerialPort
import fpy_vin.fpyVIN as fpyVIN



class Ui_Dialog(object):
    portSelectid = ""
    frequency = 0
    baudrate = 0
    console_text = ""

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(802, 602)
        port = scanAvaiableSerialPorts()
        Dialog.setMinimumSize(QtCore.QSize(802, 602))
        Dialog.setInputMethodHints(QtCore.Qt.InputMethodHint.ImhDigitsOnly)

        self.comboBox_2 = QtWidgets.QComboBox(parent=Dialog)
        self.comboBox_2.setObjectName("Devices")
        self.comboBox_2.setGeometry(QtCore.QRect(19, 8, 641, 23))
        for i in range(0, len(port)): #Добавляем слоты для Devices
            self.comboBox_2.addItem("")
        Ui_Dialog.portSelectid = port[0]

        self.pushButton = QtWidgets.QPushButton(parent=Dialog)
        self.pushButton.setGeometry(QtCore.QRect(666, 4, 121, 32))
        self.pushButton.setObjectName("pushButton")
        self.textEdit = QtWidgets.QTextEdit(parent=Dialog)
        self.textEdit.setGeometry(QtCore.QRect(20, 40, 401, 511))
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setReadOnly(True)

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
        Dialog.accepted.connect(self.comboBox.clearEditText) # type: ignore
        Dialog.accepted.connect(self.comboBox_2.clearEditText)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.comboBox_2.currentTextChanged.connect(self.change_port_button)

    def change_port_button(self):
        self.pushButton.setEnabled(True)
        self.pushButton.setStyleSheet("background-color: #1E90FF; color: white;border-radius:5px;margin-top:5px")
        self.pushButton.setMaximumHeight(25)
        Ui_Dialog.portSelectid = ""
        Ui_Dialog.frequency = self.lineEdit_2.text()
        Ui_Dialog.console_text = ""
        self.textEdit.setText(Ui_Dialog.console_text)
        print(Ui_Dialog.portSelectid)


    def the_button_connect_was_clicked(self):
        Ui_Dialog.console_text = ""
        Ui_Dialog.portSelectid = self.comboBox_2.currentText()
        Ui_Dialog.frequency = self.lineEdit_2.text()
        Ui_Dialog.baudrate = int(self.comboBox.currentText())
        SerialPort.set_baudrate(SerialPort, Ui_Dialog.baudrate)
        if SerialPort(Ui_Dialog.portSelectid,0.1) == True:
            Ui_Dialog.console_text += 'Успешно' + '\n'
            Ui_Dialog.console_text += self.comboBox_2.currentText() + '\n' + 'Частота: ' + self.lineEdit_2.text() + '\n' + 'Скорость передачи данных: ' + self.comboBox.currentText() + '\n' + '\n'
            self.pushButton.setEnabled(False)
            self.pushButton.setStyleSheet("background-color: #262626; color: white;border-radius:5px;margin-top:5px")
            self.pushButton.setMaximumHeight(25)
        else:
            Ui_Dialog.console_text += 'Ошибка' + '\n'
            self.pushButton.setEnabled(True)
            self.pushButton.setStyleSheet("background-color: #1E90FF; color: white;border-radius:5px;margin-top:5px")
            self.pushButton.setMaximumHeight(25)
        self.textEdit.setText(Ui_Dialog.console_text)


    def the_button_save_was_clicked(self):
        Ui_Dialog.frequency = self.lineEdit_2.text()
        Ui_Dialog.baudrate = int(self.comboBox.currentText())
        if SerialPort.set_baudrate(SerialPort, Ui_Dialog.baudrate) == True:
            Ui_Dialog.console_text += self.comboBox_2.currentText()+'\n'+'Частота: '+self.lineEdit_2.text()+'\n'+'Скорость передачи данных: '+self.comboBox.currentText()+'\n'+'\n'
            self.textEdit.setText(Ui_Dialog.console_text)
        else:
            Ui_Dialog.console_text += 'Ошибка' +'\n'
            self.textEdit.setText(Ui_Dialog.console_text)

    def the_button_telemetria_clicked(self):
        fpyVIN.VINMachine.serial_port = Ui_Dialog.portSelectid
        Ui_Dialog.console_text += fpyVIN.VINMachine.command_a(fpyVIN.VINMachine, "0x00", fpyVIN.VINMachine.test_cmd)
        self.textEdit.setText(Ui_Dialog.console_text)

    def retranslateUi(self, Dialog):
        port = scanAvaiableSerialPorts()
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


        self.pushButton.clicked.connect(self.the_button_connect_was_clicked)
        self.pushButton_2.clicked.connect(self.the_button_telemetria_clicked)
        self.pushButton_3.clicked.connect(self.the_button_save_was_clicked)


        for i in range(0, len(port)):
            self.comboBox_2.setItemText(i, _translate("Dialog", port[i]))

        self.pushButton_2.setText(_translate("Dialog", "Запросить телеметрию"))
        self.pushButton_3.setText(_translate("Dialog", "Сохранить"))




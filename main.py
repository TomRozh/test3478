import sys
from PyQt6.QtWidgets import QApplication,QDialog
from ui_imagedialog import Ui_Dialog

app = QApplication(sys.argv)
window = QDialog()
ui = Ui_Dialog()
ui.setupUi(window)
window.show()
sys.exit(app.exec())

#pyuic6 ui_imagedialog.ui -o  ui_imagedialog.py
#self.lineEdit_2.setValidator(QDoubleValidator(0,1000000000,1))
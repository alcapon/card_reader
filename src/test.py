import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QDialog

class MyDialog(QDialog):
    def __init__(self):
        super(MyDialog, self).__init__()
        # โหลดไฟล์ test.ui
        uic.loadUi("src/test.ui", self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = MyDialog()
    dialog.show()
    sys.exit(app.exec_())

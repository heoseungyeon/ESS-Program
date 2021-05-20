import sys
from PyQt5.QtWidgets import QApplication, QWidget


class EssApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('ESS Program')
        self.move(850,100)
        self.resize(800, 500)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = EssApp()
    sys.exit(app.exec_())
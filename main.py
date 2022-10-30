import sys
import PyQt5.QtWidgets as qtw
from MainWindow import MainWindow


def main():
    app = qtw.QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("Snake")
    # We could get a fixed width and height for our window here

    window.setStyleSheet("background: #3493eb")

    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

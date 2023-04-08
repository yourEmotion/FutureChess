from PyQt5.QtWidgets import QApplication
import sys
from MainMenu import MainMenu
from PyQt5.QtWidgets import QWidget


def launch_app():
    app = QApplication(sys.argv)
    print(QWidget().frameGeometry())
    window = MainMenu()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    launch_app()

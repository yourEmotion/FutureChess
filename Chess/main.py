from PyQt5.QtWidgets import QApplication
import sys
from Window import MainMenu

def launch_app():
    app = QApplication(sys.argv)
    main_menu = MainMenu()
    main_menu.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    launch_app()

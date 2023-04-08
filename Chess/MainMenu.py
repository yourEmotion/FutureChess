from PyQt5.QtWidgets import QWidget, QDesktopWidget
from Button import *
from collections import defaultdict


WIDTH = 512
HEIGHT = 512
WIDTH_INDENT = 500
HEIGHT_INDENT = 300

class MainMenu(QWidget):
    buttons = defaultdict()

    def __init__(self):
        super().__init__()
        self.setFixedWidth(WIDTH)
        self.setFixedHeight(HEIGHT)
        self.setGeometry(WIDTH_INDENT, HEIGHT_INDENT, WIDTH, HEIGHT)
        self.setWindowTitle("Chess")
        #self.buttons["Settings"] = SettingsButton(self)
        self.buttons["Play"] = PlayButton(self)
        #self.buttons["Play vs AI"] = PlayAIButton(self)

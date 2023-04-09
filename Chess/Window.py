from collections import defaultdict
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel
from ChessMain import Game


WIDTH = 700
HEIGHT = 600
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

        self.buttons["Play"] = QPushButton(self)
        self.buttons["Play"].setGeometry(0, 0, 670, 100)
        self.buttons["Play"].move(15, 355)
        self.buttons["Play"].setText("Play!")
        self.buttons["Play"].setStyleSheet("background-color: green")
        self.buttons["Play"].clicked.connect(self.playButtonPress)

        self.buttons["Credits"] = QPushButton(self)
        self.buttons["Credits"].setGeometry(0, 0, 670, 100)
        self.buttons["Credits"].move(15, 485)
        self.buttons["Credits"].setText("Play!")
        self.buttons["Credits"].setStyleSheet("background-color: blue")
        self.buttons["Credits"].clicked.connect(self.creditsButtonPress)

    def playButtonPress(self):
        self.hide()
        result = Game()
        if result["game finished"]:
            if result["white victory"]:
                self.new_window = WhiteVictoryWindow()
            elif result["black victory"]:
                self.new_window = BlackVictoryWindow()
            else:
                self.new_window = DrawWindow()
            self.new_window.show()
        else:
            self.show()

    def creditsButtonPress(self):
        pass


class GameOverWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.label = QLabel()
        self.label.move(100, 100)
        self.label.adjustSize()
        self.setFixedWidth(WIDTH)
        self.setFixedHeight(HEIGHT)
        self.setGeometry(WIDTH_INDENT, HEIGHT_INDENT, WIDTH, HEIGHT)
        self.setWindowTitle(" ")
        self.show()

    def closeEvent(self, event):
        event.accept()
        self.new_window = MainMenu()
        self.new_window.show()


class DrawWindow(GameOverWindow):
    def __init__(self):
        super(DrawWindow, self).__init__()
        self.label.setText("DRAW")


class WhiteVictoryWindow(GameOverWindow):
    def __init__(self):
        super(WhiteVictoryWindow, self).__init__()
        self.label.setText("WHITE WON!")


class BlackVictoryWindow(GameOverWindow):
    def __init__(self):
        super(BlackVictoryWindow, self).__init__()
        self.label.setText("BLACK WON!")


class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(1000, 100, 800, 1000)
        self.setWindowTitle("Settings")


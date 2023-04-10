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
        self.buttons["Credits"].setText("Credits")
        self.buttons["Credits"].setStyleSheet("background-color: blue")
        self.buttons["Credits"].clicked.connect(self.creditsButtonPress)

    def playButtonPress(self):
        self.hide()
        result = Game()
        self.show()

    def creditsButtonPress(self):
        self.hide()
        self.new_window = CreditsWindow()

    def closeEvent(self, event):
        event.accept()
        self.show()

class GameOverWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.label = QLabel()
        self.setFixedWidth(WIDTH)
        self.setFixedHeight(HEIGHT)
        self.setGeometry(WIDTH_INDENT, HEIGHT_INDENT, WIDTH, HEIGHT)
        self.setWindowTitle("Game result")

    def closeEvent(self, event):
        event.accept()
        self.new_window = MainMenu()
        self.new_window.show()


class DrawWindow(GameOverWindow):
    def __init__(self):
        super(DrawWindow, self).__init__()
        self.label = QLabel('Draw!', self)
        self.label.setStyleSheet("color: red")
        self.label.move(WIDTH // 2 - 100, 100)
        self.label.setFixedSize(400, 400)
        self.font = self.label.font()
        self.font.setPointSize(32)
        self.label.setFont(self.font)
        self.show()


class WhiteVictoryWindow(GameOverWindow):
    def __init__(self):
        super(WhiteVictoryWindow, self).__init__()
        self.label = QLabel('White won!', self)
        self.label.setStyleSheet("color: red")
        self.label.move(WIDTH // 2 - 105, 100)
        self.label.setFixedSize(400, 400)
        self.font = self.label.font()
        self.font.setPointSize(32)
        self.label.setFont(self.font)
        self.show()


class BlackVictoryWindow(GameOverWindow):
    def __init__(self):
        super(BlackVictoryWindow, self).__init__()
        self.label = QLabel('Black won!', self)
        self.label.setStyleSheet("color: red")
        self.label.move(WIDTH // 2 - 100, 100)
        self.label.setFixedSize(400, 400)
        self.font = self.label.font()
        self.font.setPointSize(32)
        self.label.setFont(self.font)
        self.show()


class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(WIDTH)
        self.setFixedHeight(HEIGHT)
        self.setGeometry(WIDTH_INDENT, HEIGHT_INDENT, WIDTH, HEIGHT)
        self.setWindowTitle("Settings")


class CreditsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(WIDTH)
        self.setFixedHeight(HEIGHT)
        self.setGeometry(WIDTH_INDENT, HEIGHT_INDENT, WIDTH, HEIGHT)
        self.setWindowTitle("Credits")

        self.title = QLabel('Credits', self)
        self.title.setStyleSheet("color: black; font-weight: bold")
        self.title.move(WIDTH // 2 - 75, 30)
        self.title.setFixedSize(WIDTH, 100)
        self.font_title = self.title.font()
        self.font_title.setPointSize(32)
        self.title.setFont(self.font_title)

        self.text = QLabel(
            "     This app was created by Ermoshin Mikhail and Gromakov Ilia, 2nd year" + "\n" +
            "MIPT students, as a project for the course \"Python Programming\". If you" + "\n" +
            "find errors in the operation of this app, please report them to the mail:" + "\n" +
            "ermoshin.me@phystech.edu" + "\n\n\n" + "You also can share this project with your friends. " +
            "Enjoy it!",
            self)
        self.text.setStyleSheet("color: black")
        self.text.move(40, 200)
        self.text.setFixedSize(WIDTH - 30, 300)
        self.font_text = self.text.font()
        self.font_text.setPointSize(14)
        self.text.setFont(self.font_text)

        self.show()

    def closeEvent(self, event):
        event.accept()
        self.new_window = MainMenu()
        self.new_window.show()


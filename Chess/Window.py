from collections import defaultdict
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QMainWindow
from ChessMain import Game
from random import randint


WIDTH = 700
HEIGHT = 600
WIDTH_INDENT = 500
HEIGHT_INDENT = 300


class MainMenu(QMainWindow):
    buttons = defaultdict()

    def __init__(self):
        super().__init__()
        self.setFixedWidth(WIDTH)
        self.setFixedHeight(HEIGHT)
        self.setGeometry(WIDTH_INDENT, HEIGHT_INDENT, WIDTH, HEIGHT)
        self.setWindowTitle("Chess")
        self.setStyleSheet("background-color: white")

        self.pixmap = QPixmap('images/chess_picture.png')

        self.label = QLabel(self)
        self.label.setPixmap(self.pixmap)
        self.label.setGeometry(1, 1, WIDTH - 2, HEIGHT - 251)
        self.label.setScaledContents(True)

        self.buttons["Play1v1"] = QPushButton(self)
        self.buttons["Play1v1"].setGeometry(0, 0, 320, 100)
        self.buttons["Play1v1"].move(15, 365)
        self.buttons["Play1v1"].setText("Play 1v1")
        self.buttons["Play1v1"].setStyleSheet("background-color: green")
        self.buttons["Play1v1"].clicked.connect(self.play1v1ButtonPress)

        self.buttons["PlayAI"] = QPushButton(self)
        self.buttons["PlayAI"].setGeometry(0, 0, 330, 100)
        self.buttons["PlayAI"].move(353, 365)
        self.buttons["PlayAI"].setText("Play vs AI")
        self.buttons["PlayAI"].setStyleSheet("background-color: green")
        self.buttons["PlayAI"].clicked.connect(self.playVsAIButtonPress)

        self.buttons["Settings"] = QPushButton(self)
        self.buttons["Settings"].setGeometry(0, 0, 320, 100)
        self.buttons["Settings"].move(15, 485)
        self.buttons["Settings"].setText("Settings")
        self.buttons["Settings"].setStyleSheet("background-color: brown")
        self.buttons["Settings"].clicked.connect(self.settingsButtonPress)

        self.buttons["Credits"] = QPushButton(self)
        self.buttons["Credits"].setGeometry(0, 0, 330, 100)
        self.buttons["Credits"].move(353, 485)
        self.buttons["Credits"].setText("Credits")
        self.buttons["Credits"].setStyleSheet("background-color: blue")
        self.buttons["Credits"].clicked.connect(self.creditsButtonPress)

    def play1v1ButtonPress(self):
        self.hide()
        Game(white_is_human=True, black_is_human=True)
        self.show()

    def playVsAIButtonPress(self):
        self.hide()
        human = randint(0, 1)
        if human == 0:
            Game(white_is_human=True, black_is_human=False)
        else:
            Game(white_is_human=False, black_is_human=True)
        self.show()

    def settingsButtonPress(self):
        self.hide()
        self.new_window = SettingsWindow()
    def creditsButtonPress(self):
        self.hide()
        self.new_window = CreditsWindow()


class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(WIDTH)
        self.setFixedHeight(HEIGHT)
        self.setGeometry(WIDTH_INDENT, HEIGHT_INDENT, WIDTH, HEIGHT)
        self.setWindowTitle("Settings")

        self.title = QLabel('Settings', self)
        self.title.setStyleSheet("color: black; font-weight: bold")
        self.title.move(WIDTH // 2 - 75, 30)
        self.title.setFixedSize(WIDTH, 100)
        self.font_title = self.title.font()
        self.font_title.setPointSize(32)
        self.title.setFont(self.font_title)

        self.show()

    def closeEvent(self, event):
        event.accept()
        self.new_window = MainMenu()
        self.new_window.show()


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

from collections import defaultdict

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QMainWindow, QRadioButton

from game_runner import game

WIDTH = 700
HEIGHT = 600
WIDTH_INDENT = 500
HEIGHT_INDENT = 300

BOARD_COLOR = "white-gray"


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
        self.buttons["Play1v1"].clicked.connect(self.play1v1_button_press)

        self.buttons["PlayAI"] = QPushButton(self)
        self.buttons["PlayAI"].setGeometry(0, 0, 330, 100)
        self.buttons["PlayAI"].move(353, 365)
        self.buttons["PlayAI"].setText("Play vs AI")
        self.buttons["PlayAI"].setStyleSheet("background-color: green")
        self.buttons["PlayAI"].clicked.connect(self.play_vs_ai_button_press)

        self.buttons["Settings"] = QPushButton(self)
        self.buttons["Settings"].setGeometry(0, 0, 320, 100)
        self.buttons["Settings"].move(15, 485)
        self.buttons["Settings"].setText("Settings")
        self.buttons["Settings"].setStyleSheet("background-color: brown")
        self.buttons["Settings"].clicked.connect(self.settings_button_press)

        self.buttons["Credits"] = QPushButton(self)
        self.buttons["Credits"].setGeometry(0, 0, 330, 100)
        self.buttons["Credits"].move(353, 485)
        self.buttons["Credits"].setText("Credits")
        self.buttons["Credits"].setStyleSheet("background-color: blue")
        self.buttons["Credits"].clicked.connect(self.credits_button_press)

    def play1v1_button_press(self):
        self.hide()
        game(white_is_human=True, black_is_human=True, board_color=BOARD_COLOR)
        self.show()

    def play_vs_ai_button_press(self):
        self.hide()
        self.new_window = ChoiceColorWindow()

    def settings_button_press(self):
        self.hide()
        self.new_window = SettingsWindow()

    def credits_button_press(self):
        self.hide()
        self.new_window = CreditsWindow()


class ChoiceColorWindow(QWidget):
    white_chosen = None
    buttons = defaultdict()

    def __init__(self):
        super().__init__()
        self.setFixedWidth(WIDTH)
        self.setFixedHeight(HEIGHT)
        self.setGeometry(WIDTH_INDENT, HEIGHT_INDENT, WIDTH, HEIGHT)
        self.setWindowTitle("Color choice")

        self.title = QLabel('Choose the color', self)
        self.title.setStyleSheet("color: black; font-weight: bold")
        self.title.move(WIDTH // 2 - 160, 30)
        self.title.setFixedSize(WIDTH, 100)
        self.font_title = self.title.font()
        self.font_title.setPointSize(32)
        self.title.setFont(self.font_title)

        for index, color in enumerate(("white", "black")):
            self.buttons[color] = QPushButton(self)
            self.buttons[color].setStyleSheet("background-color: green; font-weight: bold; color: " + color)
            self.buttons[color].setGeometry(0, 0, 280, 200)
            self.buttons[color].move(35 + index * 350, 250)
            self.buttons[color].setText(color)
            self.font = self.buttons[color].font()
            self.font.setPointSize(32)
            self.buttons[color].setFont(self.font)

        self.buttons["white"].clicked.connect(self.white_start_button_press)
        self.buttons["black"].clicked.connect(self.black_start_button_press)

        self.show()

    def white_start_button_press(self):
        self.hide()
        game(white_is_human=True, black_is_human=False, board_color=BOARD_COLOR)
        self.new_window = MainMenu()
        self.new_window.show()

    def black_start_button_press(self):
        self.hide()
        game(white_is_human=False, black_is_human=True, board_color=BOARD_COLOR)
        self.new_window = MainMenu()
        self.new_window.show()

    def closeEvent(self, event):
        event.accept()
        self.new_window = MainMenu()
        self.new_window.show()


class SettingsWindow(QWidget):
    buttons = defaultdict()

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

        self.board_color = QLabel('Choose board color:', self)
        self.board_color.setStyleSheet("color: black; font-weight: bold")
        self.board_color.move(WIDTH // 2 - 90, 100)
        self.board_color.setFixedSize(WIDTH, 100)
        self.font_board_color = self.board_color.font()
        self.font_board_color.setPointSize(16)
        self.board_color.setFont(self.font_board_color)

        self.board_colors = ("white-gray", "white-green", "white-blue", "white-brown")
        for index, color in enumerate(self.board_colors):
            self.buttons[color] = QRadioButton(self)
            self.buttons[color].setGeometry(0, 0, 300, 50)
            self.buttons[color].move(25 + index * 180, 175)
            self.buttons[color].setText(color)
        self.buttons[BOARD_COLOR].setChecked(True)

        self.buttons["white-gray"].toggled.connect(self.white_gray_button_press)
        self.buttons["white-green"].toggled.connect(self.white_green_button_press)
        self.buttons["white-blue"].toggled.connect(self.white_blue_button_press)
        self.buttons["white-brown"].toggled.connect(self.white_brown_button_press)

        self.show()

    def white_gray_button_press(self):
        global BOARD_COLOR
        BOARD_COLOR = "white-gray"

    def white_green_button_press(self):
        global BOARD_COLOR
        BOARD_COLOR = "white-green"

    def white_blue_button_press(self):
        global BOARD_COLOR
        BOARD_COLOR = "white-blue"

    def white_brown_button_press(self):
        global BOARD_COLOR
        BOARD_COLOR = "white-brown"

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

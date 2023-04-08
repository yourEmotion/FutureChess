from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QSizePolicy, QWidget
from SettingsWindow import SettingsWindow
from ChessMain import *


class Button():
    def __init__(self, window):
        self.button = QtWidgets.QPushButton(window)
        self.button.setBaseSize(500, 500)
        self.button.setSizePolicy(QSizePolicy())


'''class SettingsButton(Button):
    def __init__(self, window):
        super().__init__(window)
        self.button.move(200, 200)
        self.button.setText("Настройки")
        self.button.setStyleSheet("background-color: white")
        self.button.clicked.connect(self.press)

    def press(self):
        self.new_window = SettingsWindow()
        self.new_window.show()
'''

class PlayButton(Button):
    def __init__(self, window):
        super().__init__(window)
        self.window = window
        self.button.move(WIDTH // 2, HEIGHT // 2)
        self.button.setText("Play!")
        self.button.setStyleSheet("background-color: blue")
        self.button.clicked.connect(self.press)
        self.board = None

    def press(self):
        self.window.hide()
        Game()
        self.window.show()


'''class PlayAIButton(Button):
    def __init__(self, window):
        super().__init__(window)
        self.button.move(200, 800)
        self.button.setText("Играть против ИИ")
        self.button.setStyleSheet("background-color: red")'''

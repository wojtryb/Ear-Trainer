from typing import Callable

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QPushButton,
    QVBoxLayout,
    QGridLayout,
    QWidget,
    QLabel)

from melody_navigator import MelodyNavigator


class MainWindow(QWidget):

    def __init__(
        self,
        request_new_tune_cb: Callable[[], MelodyNavigator],
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self._request_new_tune_cb = request_new_tune_cb

        self._navigator = self._request_new_tune_cb()

        self._image_widget = HideableImageWidget()
        self._repeat_button = self._init_repeat_button()
        self._continue_button = self._init_continue_button()
        self._select_next_button = self._init_select_next_button()
        self._select_previous_button = self._init_select_previous_button()

        self.setLayout(self._init_layout())
        self.resize(1200, 500)

    def _init_layout(self) -> QVBoxLayout:
        layout = QVBoxLayout()
        layout.addWidget(self._image_widget)

        navigator = QGridLayout()
        navigator.addWidget(self._select_previous_button, 0, 0, 0, 1)
        navigator.addWidget(self._select_next_button, 0, 1, 0, 1)
        layout.addLayout(navigator)

        footer = QGridLayout()
        footer.addWidget(self._repeat_button, 0, 0, 1, 1)
        footer.addWidget(self._continue_button, 0, 1, 1, 2)
        layout.addLayout(footer)
        return layout

    def _init_repeat_button(self) -> QPushButton:
        def on_click():
            self._navigator.play_whole()

        button = QPushButton(text="Repeat tune")
        button.clicked.connect(on_click)
        button.setFixedHeight(button.sizeHint().height()*2)
        return button

    def _init_continue_button(self) -> QPushButton:
        def on_click() -> None:
            if not self._image_widget.is_revealed:
                self._image_widget.is_revealed = True
                self._continue_button.setText("Continue")
                self._continue_button.setStyleSheet(
                    "background-color: darkgreen")
            else:
                self._image_widget.is_revealed = False
                self._continue_button.setText("Reveal")
                self._continue_button.setStyleSheet("")
                self.repaint()
                self._navigator = self._request_new_tune_cb()
                self._navigator.play_whole()
                self._image_widget.load_from_navigator(self._navigator)

        button = QPushButton(text="Start")
        button.clicked.connect(on_click)
        button.setFixedHeight(button.sizeHint().height()*2)
        return button

    def _init_select_next_button(self) -> QPushButton:
        def on_click():
            self._navigator.select_next_note()
            self._navigator.play_selection()
        button = QPushButton(text=">")
        button.clicked.connect(on_click)
        button.setFixedHeight(button.sizeHint().height()*2)
        return button

    def _init_select_previous_button(self) -> QPushButton:
        def on_click():
            self._navigator.select_previous_note()
            self._navigator.play_selection()
        button = QPushButton(text="<")
        button.clicked.connect(on_click)
        button.setFixedHeight(button.sizeHint().height()*2)
        return button


class HideableImageWidget(QLabel):

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.setStyleSheet("QLabel { background-color : white }")
        self.setAlignment(Qt.AlignCenter)  # type: ignore

        self._current_image = QPixmap()
        self._is_revealed = True

    @property
    def is_revealed(self) -> bool:
        return self._is_revealed

    @is_revealed.setter
    def is_revealed(self, value: bool):
        if value:
            self.setPixmap(self._current_image)
        else:
            self.setPixmap(QPixmap())

        self._is_revealed = value

    def load_from_navigator(self, navigator: MelodyNavigator):
        path = navigator.request_image()
        self._current_image = QPixmap(path)

        if self.is_revealed:
            self.setPixmap(self._current_image)

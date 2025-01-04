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

        self._select_previous_button = self._init_button(
            self.perform_select_previous, "<")
        self._repeat_selection_button = self._init_button(
            self.perform_repeat_selection, "O")
        self._select_next_button = self._init_button(
            self.perform_select_next, ">")
        self._repeat_melody_button = self._init_button(
            self.perform_repeat_melody, "Repeat melody")
        self._continue_button = self._init_button(
            self.perform_continue, "Start")

        self.setLayout(self._init_layout())
        self.resize(1200, 500)

    def _init_layout(self) -> QVBoxLayout:
        layout = QVBoxLayout()
        layout.addWidget(self._image_widget)

        footer = QGridLayout()
        footer.addWidget(self._select_previous_button, 0, 0, 0, 1)
        footer.addWidget(self._repeat_selection_button, 0, 1, 0, 1)
        footer.addWidget(self._select_next_button, 0, 2, 0, 1)
        footer.addWidget(self._repeat_melody_button, 0, 3, 0, 3)
        footer.addWidget(self._continue_button, 0, 6, 0, 5)
        layout.addLayout(footer)

        return layout

    def perform_repeat_melody(self):
        self._navigator.play_whole()

    def perform_continue(self):
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

    def perform_select_next(self):
        self._navigator.select_next_note()
        self._navigator.play_selection()

    def perform_select_previous(self):
        self._navigator.select_previous_note()
        self._navigator.play_selection()

    def perform_repeat_selection(self):
        self._navigator.play_selection()

    def _init_button(self, on_click_callback: Callable[[], None], text: str):
        button = QPushButton(text=text)
        button.clicked.connect(on_click_callback)
        button.setFixedHeight(button.sizeHint().height()*2)
        return button

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_J:  # type: ignore
            self.perform_select_previous()
        if event.key() == Qt.Key_L:  # type: ignore
            self.perform_select_next()
        if event.key() == Qt.Key_K:  # type: ignore
            self.perform_repeat_selection()
        if event.key() == Qt.Key_I:  # type: ignore
            self.perform_repeat_melody()
        if event.key() == Qt.Key_U:  # type: ignore
            self.perform_continue()


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

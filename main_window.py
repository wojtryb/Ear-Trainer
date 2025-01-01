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
        self._is_revealed_state = True

        self._image_widget = self._init_image_widget()
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

    def _init_image_widget(self) -> QLabel:
        image_widget = QLabel(self)
        image_widget.setStyleSheet("QLabel { background-color : white }")
        image_widget.setAlignment(Qt.AlignCenter)  # type: ignore
        return image_widget

    def _init_repeat_button(self) -> QPushButton:
        def do_stuff():
            self._navigator.play_whole()

        button = QPushButton(text="Repeat tune")
        button.clicked.connect(do_stuff)
        button.setFixedHeight(button.sizeHint().height()*2)
        return button

    def _init_continue_button(self) -> QPushButton:
        def do_stuff() -> None:
            if not self._is_revealed_state:
                self._update_image()
                self._continue_button.setText("Continue")
                self._continue_button.setStyleSheet(
                    "background-color: darkgreen")
                self._is_revealed_state = True
            else:
                self._reset_image()
                self._continue_button.setText("Reveal")
                self._continue_button.setStyleSheet("")
                self.repaint()
                self._navigator = self._request_new_tune_cb()
                self._navigator.play_whole()
                self._is_revealed_state = False

        button = QPushButton(text="Start")
        button.clicked.connect(do_stuff)
        button.setFixedHeight(button.sizeHint().height()*2)
        return button

    def _init_select_next_button(self) -> QPushButton:
        def do_stuff():
            self._navigator.select_next_note()
            self._navigator.play_selection()
        button = QPushButton(text=">")
        button.clicked.connect(do_stuff)
        button.setFixedHeight(button.sizeHint().height()*2)
        return button

    def _init_select_previous_button(self) -> QPushButton:
        def do_stuff():
            self._navigator.select_previous_note()
            self._navigator.play_selection()
        button = QPushButton(text="<")
        button.clicked.connect(do_stuff)
        button.setFixedHeight(button.sizeHint().height()*2)
        return button

    def _reset_image(self) -> None:
        self._image_widget.setPixmap(QPixmap())

    def _update_image(self) -> None:
        path = self._navigator.request_image()
        pixmap = QPixmap(path)
        self._image_widget.setPixmap(pixmap)

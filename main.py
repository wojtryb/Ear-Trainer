import sys
from threading import Thread

from PyQt5.QtWidgets import QApplication

from music21.stream.base import Score

from main_window import MainWindow
from melody_generators import generate_diatonic_melody


class Logic:
    def __init__(self) -> None:
        self._last_melody: Score | None = None
        self.request_new_tune()

    def play_tune(self):
        if self._last_melody is None:
            raise RuntimeError("No melody provided")

        thread = Thread(target=self._last_melody.show, args=['midi'])
        thread.daemon = True
        thread.start()

    def request_new_tune(self) -> str:
        self._last_melody = generate_diatonic_melody()
        return str(self._last_melody.write("musicxml.png"))


app = QApplication(sys.argv)
logic = Logic()

window = MainWindow(logic.play_tune, logic.request_new_tune)
window.show()

app.exec()

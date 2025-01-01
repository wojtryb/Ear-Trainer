import sys

from PyQt5.QtWidgets import QApplication

from main_window import MainWindow
from melody_generators import generate_diatonic_melody
from melody_navigator import MelodyNavigator


def request_new_tune() -> MelodyNavigator:
    melody = generate_diatonic_melody()
    return MelodyNavigator(melody)


app = QApplication(sys.argv)

window = MainWindow(request_new_tune)
window.show()

app.exec()

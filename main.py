import sys

from PyQt5.QtWidgets import QApplication

from music21 import instrument

import scale_generators
from main_window import MainWindow
from melody_generators import random_step_melody
from melody_navigator import MelodyNavigator


def request_new_tune() -> MelodyNavigator:
    scale = scale_generators.random_diatonic()
    # scale = scale_generators.random_chromatic()
    melody = random_step_melody(scale, notes_to_play=4, max_jump=3)
    return MelodyNavigator(melody, instrument.Piano())


app = QApplication(sys.argv)

window = MainWindow(request_new_tune)
window.show()

sys.exit(app.exec_())

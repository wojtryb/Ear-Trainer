from threading import Thread

from music21.note import Note
from music21.stream.base import Score
from music21.tempo import MetronomeMark


def get_notes(melody: Score):
    # TODO: support chords too
    return melody.getElementsByClass(Note)


class MelodyNavigator:

    def __init__(self, melody: Score):
        self._melody = melody
        self._selection: int | None = None

    def request_image(self):
        return str(self._melody.write("musicxml.png"))

    def play_whole(self, tempo: int = 90):
        score_with_tempo = Score(MetronomeMark(tempo))
        score_with_tempo.append(self._melody)

        thread = Thread(target=score_with_tempo.show, args=['midi'])
        thread.daemon = True
        thread.start()

    def play_selection(self, tempo: int = 90):
        if self._selection is None:
            return

        note = get_notes(self._melody)[self._selection]
        score_with_tempo = Score(MetronomeMark(tempo))
        score_with_tempo.append(note)
        thread = Thread(target=score_with_tempo.show, args=['midi'])
        thread.daemon = True
        thread.start()

    def select_next_note(self):
        if self._selection is None:
            self._selection = 0
        else:
            self._selection += 1

        if self._selection >= len(get_notes(self._melody)):
            self._selection = 0

    def select_previous_note(self):
        notes = get_notes(self._melody)
        if self._selection is None:
            self._selection = len(notes)-1
        else:
            self._selection -= 1

        if self._selection < 0:
            self._selection = len(notes)-1

    def deselect(self):
        self._selection = None

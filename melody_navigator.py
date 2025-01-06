from threading import Thread
from copy import deepcopy

from music21.instrument import Instrument
from music21.note import Note
from music21.interval import Interval
from music21.stream.base import Score
from music21.tempo import MetronomeMark


def get_notes(melody: Score):
    # TODO: support chords too
    return melody.getElementsByClass(Note)


class MelodyNavigator:

    def __init__(self, melody: Score, instrument: Instrument):
        self._melody = melody
        self._instrument = instrument
        self._selection: int | None = None

    def request_image(self):
        melody = deepcopy(self._melody)

        notes = melody.getElementsByClass(Note)
        for note_1, note_2 in zip(notes, notes[1:]):
            interval = Interval(pitchStart=note_1.pitch, pitchEnd=note_2.pitch)
            note_2.addLyric(interval.name)

        return str(melody.write("musicxml.png"))

    def play_whole(self, tempo: int = 90):
        score_with_tempo = deepcopy(self._melody)
        score_with_tempo.insert(MetronomeMark(tempo))
        score_with_tempo.insert(self._instrument)

        thread = Thread(target=score_with_tempo.show, args=['midi'])
        thread.daemon = True
        thread.start()

    def play_selection(self, tempo: int = 90):
        if self._selection is None:
            return

        note = get_notes(self._melody)[self._selection]
        score_with_tempo = Score(MetronomeMark(tempo))
        score_with_tempo.insert(self._instrument)
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

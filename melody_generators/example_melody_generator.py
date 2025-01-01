import random

from music21.note import Note
from music21.stream.base import Score
from music21.scale import MinorScale, MajorScale, ChromaticScale
from music21.interval import Interval
from music21.tempo import MetronomeMark


def generate_diatonic_melody() -> Score:
    NOTES_TO_PLAY = 4
    MAX_JUMP = 2
    TEMPO = 120

    note_ids_to_play = [random.choice((0, 7))]
    for _ in range(NOTES_TO_PLAY-1):
        last_note = note_ids_to_play[-1]
        min_note_id = max(0, last_note-MAX_JUMP)
        max_note_id = min(7, last_note+MAX_JUMP)
        ids = [id for id in range(min_note_id, max_note_id+1)
               if not id == last_note]
        note_ids_to_play.append(random.choice(ids))

    scale_type = random.choice((MajorScale, MinorScale))
    key = random.choice(ChromaticScale().getPitches())
    pitches = [pitch for pitch in scale_type(key).getPitches()]

    output_melody = Score()
    output_melody.append(MetronomeMark(TEMPO))
    for id in note_ids_to_play:
        note = Note(pitches[id])
        output_melody.append(note)

    notes = output_melody.getElementsByClass(Note)
    for note_1, note_2 in zip(notes, notes[1:]):
        interval = Interval(pitchStart=note_1.pitch, pitchEnd=note_2.pitch)
        note_2: Note
        note_2.addLyric(interval.name)

    return output_melody

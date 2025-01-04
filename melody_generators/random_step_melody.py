import random

from music21.note import Note
from music21.stream.base import Score
from music21.scale import ConcreteScale


def random_step_melody(
    scale: ConcreteScale,
    notes_to_play: int,
    max_jump: int
) -> Score:
    pitches = [pitch for pitch in scale.getPitches()]

    first_note_id = random.choice((0, len(pitches)-1))
    note_ids_to_play = [first_note_id]
    for _ in range(notes_to_play-1):
        last_note = note_ids_to_play[-1]
        min_note_id = max(0, last_note-max_jump)
        max_note_id = min(len(pitches)-1, last_note+max_jump)
        possibilities = [id for id in range(min_note_id, max_note_id+1)
                         if not id == last_note]
        note_ids_to_play.append(random.choice(possibilities))

    output_melody = Score()
    for id in note_ids_to_play:
        output_melody.append(Note(pitches[id]))

    return output_melody

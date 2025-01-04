import random

from music21.scale import MinorScale, MajorScale, ChromaticScale, ConcreteScale


def random_diatonic() -> ConcreteScale:
    scale_type = random.choice((MajorScale, MinorScale))
    tonic = random.choice(ChromaticScale().getPitches("C2", "C5"))
    scale = scale_type(tonic)
    return scale


def random_chromatic() -> ChromaticScale:
    tonic = random.choice(ChromaticScale().getPitches("C2", "C5"))
    return ChromaticScale(tonic)

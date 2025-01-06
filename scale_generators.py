import random

from music21.scale import MinorScale, MajorScale, ChromaticScale, ConcreteScale


def random_diatonic(lowest_tonic: str, highest_tonic: str) -> ConcreteScale:
    scale_type = random.choice((MajorScale, MinorScale))
    tonic = random.choice(ChromaticScale().getPitches(
        lowest_tonic, highest_tonic))
    scale = scale_type(tonic)
    return scale


def random_chromatic(lowest_tonic: str, highest_tonic: str) -> ChromaticScale:
    tonic = random.choice(ChromaticScale().getPitches(
        lowest_tonic, highest_tonic))
    return ChromaticScale(tonic)

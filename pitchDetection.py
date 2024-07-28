import numpy as np
import os

BASIC_PITCH = 440
NOTES = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]

def findNote(freq):
    # detect the current half step away from 440Hz
    halfStep = int(np.round(np.log2(freq / BASIC_PITCH) * 12))
    closePitch = BASIC_PITCH * 2 ** (halfStep / 12)
    closeNote = NOTES[halfStep % 12]

    return closePitch, closeNote
    

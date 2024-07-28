import time
import sounddevice as sd
import numpy as np
import scipy.fftpack
import os

SAMPLE_FREQ = 44100 # Sampling frequency of the recording
SAMPLE_DUR = 2  # Duration of the recoding

time.sleep(1)
myRecording = sd.rec(SAMPLE_DUR * SAMPLE_FREQ, samplerate=SAMPLE_FREQ, channels=1,dtype='float64')
print("Recording audio")
sd.wait()

sd.play(myRecording, SAMPLE_FREQ)
print("Playing audio")
sd.wait()
    
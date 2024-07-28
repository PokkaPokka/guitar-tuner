import sounddevice as sd
import numpy as np
import scipy.fftpack
import os
import tkinter as tk
from tkinter import ttk
import threading
from pitchDetection import findNote

# GUI class
class TunerGUI:
    def __init__(self, root):
        self.root = root
        root.title("Guitar Tuner")

        self.canvas = tk.Canvas(root, width=140, height=35)
        self.canvas.pack(padx=5, pady=(10, 0))

        colors = ['#F5BF4F'] * 3 + ['#99dc74'] + ['#ED6A5E'] * 3
        self.bars = [self.canvas.create_rectangle
                     (i*20, 0, (i+1)*20, 20, fill=color, outline='#323232') for i, color in enumerate(colors)]

        self.triangle = self.canvas.create_text(70, 32, text="▲", font=('Arial', 15))

        self.label = tk.Label(root, text="C", font=('Arial', 50))
        self.label.pack(padx=5, pady=0)

    def updateLabel(self, text):
        self.label.config(text=text)

    def updateProgressbar(self, maxFreq):
        closePitch, closeNote = findNote(maxFreq)
        ratio = maxFreq / closePitch
        if ratio >= 1.011:
            place = 130
        elif 1.005 < ratio < 1.011:
            place = 110
        elif 1.0015 < ratio <= 1.005:
            place = 90
        elif 0.995 <= ratio <= 1.0015:
            place = 70
        elif 0.989 < ratio < 0.995:
            place = 50
        elif 0.890 < ratio <= 0.989:
            place = 30
        else:
            place = 10

        self.canvas.coords(self.triangle, place, 32)

def audio_stream(gui):
    SAMPLE_FREQ = 44100
    WINDOW_SIZE = 44100
    WINDOW_STEP = 21050
    WINDOW_SAMPLES = [0 for _ in range(WINDOW_SIZE)]

    def callback(inData, frames, time, status):
        nonlocal WINDOW_SAMPLES
        if status:
            print(status)

        inputLevel = np.sqrt(np.mean(inData**2))
        levelThreshold = 0.05
        if (inputLevel > levelThreshold):
            if any(inData):
                # append new samples
                # ':' indicates select every row
                # '0' inidactes the element at index 0 from each row
                # '[:, 0]' in this case select the channel of audio data
                WINDOW_SAMPLES = np.concatenate((WINDOW_SAMPLES, inData[:, 0]))
                # remove old samples
                WINDOW_SAMPLES = WINDOW_SAMPLES[len(inData[:, 0]):]

                # magnitude spectrum obtained by FFT
                # to conver the time-domain signal into-frequency-domain data
                magnitudeSpec = abs(scipy.fftpack.fft(WINDOW_SAMPLES)[:len(WINDOW_SAMPLES) // 2])
                for i in range(int(62 / (SAMPLE_FREQ / WINDOW_SIZE))):
                    magnitudeSpec[i] = 0
                maxFreq = np.argmax(magnitudeSpec) * (SAMPLE_FREQ / WINDOW_SIZE)

                closePitch, closeNote = findNote(maxFreq)

                os.system('cls' if os.name == 'nt' else 'clear')
                print(f"Current Note: {closeNote} {maxFreq:.1f} / {closePitch:.1f}")
                gui.updateLabel(closeNote)
                gui.updateProgressbar(maxFreq)
            else:
                print('no input')

    try:
        with sd.InputStream(channels=1, callback=callback, 
                            blocksize=WINDOW_STEP, 
                            samplerate=SAMPLE_FREQ):
            while True:
                pass
    except Exception as e:
        print(str(e))

def main():
    root = tk.Tk()
    root.geometry("170x135")
    gui = TunerGUI(root)
    threading.Thread(target=audio_stream, args=(gui,), daemon=True).start()
    root.mainloop()

if __name__ == "__main__":
    main()

import datetime
import multiprocessing

import numpy as np
import sounddevice as sd

from oscillator import Oscillator
from utils import SAMPLE_RATE, NOTE_FREQUENCIES

class Synthesis():

    def __init__(self, lFrequencies = [NOTE_FREQUENCIES['C4']], duration=10):
        self.lFrequencies = lFrequencies
        self.lOscillators = [Oscillator(frequency) for frequency in self.lFrequencies]
        self.duration = duration
        self.t = np.linspace(0, self.duration, int(SAMPLE_RATE * self.duration), endpoint=False)
        self.signal = self.t * 0
        self.stop_thread = False

    def computeSignal(self):
        for oscillator in self.lOscillators:
            self.signal += oscillator.amplitude * np.sin(2 * np.pi * oscillator.frequency * self.t)
        #TODO : normaliser ?
    
    def playSignal(self):
        self.computeSignal()
        sd.play(self.signal, samplerate=SAMPLE_RATE)
        sd.wait()  # Wait for the audio to finish playing

    def updateSignal(self, lFrequencies):
        self.lOscillators = [Oscillator(frequency) for frequency in lFrequencies]
        self.proc.terminate()
        self.proc = multiprocessing.Process(target=test.playSignal, args=())
        self.proc.start()

        # self.lOscillators = [Oscillator(frequency) for frequency in lFrequencies]
        # self.tempProc = multiprocessing.Process(target=test.playSignal, args=())
        # self.tstart = datetime.datetime.now()
        # self.tempProc.start()
        # print("self.tempProc.start()")
        # print(datetime.datetime.now() - self.tstart)
        # self.proc.terminate()
        # self.proc = multiprocessing.Process(target=test.playSignal, args=())
        # self.proc.start()
        # print("self.proc.start()")
        # print(datetime.datetime.now() - self.tstart)
        # self.tempProc.terminate()

    def startPlaying(self):
        self.proc = multiprocessing.Process(target=self.playSignal, args=())
        self.proc.start()

if __name__ == "__main__":

    lOscillators = [
        NOTE_FREQUENCIES["C3"],
        NOTE_FREQUENCIES["E3"],
        NOTE_FREQUENCIES["G3"],
    ]
    test = Synthesis(lFrequencies=lOscillators, duration=10)
    test.startPlaying()
    # Start the user input thread
    
    lOscillators = [
        NOTE_FREQUENCIES["D3"],
        NOTE_FREQUENCIES["F3"],
        NOTE_FREQUENCIES["A3"],
    ]

    import time
    time.sleep(2)
    test.updateSignal(lOscillators)

    lOscillators = [
        NOTE_FREQUENCIES["F3"],
        NOTE_FREQUENCIES["A3"],
        NOTE_FREQUENCIES["C4"],
    ]
    time.sleep(2)
    test.updateSignal(lOscillators)

    lOscillators = [
        NOTE_FREQUENCIES["C3"],
        NOTE_FREQUENCIES["E3"],
        NOTE_FREQUENCIES["G3"],
    ]
    time.sleep(2)
    test.updateSignal(lOscillators)


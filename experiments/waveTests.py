import pygame
import numpy as np
import time
import matplotlib.pyplot as plt
import math

from utils import note_frequencies, sample_rate

class Wave:
    def __init__(self, bits, sample_rate, freq, function):
        self.bits = bits
        self.sample_rate = sample_rate
        self.freq = freq
        self.function = function

    def set_freq(self, freq):
        self.freq = freq

    def set_function(self, function):
        self.function = function

    def play(self, duration=1):
        num_samples = int(round(duration * self.sample_rate))
        sound = pygame.sndarray.make_sound(self._get_sound_buffer(num_samples))
        sound.play(loops=1, maxtime=int(duration * 1000))
        time.sleep(duration)

    def plot_wave(self, num_samples=100):
        plt.plot(self._get_sound_buffer(num_samples)[:, 0])

    def _get_sound_buffer(self, num_samples):
        sound_buffer = np.zeros((num_samples, 2), dtype=np.int16)
        amplitude = 2 ** (self.bits - 1) - 1

        for sample_num in range(num_samples):
            t = float(sample_num) / self.sample_rate
            y = self.function(amplitude, self.freq, t)
            sound_buffer[sample_num][1] = y
            sound_buffer[sample_num][0] = y

        return sound_buffer

if __name__ == "__main__":
    pygame.init()
    pygame.mixer.pre_init(sample_rate, 16)
    wave = Wave(16, sample_rate, note_frequencies["C4"], lambda A, f, t: int(round(A * math.sin(2 * math.pi * f * t))))
    wave.play(1)
    wave.set_freq(note_frequencies["E4"])
    wave.play(1)
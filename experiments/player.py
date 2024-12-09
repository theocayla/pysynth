import sounddevice as sd
import numpy as np
import threading

from utils import NOTE_FREQUENCIES, SAMPLE_RATE

class FrequencyPlayer:
    def __init__(self, initial_frequency=440.0, volume=1):
        self.frequency = initial_frequency
        self.volume = volume
        self.stop_thread = False

    def callback(self, outdata, frames, time, status):
        if self.stop_thread:
            return

        t = np.linspace(0, frames / SAMPLE_RATE, frames, endpoint=False)
        signal = self.volume * np.sin(2 * np.pi * self.frequency * t)
        signal = signal.astype(np.float32)
        outdata[:] = signal.reshape(-1, 1)


    def play_frequency(self):
        with sd.OutputStream(callback=self.callback, channels=1, blocksize=0, samplerate=SAMPLE_RATE):
            while not self.stop_thread:
                pass  # Keep the stream open

    def start_player(self):
        player_thread = threading.Thread(target=self.play_frequency)
        player_thread.start()

        while True:
            user_input = input("Enter new note (or 'exit' to stop): ")
            if user_input.lower() == 'exit':
                self.stop_thread = True
                break

            try:
                new_frequency = NOTE_FREQUENCIES.get(user_input, 440.)
                self.frequency = new_frequency
            except ValueError:
                print("Invalid input. Please enter a valid number.")

        player_thread.join()

if __name__ == "__main__":
    initial_frequency = 440.0
    volume = 0.5

    player = FrequencyPlayer(initial_frequency, volume)
    player.start_player()
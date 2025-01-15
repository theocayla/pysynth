import numpy as np
import sounddevice as sd
import threading

from synthesis import generate_envelope, generate_tone_with_envelope_continuous_phase
from utils import SAMPLE_RATE, NOTE_FREQUENCIES, notes2freqs

# Global constants
CHUNK_DURATION = 0.05  # Duration of each chunk in seconds
AMPLITUDE = 0.5  # Amplitude of the sine waves

# Mapping of keys to frequencies (in Hz)
key_to_frequency = {
    'q': NOTE_FREQUENCIES["C4"],
    's': NOTE_FREQUENCIES["D4"],
    'd': NOTE_FREQUENCIES["E4"],
    'f': NOTE_FREQUENCIES["F4"],
}

# Multithreading
note_thread = None
stop_event = threading.Event()

global last_phase
last_phase = 0


def note_runner(frequencies, duration, envelope):
    '''
    Executes play_chord_with_envelope with conditionnal stop
    '''
    global stop_event, last_phase
    stop_event.clear()
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    signal = t * 0
    for frequency in frequencies:
        tone, last_phase = generate_tone_with_envelope_continuous_phase(
            frequency, duration, envelope, SAMPLE_RATE, initial_phase=last_phase
        )
        signal += tone
    try:
        stream = sd.OutputStream(samplerate=SAMPLE_RATE, channels=1)
        with stream:
            for chunk in np.array_split(signal, 100):
                if stop_event.is_set():
                    break
                stream.write(chunk.astype(np.float32))
    except Exception as e:
        print(f"Error playing chord: {e}")


def main():
    global note_thread, stop_event

    while True:
        note = input("")
        try:
            frequency = [key_to_frequency[note]]
            print(frequency)
            duration = 10  # Durée en secondes

            _, envelope = generate_envelope(
                duration=duration,
                attack_time=0.5,
                decay_time=0.1,
                sustain_level=0.5,
                release_time=0.1
                )
            if note_thread and note_thread.is_alive():
                stop_event.set()
                note_thread.join()

            stop_event.clear()
            note_thread = threading.Thread(target=note_runner, args=(frequency, duration, envelope))
            note_thread.start()
        except ValueError:
            print("Invalid input.")

if __name__ == "__main__":
    main()

import threading

import numpy as np
import sounddevice as sd

from chord_maker import buildChord
from simple_synthesis import generate_envelope, generate_tone_with_envelope
from utils import SAMPLE_RATE, notes2freqs

# Multithreading
chord_thread = None
stop_event = threading.Event()

def chord_runner(frequencies, duration, envelope):
    '''
    Executes play_chord_with_envelope with conditionnal stop
    '''
    global stop_event
    stop_event.clear()
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    signal = t * 0
    for frequency in frequencies:
        signal += generate_tone_with_envelope(frequency, duration, envelope, SAMPLE_RATE)

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
    global chord_thread, stop_event

    while True:
        chordPrompt = input("Enter chord :")
        if chordPrompt.lower() == 'q':
            if chord_thread and chord_thread.is_alive():
                stop_event.set()
                chord_thread.join()
            break

        try:
            frequencies = notes2freqs(buildChord(chordPrompt))
            duration = 10  # Durée en secondes

            _, envelope = generate_envelope(
                duration=duration,
                attack_time=0.3,
                decay_time=0.1,
                sustain_level=1,
                release_time=1
                )
            if chord_thread and chord_thread.is_alive():
                stop_event.set()
                chord_thread.join()

            stop_event.clear()
            chord_thread = threading.Thread(target=chord_runner, args=(frequencies, duration, envelope))
            chord_thread.start()
        except ValueError:
            print("Invalid input. Please enter comma-separated numbers.")

if __name__ == "__main__":
    main()

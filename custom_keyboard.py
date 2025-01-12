import numpy as np
import sounddevice as sd
import threading
from simple_synthesis import generate_tone, generate_envelope
from utils import NOTE_FREQUENCIES, SAMPLE_RATE

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

# key_to_frequency = {
#     16: NOTE_FREQUENCIES["C4"],  # 'q' -> 16
#     31: NOTE_FREQUENCIES["D4"],  # 's' -> 31
#     32: NOTE_FREQUENCIES["E4"],  # 'd' -> 32
#     33: NOTE_FREQUENCIES["F4"],  # 'f' -> 33
# }

# Shared state
# We need to track the signal phase to make sure we sync each note and don't hear a click when switching
current_phase = 0  # Phase of the current note
current_frequency = 0  # Frequency of the current note
lock = threading.Lock()  # To safely update shared variables

# Event to stop playback
stop_event = threading.Event()

def generate_sine_wave(frequency, duration, sample_rate, initial_phase):
    """Generate a sine wave with a given frequency, duration, and initial phase."""
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    omega = 2 * np.pi * frequency
    signal = np.sin(omega * t + initial_phase)
    final_phase = (omega * duration + initial_phase) % (2 * np.pi)
    return AMPLITUDE * signal, final_phase


def audio_callback(outdata, frames, time, status):
    """Audio callback to generate and stream the sound in real-time."""
    global current_phase, current_frequency

    if stop_event.is_set():
        outdata.fill(0)
        return

    with lock:
        frequency = current_frequency
        phase = current_phase

    duration = frames / SAMPLE_RATE
    wave, phase = generate_tone(frequency, duration, envelope=None, sample_rate=SAMPLE_RATE, initial_phase=phase, waveform="sawtooth")

    with lock:
        current_phase = phase  # Update global phase to keep track of where we are

    outdata[:] = wave.reshape(-1, 1)


def start_audio_stream():
    """Start the audio stream."""
    global current_phase, current_frequency
    current_phase = 0  # Reset phase at the start
    current_frequency = 0  # No note initially
    stream = sd.OutputStream(
        samplerate=SAMPLE_RATE,
        channels=1,
        callback=audio_callback,
        blocksize=int(CHUNK_DURATION * SAMPLE_RATE),
    )
    stream.start()


def play_note(note):
    """Start playing a note."""
    global current_frequency
    with lock:
        current_frequency = key_to_frequency[note]


def stop_note():
    """Stop playing the current note."""
    global current_frequency
    with lock:
        current_frequency = 0


def main():
    print("Press keys to play notes. Press ESC to quit.")
    start_audio_stream()  # Start audio playback

    # TODO : find a way to use the keyboard lib or pynput, now we need to press enter for eahc note
    while True:
        try:
            note = input("Enter note key (q/s/d/f): ").strip()
            if note == "ESC":
                stop_event.set()
                break
            elif note in key_to_frequency:
                play_note(note)
            else:
                print("Invalid key.")
        except KeyboardInterrupt:
            stop_event.set()
            break

if __name__ == "__main__":
    main()

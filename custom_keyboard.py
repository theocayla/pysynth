import numpy as np
import sounddevice as sd
import threading

from pynput import keyboard
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

# Set to track currently active keys
active_keys = set()
lock = threading.Lock()  # To safely access shared state

def generate_sine_wave(frequencies, duration, sample_rate, phase):
    """Generate a combined sine wave for the given frequencies."""
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = np.zeros_like(t)
    new_phases = []
    for freq, ph in zip(frequencies, phase):
        omega = 2 * np.pi * freq
        wave += np.sin(omega * t + ph)
        new_phases.append((omega * duration + ph) % (2 * np.pi))
    return AMPLITUDE * wave / len(frequencies), new_phases


def audio_callback(outdata, frames, time, status):
    """Audio callback function to generate audio chunks in real-time."""
    global current_phases
    with lock:
        frequencies = [key_to_frequency[key] for key in active_keys]
    if frequencies:
        wave, current_phases = generate_sine_wave(
            frequencies, CHUNK_DURATION, SAMPLE_RATE, current_phases
        )
    else:
        wave = np.zeros(frames)
    outdata[:len(wave)] = wave.reshape(-1, 1)


def start_audio_stream():
    """Start the audio stream."""
    global current_phases
    current_phases = [0] * len(key_to_frequency)  # Initial phases for each frequency
    stream = sd.OutputStream(
        samplerate=SAMPLE_RATE,
        channels=1,
        callback=audio_callback,
        # blocksize=int(CHUNK_DURATION * SAMPLE_RATE),
        blocksize=int(1024),
    )
    stream.start()


def on_press(key):
    """Handle key press events."""
    try:
        if key.char in key_to_frequency:
            with lock:
                active_keys.add(key.char)
    except AttributeError:
        pass


def on_release(key):
    """Handle key release events."""
    try:
        if key.char in key_to_frequency:
            with lock:
                active_keys.discard(key.char)
    except AttributeError:
        pass


# Main
if __name__ == "__main__":
    print("Press keys to play notes. Press ESC to quit.")

    start_audio_stream()  # Start audio playback thread

    # Listen for keyboard input
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
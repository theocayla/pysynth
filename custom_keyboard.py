import keyboard
import numpy as np
import sounddevice as sd
import threading

from simple_synthesis import play_note

# Mapping of keys to frequencies (in Hz)
key_to_frequency = {
    'q': "C4",
    's': "D4",
    'd': "E4",
    'f': "F4",
}

# Set to track currently active keys
active_keys = set()

# Sample rate for audio playback
SAMPLE_RATE = 44100

def handle_key_press(event):
    """Handle key press events to start playing a note."""
    key = event.name
    if key in key_to_frequency and key not in active_keys:
        active_keys.add(key)
        threading.Thread(target=play_note, args=(frequency, duration, envelope), daemon=True).start()

def handle_key_release(event):
    """Handle key release events to stop playing a note."""
    key = event.name
    if key in active_keys:
        active_keys.remove(key)

# Main program setup
print("Press keys to play notes. Press ESC to quit.")


# Set up event listeners for key press and release
keyboard.on_press(handle_key_press)
keyboard.on_release(handle_key_release)

# Keep the script running until ESC is pressed
keyboard.wait('esc')

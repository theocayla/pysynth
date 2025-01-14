import numpy as np
import sounddevice as sd
import threading
from synthesis import generate_tone, generate_envelope
from utils import NOTE_FREQUENCIES, SAMPLE_RATE

# Global constants
CHUNK_DURATION = 0.05  # Duration of each chunk in seconds
AMPLITUDE = 0.5  # Amplitude of the sine waves
DURATION = 0.8 # Total duration for a note
# Envelope parameters
ATTACK = 0.1 # in seconds
DECAY = 0.5 # in seconds

# Mapping of the keyboard to frequencies (in Hz)
key_to_frequency = {
    'q': NOTE_FREQUENCIES["C4"],
    's': NOTE_FREQUENCIES["D4"],
    'd': NOTE_FREQUENCIES["E4"],
    'f': NOTE_FREQUENCIES["F4"],
}

# Shared state
# We need to track the signal phase to make sure we sync each note and don't hear a click when switching
current_phase = 0  # Phase of the current note
current_frequency = 0  # Frequency of the current note

# Envelop is generated once for the whole note, then each chunk is applied during audio_callback
current_envelope = None  # Envelope of the current note
current_envelope_position = 0  # Position in the envelope

lock = threading.Lock()  # To safely update shared variables
stop_event = threading.Event() # Event to stop playback

def audio_callback(outdata, frames, time, status):
    """Audio callback to generate and stream the sound in real-time."""
    global current_phase, current_frequency, current_envelope, current_envelope_position

    if stop_event.is_set():
        outdata.fill(0)
        return

    with lock:
        frequency = current_frequency
        phase = current_phase
        envelope = current_envelope
        envelope_position = current_envelope_position

    duration = frames / SAMPLE_RATE
    if frequency > 0:
        wave, phase = generate_tone(
            frequency,
            duration,
            sample_rate=SAMPLE_RATE,
            initial_phase=phase,
            waveform="sinus"
        )

        # Apply the corresponding portion of the envelope
        if envelope is not None:
            start_idx = envelope_position
            end_idx = start_idx + frames
            chunk_envelope = envelope[start_idx:end_idx]
            wave[:len(chunk_envelope)] *= chunk_envelope
            envelope_position += frames

            # If we've reached the end of the envelope, stop the note
            if envelope_position >= len(envelope):
                wave[len(chunk_envelope):] = 0
                frequency = 0  # Stop the note

    else:
        wave = np.zeros(frames)

    with lock:
        current_phase = phase  # Update global phase to keep track of where we are
        current_frequency = frequency
        current_envelope_position = envelope_position

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
    global current_frequency, current_envelope, current_envelope_position

    with lock:
        current_frequency = key_to_frequency[note]
        current_envelope = generate_envelope(DURATION, ATTACK, DECAY, sample_rate=SAMPLE_RATE)
        current_envelope_position = 0



def stop_note():
    """Stop playing the current note."""
    global current_frequency, current_envelope, current_envelope_position
    with lock:
        current_frequency = 0
        current_envelope = None
        current_envelope_position = 0

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

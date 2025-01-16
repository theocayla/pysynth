import numpy as np
import sounddevice as sd
import threading
import json
from datetime import datetime 

import matplotlib.pyplot as plt

from synthesis import generate_tone, generate_envelope
from utils import KEY2FREQ, SAMPLE_RATE
import parameters as p
# If True, we dump data into a csv file for further observation
DEBUG = True

# Shared state
# We need to track the signal phase to make sure we sync each note and don't hear a click when switching
current_phase = 0  # Phase of the current note
current_frequency = 0  # Frequency of the current note

# Envelop is generated once for the whole note, then each chunk is applied during audio_callback
current_envelope = None  # Envelope of the current note
current_envelope_position = 0  # Position in the envelope

lock = threading.Lock()  # To safely update shared variables
stop_event = threading.Event() # Event to stop playback

# For debugging
waveform_data = []  # Stores the waveform if DEBUG_MODE is active

def audio_callback(outdata, frames, time, status):
    """Audio callback to generate and stream the sound in real-time."""
    global current_phase, current_frequency, current_envelope, current_envelope_position, waveform_data

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
            waveform=p.WAVEFORM,
            harmonics=p.HARMONICS
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

            # Save waveform data for debugging
        if DEBUG:
            waveform_data.extend(wave)

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
        blocksize=int(p.CHUNK_DURATION * SAMPLE_RATE),
    )
    stream.start()


def play_note(note):
    """Start playing a note."""
    global current_frequency, current_envelope, current_envelope_position

    with lock:
        current_frequency = KEY2FREQ[note]
        current_envelope = generate_envelope(p.DURATION, p.ATTACK, p.DECAY, sample_rate=SAMPLE_RATE)
        current_envelope_position = 0

def stop_note():
    """Stop playing the current note."""
    global current_frequency, current_envelope, current_envelope_position
    with lock:
        current_frequency = 0
        current_envelope = None
        current_envelope_position = 0

def downsample_waveform(data, downsample_factor):
    """Downsample waveform by the given factor."""
    return data[::downsample_factor]  # Downsample the waveform by factor


def plot_waveform(data, downsample_factor):
    """Plot the waveform with zooming capability."""
    plt.plot(data)
    plt.savefig("test.png")
    plt.show()

def main():
    print("Press a key")
    start_audio_stream()  # Start audio playback
    if DEBUG:
        key_sequence = []
        timestamps = []
        tStart = datetime.now()
    # TODO : find a way to use the keyboard lib or pynput, now we need to press enter for eahc note
    while True:
        try:
            note = input("Enter note key (q/s/d/f): ").strip()
            if note == "x":
                stop_event.set()
                break
            elif note == "save":

                formatted_waveform = {
                    "data" : waveform_data,
                    "key_sequence" : key_sequence,
                    "timestamps" : timestamps
                }
                # TODO : investigate why this provoques a segfault
                # plot_waveform(np.array(waveform_data, dtype=np.float32), 1)    
                
                with open("data/waveform.json", 'w') as fp:
                    json.dump(formatted_waveform, fp)
                stop_event.set()
                break
            elif note in KEY2FREQ:
                play_note(note)
                if DEBUG:
                    key_sequence.append(KEY2FREQ[note])
                    timestamps.append(int((datetime.now() - tStart).total_seconds() * SAMPLE_RATE))
            else:
                print("Invalid key.")
        except KeyboardInterrupt:
            stop_event.set()
            break

if __name__ == "__main__":
    main()

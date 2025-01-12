import random

import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd

from utils import NOTE_FREQUENCIES, SAMPLE_RATE

def play_frequency(frequency, duration=5, volume=0.5):
    # Generate a sine wave of the specified frequency
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    signal = volume * np.sin(2 * np.pi * frequency * t)

    # Play the generated signal
    sd.play(signal, samplerate=SAMPLE_RATE)
    sd.wait()  # Wait for the audio to finish playing

def playSequence(frequencies, duration):
    for frequency in frequencies:
        print(frequency)
        play_frequency(frequency, duration)

def polyphony(frequencies, duration=5, volume=0.5):        
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    signal = t * 0
    for frequency in frequencies:
        signal += volume * np.sin(2 * np.pi * frequency * t)

    # Play the generated signal
    sd.play(signal, samplerate=SAMPLE_RATE)
    sd.wait()  # Wait for the audio to finish playing

def generate_envelope(duration, attack_time=0.1, decay_time=0.1, sustain_level=0.8, release_time=0.1, SAMPLE_RATE=44100):
    total_samples = int(duration * SAMPLE_RATE)
    t = np.linspace(0, duration, total_samples, endpoint=False)

    # Attack phase
    attack_samples = int(attack_time * SAMPLE_RATE * duration)
    attack_env = np.linspace(0, 1, attack_samples)

    # Decay phase
    decay_samples = int(decay_time * SAMPLE_RATE* duration)
    decay_env = np.linspace(1, sustain_level, decay_samples)

    # Sustain phase
    sustain_samples = total_samples - attack_samples - decay_samples
    sustain_env = np.ones(sustain_samples) * sustain_level

    # Release phase
    release_samples = int(release_time * SAMPLE_RATE)
    release_env = np.linspace(sustain_level, 0, release_samples)

    envelope = np.concatenate((attack_env, decay_env, sustain_env, release_env[:total_samples-len(attack_env)-len(decay_env)-len(sustain_env)]))
    envelope = np.clip(envelope, 0, 1)  # Ensure envelope values are between 0 and 1

    return t, envelope

def generate_tone_with_envelope(frequency, duration, envelope, SAMPLE_RATE=44100):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    signal = envelope * np.sin(2 * np.pi * frequency * t)
    return signal

def generate_tone(frequency, duration, envelope=None, sample_rate=SAMPLE_RATE, initial_phase=0, waveform="sinus"):
    '''
    Generates tone, applies envelope if it exists, and tracks phase for sound continuity puropses.
    Three waveforms are available : sinus, sawtooth or square
    '''
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    omega = 2 * np.pi * frequency

    # Define waveform 
    if waveform == 'sinus':
        signal = np.sin(omega * t + initial_phase)
    elif waveform == 'sawtooth':
        signal = 2 * (t * frequency - np.floor(0.5 + t * frequency))
    elif waveform == 'square':
        signal = np.sign(np.sin(omega * t + initial_phase))
    else:
        raise ValueError("Unsupported wave type. Choose among 'sinus', 'sawtooth', or 'square'.")

    # Applies envelop
    if envelope is not None:
        signal *= envelope
    final_phase = (omega * duration + initial_phase) % (2 * np.pi)
    return signal, final_phase

def play_tone_with_envelope(frequency, duration, envelope):
    signal = generate_tone_with_envelope(frequency, duration, envelope, SAMPLE_RATE)
    sd.play(signal, samplerate=SAMPLE_RATE)
    sd.wait()

def play_chord_with_envelope(frequencies, duration, envelope):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    signal = signal = t * 0
    for frequency in frequencies:
        signal += generate_tone_with_envelope(frequency, duration, envelope, SAMPLE_RATE)
    sd.play(signal, samplerate=SAMPLE_RATE)
    sd.wait()

def apply_chorus_effect(signal, SAMPLE_RATE=44100, depth=0.02, rate=1.5):
    # Generate a modulation signal for pitch variation
    t = np.arange(len(signal)) / SAMPLE_RATE
    modulation_signal = depth * np.sin(2 * np.pi * rate * t)

    # Apply chorus effect by varying pitch
    modulated_signal = np.interp(t + modulation_signal, t, signal)

    return modulated_signal

def play_chorus_effect(frequencies, duration, depth=0.02, rate=1.5):
    SAMPLE_RATE = 44100
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    signal = t * 0
    for frequency in frequencies:
        signal += np.sin(2 * np.pi * frequency * t)

    # Apply chorus effect
    modulated_signal = apply_chorus_effect(signal, SAMPLE_RATE, depth, rate)

    # Play the original and modulated signals
    # sd.play(signal, samplerate=SAMPLE_RATE, blocking=True)
    sd.play(modulated_signal, samplerate=SAMPLE_RATE, blocking=True)


# Set to keep track of currently pressed keys
pressed_keys = set()

if __name__ == "__main__":

    frequencyRange = [100, 1000]

    sequenceLength = 30
    sequence = [NOTE_FREQUENCIES[random.choice(list(NOTE_FREQUENCIES.keys()))]for _ in range(sequenceLength)]
    # playSequence(sequence, duration=0.2)

    chord1 = [
        NOTE_FREQUENCIES["C4"],
        NOTE_FREQUENCIES["E4"],
        NOTE_FREQUENCIES["G4"],
        NOTE_FREQUENCIES["B4"],
        NOTE_FREQUENCIES["D5"],
    ]
    chord2 = [
        NOTE_FREQUENCIES["D4"],
        NOTE_FREQUENCIES["F4"],
        NOTE_FREQUENCIES["A4"],
        NOTE_FREQUENCIES["C5"],
        NOTE_FREQUENCIES["E5"],
    ]
    # polyphony(chord1, duration=5, volume=0.5)


    # Example usage:
    duration = 4.0
    frequency = 440.0  # Hz

    # Generate envelope
    t, envelope = generate_envelope(
        duration=duration,
        attack_time=1,
        decay_time=0.5
        )

    # # Plot the envelope
    plt.plot(t, envelope)
    plt.title("Amplitude Envelope")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Amplitude")
    plt.show()

    # Play tone with the generated envelope
    # play_tone_with_envelope(frequency, duration, envelope)
    # play_chord_with_envelope(chord1, duration, envelope)
    # play_chord_with_envelope(chord2, duration, envelope)
    # play_chorus_effect([frequency], duration, depth=0.002, rate=4)

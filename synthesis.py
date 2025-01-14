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

import numpy as np

def generate_envelope(duration, attack, decay, sample_rate=44100):
    """
    Generate a simple envelop    
    Parameters:
    - duration (float): duration of the signal
    - attack (float): duration of the attack -> increase of the amplitude
    - decay (float): duration of the decay -> decrease of the amplitude
    - sample_rate (int): Fréquence d'échantillonnage (en Hz).
    
    Returns:
    - envelope (numpy.ndarray)
    """
    if attack + decay > duration:
        raise ValueError("La somme de l'attaque et du decay ne doit pas dépasser la durée totale.")
    
    # Temps total
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    
    # Phase d'attaque : montée linéaire de 0 à 1
    attack_samples = int(attack * sample_rate)
    attack_envelope = np.linspace(0, 1, attack_samples)
    
    # Phase de décroissance : descente linéaire de 1 à 0
    decay_samples = int(decay * sample_rate)
    decay_envelope = np.linspace(1, 0, decay_samples)
    
    # Phase de maintien (sustain) : constante à 0 (si reste du temps)
    sustain_samples = len(t) - attack_samples - decay_samples
    if sustain_samples > 0:
        sustain_envelope = np.ones(sustain_samples)
    else:
        sustain_envelope = np.array([])
    
    # Construction de l'enveloppe complète
    envelope = np.concatenate((attack_envelope, sustain_envelope, decay_envelope))
    
    # Assurer que l'enveloppe correspond exactement à la durée
    envelope = np.pad(envelope, (0, len(t) - len(envelope)), mode='constant', constant_values=0)
    
    return envelope


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
    attack = 0.4    # 0.5 seconde
    decay = 2.5     # 1 seconde
    # Generate envelope
    envelope = generate_envelope(duration, attack, decay, SAMPLE_RATE)

    # Visualiser l'enveloppe
    time = np.linspace(0, duration, len(envelope))
    plt.plot(time, envelope)
    plt.title("Enveloppe sonore")
    plt.xlabel("Temps (s)")
    plt.ylabel("Amplitude")
    plt.grid()
    plt.show()

    # Play tone with the generated envelope
    # play_tone_with_envelope(frequency, duration, envelope)
    # play_chord_with_envelope(chord1, duration, envelope)
    # play_chord_with_envelope(chord2, duration, envelope)
    # play_chorus_effect([frequency], duration, depth=0.002, rate=4)

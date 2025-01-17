from typing import Optional, List

import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd

from utils import SAMPLE_RATE

def generate_envelope(
        duration : float,
        attack : float,
        decay : float,
        sample_rate=44100
) -> List[float]:
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

def generate_tone(
    frequency: float,  # Fundamental frequency in Hz
    duration: float,  # Sound duration in seconds
    envelope: Optional[List[float]] = None,  # Envelope array
    sample_rate: int = 44100,
    initial_phase: float = 0.0,  # Initial phase in rad
    waveform: str = "sinus",  # Wave type ("sinus", "square", "triangle")
    harmonics: List[float] = [1.0]  # Harmonics coefficients
) -> List[float]:
    '''
    Generates tone, applies envelope if it exists, and tracks phase for sound continuity puropses.
    Three waveforms are available : sinus, sawtooth or square
    TODO : adapt function to take a list of frequency as input
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

    # Adding harmonics
    # TODO : this needs debugging, continuity issues
    for i, coeff in enumerate(harmonics[1:], start=2):  # Commence à la 2e harmonique
        signal += coeff * np.sin(omega * t * i + initial_phase)
    
    # Computing final phase (useless for real time usage)
    final_phase = (omega * duration + initial_phase) % (2 * np.pi)

    # Normalization
    # signal = signal / np.max(np.abs(signal))

    return signal, final_phase

def generate_tone_with_envelope(frequency, duration, envelope, SAMPLE_RATE=44100):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    signal = envelope * np.sin(2 * np.pi * frequency * t)
    return signal

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

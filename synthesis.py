from typing import Optional, List

import numpy as np

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
    initial_phases: Optional[List[float]] = None, # Initial phase of each harmonic
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

    # Initialize signal and final phases
    signal = np.zeros_like(t)
    final_phases = []

    if initial_phases is None:
        initial_phases = [0.0] * len(harmonics)

    # Define waveform 
    if waveform == 'sinus':
        pass
    elif waveform == 'sawtooth':
        signal += 2 * (t * frequency - np.floor(0.5 + t * frequency))
    elif waveform == 'square':
        signal += np.sign(np.sin(omega * t))
    else:
        raise ValueError("Unsupported wave type. Choose among 'sinus', 'sawtooth', or 'square'.")

    # Adding harmonics
    # TODO : a slight click is hearable when changing notes, phase need to be properly set
    if waveform == 'sinus':
        # Generate fundamental and harmonics
        for i, (coeff, harmonic_phase) in enumerate(zip(harmonics, initial_phases), start=1):
            # Each harmonic needs to be initialized with its own initial phase
            harmonic_omega = omega * i  # Frequency for harmonic
            harmonic_signal = coeff * np.sin(harmonic_omega * t + harmonic_phase)
            signal += harmonic_signal
            # We compute the final phase for each harmonic to initialize the next chunk
            harmonic_final_phase = (harmonic_omega * duration + harmonic_phase) % (2 * np.pi)
            final_phases.append(harmonic_final_phase)

    if envelope is not None:
        # TODO : need to select the right slice of the enveloppe to be applied for a given chunk
        signal *= envelope

    # Normalization
    signal = signal / np.max(np.abs(signal))

    return signal, final_phases

def generate_tone_with_envelope(
    frequency: float,
    duration: float,
    envelope: np.ndarray,
    SAMPLE_RATE: int = 44100
) -> np.ndarray:
    """
    Generate a sinusoidal tone modulated by an envelope.

    Args:
        frequency (float): Frequency of the tone in Hz.
        duration (float): Duration of the tone in seconds.
        envelope (np.ndarray): Envelope array to shape the amplitude of the tone.
        SAMPLE_RATE (int, optional): Sampling rate in Hz. Defaults to 44100.

    Returns:
        np.ndarray: The generated audio signal as a NumPy array.
    """
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    signal = envelope * np.sin(2 * np.pi * frequency * t)
    return signal


def apply_chorus_effect(
    signal: np.ndarray,
    SAMPLE_RATE: int = 44100,
    depth: float = 0.02,
    rate: float = 1.5
) -> np.ndarray:
    """
    Apply a chorus effect to an audio signal by introducing pitch modulation.

    Args:
        signal (np.ndarray): Input audio signal as a NumPy array.
        SAMPLE_RATE (int, optional): Sampling rate in Hz. Defaults to 44100.
        depth (float, optional): Depth of the modulation in seconds. Defaults to 0.02.
        rate (float, optional): Rate of modulation in Hz. Defaults to 1.5.

    Returns:
        np.ndarray: The audio signal with the chorus effect applied.
    """
    t = np.arange(len(signal)) / SAMPLE_RATE
    modulation_signal = depth * np.sin(2 * np.pi * rate * t)

    # Apply chorus effect by interpolating the modulated signal
    modulated_signal = np.interp(t + modulation_signal, t, signal)
    return modulated_signal
import argparse
import json
import logging
import os

from typing import Optional, List, Union

import matplotlib.pyplot as plt
import numpy as np

from utils import SAMPLE_RATE

def plot_waveform(
    data: Union[str, np.ndarray], 
    save: bool = False, 
    slice: Optional[List[int]] = None
) -> None:
    """
    Plots an audio signal.

    Args:
        data (str | np.ndarray): The input data. It can be either the path to a JSON file containing the signal
            or a NumPy array representing the signal directly.
        save (bool, optional): If True, saves the plot as an image file. Defaults to False.
        slice (List[int], optional): Defines a range of the signal to plot as [start, end]. If None, plots the entire signal.
            Defaults to None.
    """
    # Load data if it's a file path
    if isinstance(data, str):
        if os.path.isfile(data): 
            with open(data, 'r') as file:
                signal = np.array(json.load(file).get("data", []))
        else:
            raise FileNotFoundError(f"No file found at path: {data}")
    elif isinstance(data, np.ndarray):
        signal = data
    else:
        raise TypeError("The 'data' argument must be a string (file path) or a NumPy array.")
    
    if slice is not None:
        print(type(signal))
        print(signal.shape[0])
        if not (isinstance(slice, list) and len(slice) == 2 and (slice[0] < 0 or slice[1] > len(signal))):
            raise ValueError(f"Error ploting the signal : slice should be a list of two integer indices within signal boundaries (slice = {slice}).")
    plt.plot(signal)
    if save:
        plt.savefig("waveform.png")
    plt.show()

def plot_spectrum(
        data: Union[str, np.ndarray],
        save: bool = False
) -> None:
    """
    Loads an audio signal and plots its spectrum.

    Args:
        data (str | np.ndarray): The input data. It can be either the path to a JSON file containing the signal
            or a NumPy array representing the signal directly.
        save (bool, optional): If True, saves the plot as an image file. Defaults to False.
    """
    # Load the audio signal
    if isinstance(data, str):
        if os.path.isfile(data):
            with open(data, 'r') as file:
                try:
                    signal = np.array(json.load(file)["data"])
                except (KeyError, ValueError, TypeError) as e:
                    logging.error(f"Failed to load data from {data}: {e}")
                    return
        else:
            raise FileNotFoundError(f"No file found at path: {data}")
    elif isinstance(data, np.ndarray):
        signal = data
    else:
        raise TypeError("The 'data' argument must be a string (file path) or a NumPy array.")

    # Compute FFT and frequencies
    fft_values = np.fft.fft(signal)
    frequencies = np.fft.fftfreq(len(signal), d=1 / SAMPLE_RATE)
    positive_freq = frequencies[:len(signal) // 2]
    spectrum = np.abs(fft_values)[:len(signal) // 2]

    # Plot the spectrum
    plt.figure(figsize=(10, 6))
    plt.plot(positive_freq, spectrum)
    plt.title("Audio Signal Power Spectrum")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Amplitude")
    plt.grid()

    # Save or show the plot
    if save:
        plt.savefig("spectrum.png")
    else:
        plt.show()

default_path = "data/waveform.json"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path",
        nargs="?",
        default=default_path,
        help="Specify the path of the json fil containing the audio sample"
    )
    args = parser.parse_args()
    plot_waveform(args.path)
    plot_spectrum(args.path)
import json
import matplotlib.pyplot as plt
import numpy as np
import argparse

from utils import SAMPLE_RATE

def plot_waveform(filepath):
    with open(filepath, 'r') as fp:
        x = json.load(fp)["data"]
    plt.plot(x)
    plt.savefig("test.png")
    plt.show()

def plot_spectrum(filepath):
    '''
    Loads the audio signal and plot its spectrum
    '''
    with open(filepath, 'r') as fp:
        x = json.load(fp)["data"]
    fft_values = np.fft.fft(x)
    frequencies = np.ft.fftfreq(len(x), d=1/SAMPLE_RATE)
    positive_freq = frequencies[:len(x)//2]
    spectrum = np.abs(fft_values)[:len(x)//2]

    plt.figure(figsize=(10,6))
    plt.plot(positive_freq, spectrum)
    plt.title("Audio signal power spectrum")
    plt.xlabel("Freq")
    plt.ylabel("Amplitude")
    plt.grid()
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
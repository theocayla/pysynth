import argparse
import json
import logging
import os

import matplotlib.pyplot as plt
import numpy as np

from utils import SAMPLE_RATE

def plot_waveform(data, save=False):
    if isinstance(data, str):
        if os.path.isfile(data):
            with open(data, 'r') as fp:
                x = json.load(fp)["data"]
        else:
            logging.info(f"No debug file found : {data}")
    else:
        x = data
    plt.plot(x)
    if save:
        plt.savefig("waveform.png")
    plt.show()

def plot_spectrum(data, save=False):
    '''
    Loads the audio signal and plot its spectrum
    '''
    if isinstance(data, str):
        if os.path.isfile(data):
            with open(data, 'r') as fp:
                x = json.load(fp)["data"]
        else:
            logging.info(f"No debug file found : {data}")
    else:
        x = data
    fft_values = np.fft.fft(x)
    frequencies = np.fft.fftfreq(len(x), d=1/SAMPLE_RATE)
    positive_freq = frequencies[:len(x)//2]
    spectrum = np.abs(fft_values)[:len(x)//2]

    plt.figure(figsize=(10,6))
    plt.plot(positive_freq, spectrum)
    plt.title("Audio signal power spectrum")
    plt.xlabel("Freq")
    plt.ylabel("Amplitude")
    plt.grid()
    if save:
        plt.savefig("spectrum.png")
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
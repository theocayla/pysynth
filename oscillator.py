import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QSlider, QCheckBox, QLabel, QPushButton

import utils

class Oscillator():

    MIN_FREQUENCY = 16
    MAX_FREQUENCY = 7100

    def __init__(self, frequency, amplitude=1, label="", isActivated=True):
        self.frequency = frequency
        self.amplitude = amplitude
        self.label = label
        self.isActivated = isActivated

        # UI
        self.slider_label = QLabel(self.label)
        self.slider = QSlider()
        self.slider.setOrientation(1)
        initialNote = utils.getClosestNote(self.frequency)
        initial_value = self.frequencyToSliderValue(self.frequency)
        self.slider.setValue(initial_value)  # Initial value
        self.frequency = self.sliderValueToFrequency(self.slider.value())
        self.slider_frequency_value_label = QLabel(f"Frequency: {int(self.frequency)} Hz")
        self.slider_note_value_label = QLabel(f'Note: {initialNote}')

        self.activationButton = QCheckBox('Activate')
        self.discreteFrequecyButton = QCheckBox('Adjust frequency to closest note')
        self.noteIncreaseButton = QPushButton('+')
        self.noteDecreaseButton = QPushButton('-')
        self.octaveIncreaseButton = QPushButton('+')
        self.octaveDecreaseButton = QPushButton('-')

        # Connect signals
        self.slider.valueChanged.connect(self.slider_changed)
        self.activationButton.clicked.connect(self.activate)         
        self.octaveIncreaseButton.clicked.connect(lambda: self.octaveChange(1))
        self.octaveDecreaseButton.clicked.connect(lambda : self.octaveChange(-1))
        self.noteIncreaseButton.clicked.connect(lambda: self.noteChange(1))
        self.noteDecreaseButton.clicked.connect(lambda: self.noteChange(-1))

    def activate(self):
        if self.isActivated:
            print("Deactivating")
            self.isActivated = False
        else:
            print("Activating")
            self.isActivated = True

    def slider_changed(self):
        self.frequency = self.sliderValueToFrequency(self.slider.value())
        self.slider_frequency_value_label.setText(f"Frequency: {int(self.frequency)} Hz")
        self.slider_note_value_label.setText(f"Note: {utils.getClosestNote(self.frequency)}")

    def octaveChange(self, delta):
        # Change slider position with new octave
        # frequency = self.sliderValueToFrequency(self.slider.value())
        # if delta > 0:
        #     newFrequency = frequency*2 if frequency*2 <= self.MAX_FREQUENCY else frequency
        # else:
        #     newFrequency = frequency/2 if frequency/2 >= self.MIN_FREQUENCY else frequency
        if delta > 0:
            newFrequency = self.frequency*2 if self.frequency*2 <= self.MAX_FREQUENCY else self.frequency
        else:
            newFrequency = self.frequency/2 if self.frequency/2 >= self.MIN_FREQUENCY else self.frequency

        newSliderValue = self.frequencyToSliderValue(newFrequency)
        step = newSliderValue - self.slider.value() 
        self.adjust_slider_value(step)

    def noteChange(self, delta):
        note = utils.getNoteFromFrequency(utils.getClosestNote(self.frequency))
        # if delta > 0:
        #     aboveNote = 

    def adjust_slider_value(self, step):
        self.slider.setValue(self.slider.value() + step)
        self.slider_changed()

    def sliderValueToFrequency(self, value):
        '''
        From 0 to 100 to min, max of frequencies
        Logarithmic scale
        '''
        # Ensure the input value is within the [0, 100] range
        normalized_value = max(0, min(100, value))

        # Map to the logarithmic scale
        mapped_value = 10 ** (np.log10(self.MIN_FREQUENCY) + normalized_value * (np.log10(self.MAX_FREQUENCY) - np.log10(self.MIN_FREQUENCY)) / 100)

        return mapped_value

    def frequencyToSliderValue(self, frequency):

        # Calculate the inverse mapping
        inverse_mapped_value = ((np.log10(frequency) - np.log10(self.MIN_FREQUENCY)) / (np.log10(self.MAX_FREQUENCY) - np.log10(self.MIN_FREQUENCY))) * 100

        return inverse_mapped_value

 
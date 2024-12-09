import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QSlider, QCheckBox, QLabel, QPushButton

import utils
from oscillator import Oscillator

class UserInterface(QWidget):
    def __init__(self, lOscillators):
        super().__init__()

        self.init_ui(lOscillators)

    def init_ui(self, lOscillators):

        # Layout
        layout = QVBoxLayout()
        for oscillator in lOscillators:
        
            layout.addWidget(oscillator.slider_label)
            layout.addWidget(oscillator.slider)
            layout.addWidget(oscillator.slider_frequency_value_label)
            layout.addWidget(oscillator.slider_note_value_label)
            layout.addWidget(oscillator.activationButton)
            layout.addWidget(oscillator.discreteFrequecyButton)
            layout.addWidget(QLabel("Note change"))
            layout.addWidget(oscillator.noteIncreaseButton)
            layout.addWidget(oscillator.noteDecreaseButton)
            layout.addWidget(QLabel("Octave change"))
            layout.addWidget(oscillator.octaveIncreaseButton)
            layout.addWidget(oscillator.octaveDecreaseButton)

        self.setLayout(layout)
        self.setWindowTitle('Slider and Button Interface')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    lOscillators = [
        Oscillator(utils.NOTE_FREQUENCIES["C3"], label="Oscillator1"),
        Oscillator(utils.NOTE_FREQUENCIES["E3"], label="Oscillator1"),
        Oscillator(utils.NOTE_FREQUENCIES["G3"], label="Oscillator1"),
    ]
    ex = UserInterface(lOscillators=lOscillators)
    sys.exit(app.exec_())

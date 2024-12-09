import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QSlider, QCheckBox, QLabel, QPushButton

import utils
from oscillator import Oscillator

class UserInterface(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.slider1_label = QLabel('Oscillator 1:')
        self.slider1 = QSlider()
        self.slider1.setOrientation(1)  # 1 represents horizontal orientation
        initialFrequency1 = 440
        initialNote1 = utils.getClosestNote(initialFrequency1)
        initial_value1 = utils.frequencyToSliderValue(initialFrequency1)
        self.slider1.setValue(initial_value1)  # Initial value
        self.frequency1 = utils.sliderValueToFrequency(self.slider1.value())
        self.slider1_frequency_value_label = QLabel(f"Frequency: {int(self.frequency1)} Hz")
        self.slider1_note_value_label = QLabel(f'Note: {initialNote1}')

        self.activationButton1 = QCheckBox('Activate')
        self.discreteFrequecyButton1 = QCheckBox('Adjust frequency to closest note')
        self.octaveDecreaseButton1 = QPushButton('+')
        self.octaveIncreaseButton1 = QPushButton('-')

        # Slider 2
        self.slider2_label = QLabel('Oscillator 2:')
        self.slider2 = QSlider()
        self.slider2.setOrientation(1)  # 1 represents horizontal orientation
        self.slider2.setValue(50)  # Initial value
        self.frequency2 = utils.sliderValueToFrequency(self.slider2.value())
        self.slider2_frequency_value_label = QLabel(f"Frequency: {int(self.frequency2)} Hz")
        self.slider2_note_value_label = QLabel(f'Note: {utils.getClosestNote(self.frequency2)}')


        self.button2a = QCheckBox('Activate')
        self.button2a = QCheckBox('Activate')
        self.button2b_minus = QPushButton('+')
        self.button2b_plus = QPushButton('-')

# Layout
        layout = QVBoxLayout()
        layout.addWidget(self.slider1_label)
        layout.addWidget(self.slider1)
        layout.addWidget(self.slider1_frequency_value_label)
        layout.addWidget(self.slider1_note_value_label)
        layout.addWidget(self.activationButton1)
        layout.addWidget(self.octaveDecreaseButton1)
        layout.addWidget(self.octaveIncreaseButton1)

        layout.addWidget(self.slider2_label)
        layout.addWidget(self.slider2)
        layout.addWidget(self.slider2_frequency_value_label)
        layout.addWidget(self.slider2_note_value_label)
        layout.addWidget(self.button2a)
        layout.addWidget(self.button2b_minus)
        layout.addWidget(self.button2b_plus)

        self.setLayout(layout)

        # Connect signals
        self.slider1.valueChanged.connect(lambda : self.slider_changed(self.slider1))
        self.slider2.valueChanged.connect(lambda : self.slider_changed(self.slider2))
        self.activationButton1.clicked.connect(self.function1a)         
        self.octaveDecreaseButton1.clicked.connect(lambda : self.octaveChange(self.slider1, -1))
        self.octaveIncreaseButton1.clicked.connect(lambda: self.octaveChange(self.slider1, 1))

        self.button2a.clicked.connect(self.function2a)
        self.button2b_minus.clicked.connect(lambda: self.octaveChange(self.slider2, -1))
        self.button2b_plus.clicked.connect(lambda: self.octaveChange(self.slider2, 1))

        self.setWindowTitle('Slider and Button Interface')
        self.show()

    def slider_changed(self, slider):
        self.frequency1 = utils.sliderValueToFrequency(slider.value())
        self.slider1_frequency_value_label.setText(f"Frequency: {int(self.frequency1)} Hz")
        self.slider1_note_value_label.setText(f"Note: {utils.getClosestNote(self.frequency1)}")

    # def slider2_changed(self, value):
    #     frequency = utils.sliderValueToFrequency(value)
    #     self.slider2_value_label.setText(f'Frequency: {frequency} Hz')
    #     print(f"Slider 2 Value: {value}")

    def function1a(self):
        print("Function 1a triggered")

    def function2a(self):
        print("Function 2a triggered")

    def adjust_slider_value(self, slider, step):
        new_value = slider.value() + step
        slider.setValue(new_value)
        slider_changed_function = getattr(self, f"{slider.objectName()}_changed", None)
        if slider_changed_function:
            slider_changed_function(new_value)

    def octaveChange(self, slider, delta):
        # Change slider position with new octave
        newFreq = utils.changeOctave(utils.sliderValueToFrequency(slider.value()), delta)
        newSliderValue = utils.frequencyToSliderValue(newFreq)
        step = newSliderValue - slider.value() 
        self.adjust_slider_value(slider, step)

    def displayClosestNote(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = UserInterface()
    sys.exit(app.exec_())

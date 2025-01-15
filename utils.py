import numpy as np

SAMPLE_RATE = 44100

NOTE_FREQUENCIES = {
    'C0': 16.35, 'C#0': 17.32, 'Db0': 17.32,
    'D0': 18.35, 'D#0': 19.45, 'Eb0': 19.45,
    'E0': 20.60, 'F0': 21.83, 'F#0': 23.12, 'Gb0': 23.12,
    'G0': 24.50, 'G#0': 25.96, 'Ab0': 25.96,
    'A0': 27.50, 'A#0': 29.14, 'Bb0': 29.14,
    'B0': 30.87,    
    'C1': 32.70, 'C#1': 34.65, 'Db1': 34.65,
    'D1': 36.71, 'D#1': 38.89, 'Eb1': 38.89,
    'E1': 41.20, 'F1': 43.65, 'F#1': 46.25, 'Gb1': 46.25,
    'G1': 49.00, 'G#1': 51.91, 'Ab1': 51.91,
    'A1': 55.00, 'A#1': 58.27, 'Bb1': 58.27,
    'B1': 61.74,
    'C2': 65.41, 'C#2': 69.30, 'Db2': 69.30,
    'D2': 73.42, 'D#2': 77.78, 'Eb2': 77.78,
    'E2': 82.41, 'F2': 87.31, 'F#2': 92.50, 'Gb2': 92.50,
    'G2': 98.00, 'G#2': 103.83, 'Ab2': 103.83,
    'A2': 110.00, 'A#2': 116.54, 'Bb2': 116.54,
    'B2': 123.47,
    'C3': 130.81, 'C#3': 138.59, 'Db3': 138.59,
    'D3': 146.83, 'D#3': 155.56, 'Eb3': 155.56,
    'E3': 164.81, 'F3': 174.61, 'F#3': 185.00, 'Gb3': 185.00,
    'G3': 196.00, 'G#3': 207.65, 'Ab3': 207.65,
    'A3': 220.00, 'A#3': 233.08, 'Bb3': 233.08,
    'B3': 246.94,
    'C4': 261.63, 'C#4': 277.18, 'Db4': 277.18,
    'D4': 293.66, 'D#4': 311.13, 'Eb4': 311.13,
    'E4': 329.63, 'F4': 349.23, 'F#4': 369.99, 'Gb4': 369.99,
    'G4': 392.00, 'G#4': 415.30, 'Ab4': 415.30,
    'A4': 440.00, 'A#4': 466.16, 'Bb4': 466.16,
    'B4': 493.88,
    'C5': 523.25, 'C#5': 554.37, 'Db5': 554.37,
    'D5': 587.33, 'D#5': 622.25, 'Eb5': 622.25,
    'E5': 659.25, 'F5': 698.46, 'F#5': 739.99, 'Gb5': 739.99,
    'G5': 783.99, 'G#5': 830.61, 'Ab5': 830.61,
    'A5': 880.00, 'A#5': 932.33, 'Bb5': 932.33,
    'B5': 987.77,
    'C6': 1046.50, 'C#6': 1108.73, 'Db6': 1108.73,
    'D6': 1174.66, 'D#6': 1244.51, 'Eb6': 1244.51,
    'E6': 1318.51, 'F6': 1396.91, 'F#6': 1479.98, 'Gb6': 1479.98,
    'G6': 1567.98, 'G#6': 1661.22, 'Ab6': 1661.22,
    'A6': 1760.00, 'A#6': 1864.66, 'Bb6': 1864.66,
    'B6': 1975.53,
    'C7': 2093.00, 'C#7': 2217.46, 'Db7': 2217.46,
    'D7': 2349.32, 'D#7': 2489.02, 'Eb7': 2489.02,
    'E7': 2637.02, 'F7': 2793.83, 'F#7': 2959.96, 'Gb7': 2959.96,
    'G7': 3135.96, 'G#7': 3322.44, 'Ab7': 3322.44,
    'A7': 3520.00, 'A#7': 3729.31, 'Bb7': 3729.31,
    'B7': 3951.07,
    'C8': 4186.01, 'C#8': 4434.92, 'Db8': 4434.92,
    'D8': 4698.63, 'D#8': 4978.03, 'Eb8': 4978.03,
    'E8': 5274.04, 'F8': 5587.65, 'F#8': 5919.91, 'Gb8': 5919.91,
    'G8': 6271.93, 'G#8': 6644.88, 'Ab8': 6644.88,
    'A8': 7040
}

MIN_FREQUENCY = 16
MAX_FREQUENCY = 7100

# Mapping of the keyboard to frequencies (in Hz)
KEY2FREQ = {
    'q': NOTE_FREQUENCIES["C4"],
    'z': NOTE_FREQUENCIES["C#4"],
    's': NOTE_FREQUENCIES["D4"],
    'e': NOTE_FREQUENCIES["D#4"],
    'd': NOTE_FREQUENCIES["E4"],
    'f': NOTE_FREQUENCIES["F4"],
    't': NOTE_FREQUENCIES["F#4"],
    'g': NOTE_FREQUENCIES["G4"],
    'y': NOTE_FREQUENCIES["G#4"],
    'h': NOTE_FREQUENCIES["A4"],
    'j': NOTE_FREQUENCIES["B4"],
    'k': NOTE_FREQUENCIES["C5"],
}

def changeOctave(frequency, octaveDiff):
    '''
    takes noteKey as input and octave delta and return new note key
    'A4' -1 -> 'A3'
    'C0' - 1 -> 'C0'
    '''
    if octaveDiff > 0:
        newFrequency = frequency*2 if frequency*2 <= MAX_FREQUENCY else frequency
    else:
        newFrequency = frequency/2 if frequency/2 >= MIN_FREQUENCY else frequency

    return newFrequency

def getClosestNote(frequency):
    closestNote = min(NOTE_FREQUENCIES, key=lambda x: abs(NOTE_FREQUENCIES[x] - frequency))
    return closestNote

def sliderValueToFrequency(value):
    '''
    From 0 to 100 to min, max of frequencies
    Logarithmic scale
    '''
    # Ensure the input value is within the [0, 100] range
    normalized_value = max(0, min(100, value))

    # Map to the logarithmic scale
    mapped_value = 10 ** (np.log10(MIN_FREQUENCY) + normalized_value * (np.log10(MAX_FREQUENCY) - np.log10(MIN_FREQUENCY)) / 100)

    return mapped_value

def frequencyToSliderValue(frequency):

    # Calculate the inverse mapping
    inverse_mapped_value = ((np.log10(frequency) - np.log10(MIN_FREQUENCY)) / (np.log10(MAX_FREQUENCY) - np.log10(MIN_FREQUENCY))) * 100

    return inverse_mapped_value

def getNoteRoundingError(self, frequency):
    '''
    returns the difference between the actual frequency and the closest note
    TODO: use this to change the color of the note displayed or simulate a led
    '''
    closestNote = self.getClosestNote(frequency)
    if closestNote == frequency:
        return 0
    # get surrounding notes
    lFrequencies = sorted(list(NOTE_FREQUENCIES.values()))
    closestNoteIdx = lFrequencies.index(closestNote)
    if frequency - closestNote > 0:
        neighbourNote = lFrequencies[closestNoteIdx + 1]
    else:
        neighbourNote = lFrequencies[closestNoteIdx - 1]

    # compute distance in Hz
    notesDistance = abs(closestNote - neighbourNote)
    noteError = abs(frequency - closestNote)

    # Error normalized by the distance between notes
    proportionError = noteError / notesDistance

    return proportionError

def getNoteFromFrequency(self, frequency):
    frequency = self.getClosestNote(frequency)
    for note in NOTE_FREQUENCIES:
        if NOTE_FREQUENCIES[note] == frequency:
            return note

def notes2freqs(chord):
    '''
    Takes a list of notes and outputs a list of correpsonding frequencies
    '''
    freqs = []
    for note in chord:
        freqs.append(NOTE_FREQUENCIES.get(note))
    return filter(None, freqs)
from synthesis import play_chord_with_envelope, generate_envelope
from utils import notes2freqs

NUM_OCTAVES = 5
NOTES = [
    
    f"{x}{y}" 
    for y in range(NUM_OCTAVES)
    for x in ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
    ]

def flatToSharp(note : str):
    def decrement_letter(letter):
        if 'A' <= letter <= 'G':  # Vérifie si la lettre est une majuscule
            return chr(ord(letter) - 1) if letter != 'A' else 'G'
        else:
            raise ValueError("Note should be between A and G")
    if "b" in note:
        sharpNote = decrement_letter(note[0])
        note = f"{sharpNote}#"

    return note

def buildChord(chordStr):
    '''
    Translates the chord specified in the prompt into a list of notes to play
    Example of prompts:
    C : C major
    Cm : C minor
    C7 : C major, 7 minor
    Gmaj7 : G major, 7 major
    F#m7 : F sharp minor seven
    Gdim : G diminished
    E0 : E Major but with lower notes possible
    The octave number is 3 by default (mid tones)
    '''

    octaveNumber = chordStr[0] if chordStr[0].isdigit() else '3'
    if chordStr[0].isdigit():
        octaveNumber = chordStr[0]
        chordStr = chordStr[1:]
    fundamental = chordStr[0] if '#' not in chordStr and 'b' not in chordStr else chordStr[:2] # c or E or G#
    fundamental = flatToSharp(fundamental)

    # We can specify the octave in the prompt [0 - 4], by default its 3 (mid tones)

    fundamental += octaveNumber
    noteIdx = NOTES.index(fundamental)

    chord = [
        fundamental
    ]

    # Thirds
    if "min" in chordStr or "dim" in chordStr:
        chord.append(minorThird(noteIdx))
    else:
        chord.append(majorThird(noteIdx))

    # Fifths
    if "dim" in chordStr:
        chord.append(fifth(noteIdx - 1))
    elif "aug" in chordStr:
        chord.append(fifth(noteIdx + 1))
    elif "6" in chordStr:
        chord.append(sixth(noteIdx))
    else:
        chord.append(fifth(noteIdx))

    # Seventh
    if "dim7" in chordStr:
        chord.append(sixth(noteIdx))
    elif "maj7" in chordStr:
        chord.append(majorSeventh(noteIdx))
    elif "7" in chordStr:
        chord.append(minorSeventh(noteIdx))

    # Nineth
    if "9" in chordStr:
        if "min" in chordStr:
            chord.append(minorSeventh(noteIdx))
            chord.append(nineth(noteIdx))
        else :
            chord.append(majorSeventh(noteIdx))
            chord.append(nineth(noteIdx))

    return chord

def decodeChordSequence(chordSequence : str):
    return

def getNote(idx):
    if idx > len(NOTES):
        # Lower an octave
        return NOTES[idx - 12]
    return NOTES[idx]

def minorThird(noteIdx):
    return getNote(noteIdx + 3)

def majorThird(noteIdx):
    return getNote(noteIdx + 4)

def fifth(noteIdx):
    return getNote(noteIdx + 7)

def sixth(noteIdx):
    return getNote(noteIdx + 9)

def minorSeventh(noteIdx):
    return getNote(noteIdx + 10)

def majorSeventh(noteIdx):
    return getNote(noteIdx + 11)

def nineth(noteIdx):
    return getNote(noteIdx + 14)

def testChords():
    print("Cmin")
    print(buildChord("Cmin"))
    print("C")
    print(buildChord("C"))
    print("Dmaj7")
    print(buildChord("Dmaj7"))
    print("F#min7")
    print(buildChord("F#min7"))
    print("Ab7")
    print(buildChord("Ab7"))
    print("A#dim")
    print(buildChord("A#dim"))
    print("Aaug")
    print(buildChord("Aaug"))
    print("Aaug7")
    print(buildChord("Aaug7"))
    print("C9")
    print(buildChord("C9"))

if __name__ == "__main__":
    chordSequence = [
        "Gmin", "F6", "Abmaj7", "Abmaj7",
        "Gmin", "F6", "Abmaj7", "Abmaj7",
        "Ebmaj7", "Bb", "D7", "G",
        "Cm7", "D7", "G7", "G"
        ]
    # chordSequence = [
    #     "2Gmin", "2F6", "2Abmaj7", "2Abmaj7",
    #     "2Gmin", "2F6", "2Abmaj7", "2Abmaj7",
    #     "2Ebmaj7", "2Bb", "2D7", "2G",
    #     "2Cm7", "2D7", "2G7", "2G"
    #     ]
    duration = 2
    t, envelope = generate_envelope(
        duration=duration,
        attack_time=0.3,
        decay_time=0.1,
        sustain_level=1,
        release_time=1
        )

    for chord in chordSequence:
        play_chord_with_envelope(notes2freqs(buildChord(chord)), duration, envelope)


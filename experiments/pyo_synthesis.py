from pyo import *

class SoundSynthesis():
    def __init__(self):
        self.wav = SquareTable()
        self.beat = Metro(time=1, poly=1).play()
        self.envelope = CosTable([(0, 0), (10, 1), (500, .3), (8191, 0)])
        self.amplitude = TrigEnv(self.beat, table=self.envelope, dur=1, mul=0.7)
        self.pitch = TrigXnoiseMidi(self.beat, dist=3, scale=0, nrange=(24, 24))

    def trigger(self):
        oscillator = Osc(table=self.wav, freq=self.pitch, mul=self.amplitude).out()

if __name__ == "__main__":
    sound = SoundSynthesis()
    sound.trigger()
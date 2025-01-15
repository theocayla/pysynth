import json
import matplotlib.pyplot as plt
import numpy as np

with open("data/waveform.json", 'r') as fp:
    x = json.load(fp)["data"]
plt.plot(x)
plt.savefig("test.png")
plt.show()
from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt
from audio_handling import *

file = findFile() # holds the WAV file
# makes sure the program only runs if a file was returned
# protects against cases such as when the user exits File Explorer prematurely
if (file != ""):
    samplerate, data = wavfile.read(file)
    print(f"number of channels = {data.shape[len(data.shape) - 1]}")
    print(f'this is data shape {data.shape}')
    print(f"sample rate = {samplerate}Hz")
    length = data.shape[0] / samplerate
    print(f"length = {length}s")

    samplerate, data = wavfile.read(file)
    print(f"number of channels = {data.shape[len(data.shape) - 1]}")
    print(f'this is data shape {data.shape}')
    print(f"sample rate = {samplerate}Hz")
    length = data.shape[0] / samplerate
    print(f"length = {length}s")


    time = np.linspace(0., length, data.shape[0])
    plt.plot(time, data[:, 0], label="Left channel")
    plt.plot(time, data[:, 1], label="Right channel")
    plt.legend()
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.show()
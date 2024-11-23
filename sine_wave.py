from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt


wav_fname = '16bit2chan.wav'
samplerate, data = wavfile.read(wav_fname)
# changes the value for "samplerate". Simply there for testing
samplerate -= 40000

print(f"number of channels = {data.shape[len(data.shape) - 1]}")
print(f'this is data shape {data.shape}')
print(f"sample rate = {samplerate}Hz")
length = data.shape[0] / samplerate
print(f"length = {length}s")

wav_fname = '16bit2chan.wav'
samplerate, data = wavfile.read(wav_fname)
# changes the value for "samplerate". Simply there for testing
samplerate -= 40000

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
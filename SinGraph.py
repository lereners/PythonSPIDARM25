from scipy.io import wavfile
import scipy.io
import wave

wav_fname = '16bit2chan.wav'
samplerate, data = wavfile.read(wav_fname)
print(f"number of channels = {data.shape[len(data.shape) - 1]}")
print(f'this is data shape {data.shape}')
print(f"sample rate = {samplerate}Hz")
length = data.shape[0] / samplerate
print(f"length = {length}s")

wav_fname = '16bit2chan.wav'
samplerate, data = wavfile.read(wav_fname)
print(f"number of channels = {data.shape[len(data.shape) - 1]}")
print(f'this is data shape {data.shape}')
print(f"sample rate = {samplerate}Hz")
length = data.shape[0] / samplerate
print(f"length = {length}s")

import matplotlib.pyplot as plt
import numpy as np
time = np.linspace(0., length, data.shape[0])
plt.plot(time, data[:, 0], label="Left channel")
plt.plot(time, data[:, 1], label="Right channel")
plt.legend()
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
plt.show()

# audioSpectrum mono only
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
sample_rate, data = wavfile.read('16bit1chan.wav')
spectrum, freqs, t, im = plt.specgram(data, Fs=sample_rate, \
                    NFFT=1024, cmap=plt.get_cmap('autumn_r'))
cbar = plt.colorbar(im)
plt.xlabel('Time (s)')
plt.ylabel('Frequency (Hz)')
cbar.set_label('Intensity (dB)')
plt.show()
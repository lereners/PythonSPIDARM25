from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter.filedialog import askopenfilename
from pydub import AudioSegment
from pathlib import Path
from scipy.io import wavfile
from scipy.signal import butter, filtfilt, welch, resample
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
import os

chosen_file = None
colors = ["red", "orange", "green", "blue"]

# implement soon







def audio_display(file_path):
    wave_subplot.clear()
    rt60_subplot.clear()

    plot_spec()

    if not chosen_file:
        return

    def find_channel_num():
        if len(data.shape) == 1:
            return 1
        else:
            return data.shape[1]

    def find_decibels():
        if find_channel_num() == 1:
            rms = np.sqrt(np.mean(data / 32768.0 ** 2))
        else:
            rms = np.sqrt(np.mean(data / 32768.0 ** 2, axis=0))  # Average across channels

        # Convert RMS to decibels
        decibels = 20 * np.log10(rms)*-1
        return decibels
    
    sample_rate, data = wavfile.read(file_path)
    length = data.shape[0] / sample_rate
    diff_display.config(text=f'RT60 Difference: {length - 0.5}')
    decibel_display.config(text=f'Decibels: {find_decibels()}')
    t = np.linspace(0, length, data.shape[0])
    time_display.config(text=f'Time: {length} s')
    channel_num = find_channel_num()

    if channel_num == 1:
        frequencies, power = welch(data, sample_rate, nperseg=4096)
        dom_freq = frequencies[np.argmax(power)]
        res_freq = round(dom_freq)
        res_display.config(text=f'Resonant Frequency: {res_freq} Hz')

        wave_subplot.plot(t, data, label="Mono channel")
        wave_subplot.set_title("Mono-Channel Audio File Plotted")

        plot_all_rt60(data, sample_rate)

        spectrum, freq, t, im = spec_subplot.specgram(data, Fs=sample_rate, NFFT=1024, cmap=plt.get_cmap("autumn_r"))
        calc_rt60(spectrum, freq, t, "r", label_value=1)

    if channel_num > 1:
        if channel_num == 2:
            wave_subplot.plot(t, data[:, 0], label="Right channel", color=colors[0])
            wave_subplot.plot(t, data[:, 1], label="Left channel", color=colors[1])
            wave_subplot.set_title(f"Dual-Channel Audio File Plotted")

        else:
            for x in range(channel_num):
                label_title = f'Channel {x + 1}'
                wave_subplot.plot(t, data[:, x], label=label_title, color=colors[x])
            wave_subplot.set_title(f"{x + 1}-Channel Audio File Plotted")


        frequencies, power = welch(data[:,0], sample_rate, nperseg=4096)
        dom_freq = frequencies[np.argmax(power)]
        res_freq = round(dom_freq)
        res_display.config(text=f'Resonant Frequency: {res_freq} Hz')


        plot_all_rt60(data[:,0], sample_rate)
        spectrum, freq, t, im = spec_subplot.specgram(data[:,0], Fs=sample_rate, NFFT=1024, cmap=plt.get_cmap("autumn_r"))
        spec_subplot.set_title("Spectrogram")
        calc_rt60(spectrum, freq, t, "r", label_value=f'Channel {channel_num}')

    wave_subplot.set_xlabel("Time [s]")
    wave_subplot.set_ylabel("Amplitude")
    wave_subplot.legend()
    wave_canvas.draw()

def choose_file():
    global chosen_file
    file_path = askopenfilename(filetypes=[("Audio Files", "*.wav *.mp3")])
    if not file_path:
        print("No file selection")
        return

    extension = Path(file_path).suffix

    if extension == ".mp3":
        dst = Path("Converted Sound File.wav")
        sound = AudioSegment.from_mp3(file_path)
        sound.export(dst, format="wav")
        file_path = str(dst)
        global chosen_file
        chosen_file = file_path
    if extension not in [".wav", ".mp3"]:
        print("Filetype not supported.")

    chosen_file = file_path
    file_name.config(text=f"File name: {os.path.basename(chosen_file)}")
    audio_display(file_path)

def plot_spec():
    spec_subplot.clear()

    if not chosen_file:
        return

    sample_rate, data = wavfile.read(chosen_file)

    if len(data.shape) == 1:
        spec_data = data
    elif len(data.shape) > 1:
        spec_data = data[:,0]
    spec_subplot.specgram(spec_data, Fs=sample_rate, NFFT=1024, cmap=plt.get_cmap("autumn_r"))
    spec_subplot.set_title("Spectrogram")
    spec_subplot.set_xlabel("Time [s]")
    spec_subplot.set_ylabel("Frequency [Hz]")

    spec_canvas.draw()

def find_decibels(self):
    if self.channel_num == 1:
        rms = np.sqrt(np.mean(self.data / 32768.0**2))
    else:
        rms = np.sqrt(np.mean(self.data / 32768.0**2, axis=0))  # Average across channels
        
    # Convert RMS to decibels
    decibels = 20 * np.log10(rms)
    print("The audio file is: " + decibels + "dBFS")

def goal_freq(freq):
    for x in freq:
        if x > 1000:
            break
        return x

def calc_rt60(spectrum, freq, t, color, label_value):
    rt60_subplot.clear()

    def frequency_check():
        # identify a frequency to check
        global target_frequency
        target_frequency = goal_freq(freq)
        index_of_frequency = np.where(freq == target_frequency)[0][0]  # find sound data for a particular frequency
        data_for_frequency = spectrum[index_of_frequency]
        # change a digital signal for a values in decibels
        data_in_db_fun = 10 * np.log10(data_for_frequency)
        return data_in_db_fun

    data_in_db = frequency_check()

    rt60_subplot.set_title("RT60 Graph")
    rt60_subplot.plot(t, data_in_db, color=color, linewidth=1, alpha=0.7)
    rt60_subplot.set_xlabel("Time (s)")
    rt60_subplot.set_ylabel("Power (dB)")
    rt60_subplot.legend()

    rt60_canvas.draw()

    # find an index of a max value
    index_of_max = np.argmax(data_in_db)
    value_of_max = data_in_db[index_of_max]
    rt60_subplot.plot(t[index_of_max], data_in_db[index_of_max], 'go')

    # slice our array from a max value
    sliced_array = data_in_db[index_of_max:]
    value_of_max_less_5 = value_of_max - 5

    # find nearest value of less 5db
    def find_nearest_value(array, value):
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return array[idx]

    value_of_max_less_5 = find_nearest_value(sliced_array, value_of_max_less_5)
    index_of_max_less_5 = np.where(data_in_db == value_of_max_less_5)
    rt60_subplot.plot(t[index_of_max_less_5], data_in_db[index_of_max_less_5], 'yo')

    # slice array from a max -5db
    value_of_max_less_25 = value_of_max - 25
    value_of_max_less_25 = find_nearest_value(sliced_array, value_of_max_less_25)
    index_of_max_less_25 = np.where(data_in_db == value_of_max_less_25)
    rt60_subplot.plot(t[index_of_max_less_25], data_in_db[index_of_max_less_25], 'ro')

    rt20 = (t[index_of_max_less_5] - t[index_of_max_less_25])[0]
    print(f'rt20= {rt20}')
    rt60 = 3 * rt20
    print(f'The RT60 reverb time at freq {int(data_in_db[index_of_max])}Hz is {round(abs(rt60), 2)} seconds')

def find_target_frequency(freqs, target):
    nearest_freq = freqs[np.abs(freqs - target).argmin()]
    return nearest_freq

def bandpass_filter(data, lowcut, highcut, fs, order=4):
    if len(data) < 27:
        data = resample(data, 27)

    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')

    return filtfilt(b, a, data, axis=0)

# Function to find the nearest value in the array
def find_nearest_value(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

def freq_range(freq_choice):
    if freq_choice == "Low":
        return [20, 250]
    elif freq_choice == "Mid":
        return [250, 2000]
    elif freq_choice == "High":
        return [2000, 20000]
    else:
        return [250, 2000]

def process_band(event):
    choice = freq_choice_input.get()
    sample_rate, data = wavfile.read(chosen_file)
    range = freq_range(choice)
    filtered_data = bandpass_filter(data, range[0], range[1], sample_rate)
    plot_filtered(filtered_data, sample_rate, choice, range[1])

def plot_filtered(filtered_data, sample_rate, freq_name, target):
    rt60_subplot.clear()

    if len(filtered_data.shape) == 1:
        channel_num = 1
    else:
        channel_num = filtered_data.shape[1]

    t = np.linspace(0, len(filtered_data) / sample_rate, len(filtered_data), endpoint=False)

    if channel_num > 1:
        for i in range(channel_num):
            channel_data = filtered_data[:,i]
        # rt60_subplot.plot(t, combined_data, color=colors[0])
    # else:
       #  rt60_subplot.plot(t, filtered_data, color=colors[0])

        fft_result = np.fft.fft(channel_data)
        spectrum = np.abs(fft_result)  # Get magnitude spectrum
        freqs = np.fft.fftfreq(len(channel_data), d=1 / sample_rate)

        # Use only positive frequencies
        freqs = freqs[:len(freqs) // 2]
        spectrum = spectrum[:len(spectrum) // 2]

        # Find the target frequency
        target_frequency = find_target_frequency(freqs, target)

        # Apply a band-pass filter around the target frequency
        filtered_data = bandpass_filter(channel_data, target_frequency - 50, target_frequency + 50, sample_rate)

        # Convert the filtered audio signal to decibel scale
        data_in_db = 10 * np.log10(np.abs(filtered_data) + 1e-10)  # Avoid log of zero

        # Plot the filtered signal in decibel scale
        rt60_subplot.plot(t, data_in_db, label=f"{target} Hz", linewidth=1, alpha=0.7)

    else:
        channel_data = filtered_data
        # rt60_subplot.plot(t, combined_data, color=colors[0])
        # else:
        #  rt60_subplot.plot(t, filtered_data, color=colors[0])

        fft_result = np.fft.fft(channel_data)
        spectrum = np.abs(fft_result)  # Get magnitude spectrum
        freqs = np.fft.fftfreq(len(channel_data), d=1 / sample_rate)

        # Use only positive frequencies
        freqs = freqs[:len(freqs) // 2]
        spectrum = spectrum[:len(spectrum) // 2]

        # Find the target frequency
        target_frequency = find_target_frequency(freqs, target)

        # Apply a band-pass filter around the target frequency
        filtered_data = bandpass_filter(channel_data, target_frequency - 50, target_frequency + 50, sample_rate)

        # Convert the filtered audio signal to decibel scale
        data_in_db = 10 * np.log10(np.abs(filtered_data) + 1e-10)  # Avoid log of zero

        # Plot the filtered signal in decibel scale
        rt60_subplot.plot(t, data_in_db, label=f"{target} Hz", linewidth=1, alpha=0.7)

    index_of_max = np.argmax(data_in_db)
    value_of_max = data_in_db[index_of_max]

  #  # Slice the array from the maximum value
    sliced_array = data_in_db[index_of_max:]
    value_of_max_less_5 = value_of_max - 5

  #  # Find the nearest value for max-5dB and its index
    value_of_max_less_5 = find_nearest_value(sliced_array, value_of_max_less_5)
    index_of_max_less_5 = np.where(data_in_db == value_of_max_less_5)[0][0]
#
  #  # Find the nearest value for max-25dB and its index
    value_of_max_less_25 = value_of_max - 25
    value_of_max_less_25 = find_nearest_value(sliced_array, value_of_max_less_25)
    index_of_max_less_25 = np.where(data_in_db == value_of_max_less_25)[0][0]

    # Calculate RT60 time
    rt20 = t[index_of_max_less_5] - t[index_of_max_less_25]
    rt60 = 3 * rt20


    rt60_subplot.set_title(f'{freq_name} RT60 Plot')
    rt60_subplot.set_xlabel("Time [s]")
    rt60_subplot.set_ylabel("Amplitude")
    # rt60_subplot.legend()
    rt60_canvas.draw()

def plot_all_rt60(data, sample_rate):
    all_rt60_subplot.clear()

    targets = [250, 2000, 20000]

    t = np.linspace(0, len(data) / sample_rate, len(data), endpoint=False)

    for target in targets:
        # Calculate the Fourier Transform of the signal
        fft_result = np.fft.fft(data)
        spectrum = np.abs(fft_result)  # Get magnitude spectrum
        freqs = np.fft.fftfreq(len(data), d=1 / sample_rate)

        # Use only positive frequencies
        freqs = freqs[:len(freqs) // 2]
        spectrum = spectrum[:len(spectrum) // 2]

        # Find the target frequency
        target_frequency = find_target_frequency(freqs, target)

        # Apply a band-pass filter around the target frequency
        filtered_data = bandpass_filter(data, target_frequency - 50, target_frequency + 50, sample_rate)

        # Convert the filtered audio signal to decibel scale
        data_in_db = 10 * np.log10(np.abs(filtered_data) + 1e-10)  # Avoid log of zero

        # Plot the filtered signal in decibel scale
        all_rt60_subplot.plot(t, data_in_db, label=f"{target} Hz", linewidth=1, alpha=0.7)

        # Find the index of the maximum value
        index_of_max = np.argmax(data_in_db)
        value_of_max = data_in_db[index_of_max]

        # Slice the array from the maximum value
        sliced_array = data_in_db[index_of_max:]
        value_of_max_less_5 = value_of_max - 5

        # Find the nearest value for max-5dB and its index
        value_of_max_less_5 = find_nearest_value(sliced_array, value_of_max_less_5)
        index_of_max_less_5 = np.where(data_in_db == value_of_max_less_5)[0][0]

        # Find the nearest value for max-25dB and its index
        value_of_max_less_25 = value_of_max - 25
        value_of_max_less_25 = find_nearest_value(sliced_array, value_of_max_less_25)
        index_of_max_less_25 = np.where(data_in_db == value_of_max_less_25)[0][0]

        # Calculate RT60 time
        rt20 = t[index_of_max_less_5] - t[index_of_max_less_25]
        rt60 = 3 * rt20

        # Print RT60 value
        print(f'The RT60 reverb time at freq {int(target_frequency)}Hz is {round(abs(rt60), 2)} seconds')

    all_rt60_subplot.set_title("RT60 Combo Graph")
    all_rt60_subplot.set_xlabel("Time (s)")
    all_rt60_subplot.set_ylabel("Power (dB)")
    all_rt60_subplot.legend()

    all_rt60_canvas.draw()



_root = tk.Tk()
_root.title ("Scientific Python Interactive Data Acoustic Modeling")
_root.resizable(True, True)
_root.geometry('1280x720')

buttons = tk.Frame(_root)
buttons.grid(row=0, column=1, padx=10, pady=10)

center_1 = tk.Frame(_root)
center_1.grid(row=1, column=1, padx=10, pady=10)

center_2 = tk.Frame(_root)
center_2.grid(row=2, column=1, padx=10, pady=10)

bottom = tk.Frame(_root)
bottom.grid(row=4, column=1, padx=10, pady=10)

import_btn = ttk.Button(buttons, text="Import Audio File", command=choose_file)
import_btn.pack()

file_name = tk.Label(buttons, text=chosen_file)
file_name.pack()

time_display = tk.Label(bottom, text="", fg="black")
time_display.pack()

res_display = tk.Label(bottom, text="", fg="black")
res_display.pack()

diff_display = tk.Label(bottom, text ="", fg="black")
diff_display.pack()

decibel_display = tk.Label(bottom, text ="", fg="black")
decibel_display.pack()

freq_var = tk.StringVar(center_1, value='Display Frequency')
freq_label = tk.Label(center_1, text='Frequency Choice')
freq_choices = ("Low", "Mid", "High")
freq_choice_input = ttk.Combobox(center_1, values=freq_choices, textvariable=freq_var, state='readonly')
freq_choice_input.grid(row=3, column=4)
freq_choice_input.bind("<<ComboboxSelected>>", process_band)

wave_frame = tk.Frame(center_1)
wave_frame.grid(row=2, column=1, padx=10, pady=20)
wave_figure = plt.figure(figsize=(4,4))
wave_subplot = wave_figure.add_subplot(111)
wave_canvas = FigureCanvasTkAgg(wave_figure, wave_frame)
wave_canvas.get_tk_widget().pack()
wave_toolbar = NavigationToolbar2Tk(wave_canvas, wave_frame, pack_toolbar=False)
wave_toolbar.update()
wave_toolbar.pack(anchor="w", fill=tk.X)

spec_frame = tk.Frame(center_1)
spec_frame.grid(row=2, column=3, padx=10, pady=20)
spec_figure = plt.figure(figsize=(4,4))
spec_subplot = spec_figure.add_subplot(111)
spec_canvas = FigureCanvasTkAgg(spec_figure, spec_frame)
spec_canvas.get_tk_widget().pack()
spec_toolbar = NavigationToolbar2Tk(spec_canvas, spec_frame, pack_toolbar=False)
spec_toolbar.update()
spec_toolbar.pack(anchor="w", fill=tk.X)

all_rt60_frame = tk.Frame(center_2)
all_rt60_frame.grid(row=2, column=2, padx=10, pady=20)
all_rt60_figure = plt.figure(figsize=(4,4))
all_rt60_subplot = all_rt60_figure.add_subplot(111)
all_rt60_canvas = FigureCanvasTkAgg(all_rt60_figure,all_rt60_frame)
all_rt60_canvas.get_tk_widget().pack()
all_rt60_toolbar = NavigationToolbar2Tk(all_rt60_canvas, all_rt60_frame, pack_toolbar=False)
all_rt60_toolbar.update()
all_rt60_toolbar.pack(anchor="w", fill=tk.X)

rt60_frame = tk.Frame(center_1)
rt60_frame.grid(row=2, column=4, padx=10, pady=20)
rt60_figure = plt.figure(figsize=(4,4))
rt60_subplot = rt60_figure.add_subplot(111)
rt60_canvas = FigureCanvasTkAgg(rt60_figure, rt60_frame)
rt60_canvas.get_tk_widget().pack()
rt60_toolbar = NavigationToolbar2Tk(rt60_canvas, rt60_frame, pack_toolbar=False)
rt60_toolbar.update()
rt60_toolbar.pack(anchor="w", fill=tk.X)


_root.mainloop()


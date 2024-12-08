from tkinter import *
from scipy.io import wavfile
from scipy.signal import butter, filtfilt, welch
import numpy as np
# using Figure to place the plot in the GUI
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

# Find the target frequency closest to target Hz
def find_target_frequency(freqs, target):
    nearest_freq = freqs[np.abs(freqs - target).argmin()]
    return nearest_freq

# Band-pass filter function
def bandpass_filter(data, lowcut, highcut, fs, order=4):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return filtfilt(b, a, data)

# Function to find the nearest value in the array
def find_nearest_value(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

class BaseAudio():
    def __init__(self, fpath, master_frame):

        self.file_name = os.path.basename(fpath)
        self.file_path = fpath
        self.channel_num = self.find_channel_num()
        self.sample_rate, self.data = wavfile.read(self.file_path)
        self.master_frame = master_frame
        self.length = self.data.shape[0] / self.sample_rate

        if self.channel_num == 1:
            self.frequencies, self.power = welch(self.data, self.sample_rate, nperseg=4096)
            self.dominant_frequency = self.frequencies[np.argmax(self.power)]
            self.res_freq = self.dominant_frequency
        elif self.channel_num > 1:
            self.frequencies, self.power = welch(self.data[:,0], self.sample_rate, nperseg=4096)
            self.dominant_frequency = self.frequencies[np.argmax(self.power)]
            self.res_freq = self.dominant_frequency

        print(f'Dominant Frequency is {round(self.dominant_frequency)}Hz')
        self.rt60_diff = self.length - 0.5
        print("hello!!! init BaseAudio")

    def find_channel_num(self):
        if len(self.data.shape) == 1:
            return 1
        else:
            return self.data.shape[1]

    def plot_wave(self):
            print(f"number of channels = {self.channel_num}")
            print(f'this is data shape {self.data.shape}')
            print(f"sample rate = {self.sample_rate}Hz")
            print(f"length = {self.length}s")

            time = np.linspace(0., self.length, self.data.shape[0])

            # using matplotlib figures
            fig = Figure(figsize=(7, 5), dpi=100)
            plt = fig.add_subplot(111)

            if self.channel_num == 1:
                plt.plot(time, self.data, label="Mono channel")
                plt.set_title("Mono-Channel Audio File Plotted")

            if self.channel_num > 1:
                for x in range(self.channel_num):
                    label_title = f'Channel {x + 1}'
                    plt.plot(time, self.data[:, x], label=label_title)
                    plt.set_title("Two-Channel Audio File Plotted")

            plt.set_xlabel("Time [s]")
            plt.set_ylabel("Amplitude")
            plt.legend()

            # displaying the plot
            plot = FigureCanvasTkAgg(fig, master=self.master_frame)
            plot_display = plot.get_tk_widget()
            plot_display.grid(row=2, column=1, sticky=(N, E, S, W))
            plot.draw()
            # maybe to choose low, mid, high rt60 frequencies?
            # not sure if this would actually work, just using dummy numbers (2000, 5000)

    def plot_rt60(self, data, sample_rate, target):
            # Define the time vector
            t = np.linspace(0, len(data) / sample_rate, len(data), endpoint=False)

            # Calculate the Fourier Transform of the signal
            fft_result = np.fft.fft(data)
            spectrum = np.abs(fft_result)
            # Get magnitude spectrum
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
            fig_rt60 = Figure(figsize=(7, 5), dpi=100)
            plt = fig_rt60.add_subplot(111)

            plt.set_title("Audio File Plotted")
            plt.set_xlabel("Time [s]")
            plt.set_ylabel("Power (dB)")

            plt.plot(t, data_in_db, linewidth=1, alpha=0.7, color='#004bc6')

            # Find the index of the maximum value
            index_of_max = np.argmax(data_in_db)
            value_of_max = data_in_db[index_of_max]
            plt.plot(t[index_of_max], data_in_db[index_of_max], 'go')

            # Slice the array from the maximum value
            sliced_array = data_in_db[index_of_max:]
            value_of_max_less_5 = value_of_max - 5

            # Find the nearest value for max-5dB and its index
            value_of_max_less_5 = find_nearest_value(sliced_array, value_of_max_less_5)
            index_of_max_less_5 = np.where(data_in_db == value_of_max_less_5)[0][0]
            plt.plot(t[index_of_max_less_5], data_in_db[index_of_max_less_5], 'yo')

            # Find the nearest value for max-25dB and its index
            value_of_max_less_25 = value_of_max - 25
            value_of_max_less_25 = find_nearest_value(sliced_array, value_of_max_less_25)
            index_of_max_less_25 = np.where(data_in_db == value_of_max_less_25)[0][0]
            plt.plot(t[index_of_max_less_25], data_in_db[index_of_max_less_25], 'ro')

            # Calculate RT60 time
            rt20 = t[index_of_max_less_5] - t[index_of_max_less_25]
            rt60 = 3 * rt20

            # Print RT60 value
            print(f'The RT60 reverb time at freq {int(target_frequency)}Hz is {round(abs(rt60), 2)} seconds')

            # displaying the plot
            plot = FigureCanvasTkAgg(fig_rt60, master=self.master_frame)
            plot_display = plot.get_tk_widget()
            plot_display.grid(row=2, column=1, sticky=(N, E, S, W))
            plot.draw()

    def plot_all_rt60(self):
        # Placeholder values for testing

        # Load the audio file

        # Target frequencies to analyze
        targets = [250, 2000, 8000]

        # Create a single figure for all RT60 plots
        fig_rt60 = Figure(figsize=(7, 5), dpi=100)
        plt = fig_rt60.add_subplot(111)

        # Define the time vector
        t = np.linspace(0, len(self.data) / self.sample_rate, len(self.data), endpoint=False)

        for target in targets:
            # Calculate the Fourier Transform of the signal
            fft_result = np.fft.fft(self.data)
            spectrum = np.abs(fft_result)  # Get magnitude spectrum
            freqs = np.fft.fftfreq(len(self.data), d=1 / self.sample_rate)

            # Use only positive frequencies
            freqs = freqs[:len(freqs) // 2]
            spectrum = spectrum[:len(spectrum) // 2]

            # Find the target frequency
            target_frequency = find_target_frequency(freqs, target)

            # Apply a band-pass filter around the target frequency
            filtered_data = bandpass_filter(self.data, target_frequency - 50, target_frequency + 50, self.sample_rate)

            # Convert the filtered audio signal to decibel scale
            data_in_db = 10 * np.log10(np.abs(filtered_data) + 1e-10)  # Avoid log of zero

            # Plot the filtered signal in decibel scale
            plt.plot(t, data_in_db, label=f"{target} Hz", linewidth=1, alpha=0.7)

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

        # Finalize the plot
        plt.set_title("RT60 Analysis for Different Frequencies")
        plt.set_xlabel("Time [s]")
        plt.set_ylabel("Power (dB)")
        plt.legend()
        plt.grid(True)

        # Displaying the plot
        plot = FigureCanvasTkAgg(fig_rt60, master=self.master_frame)
        plot_display = plot.get_tk_widget()
        plot_display.grid(row=2, column=1, sticky=(N, E, S, W))
        plot.draw()

    # plot_choice from combobox - new argument
    def plot_as_chosen(self, plot_choice):
        # these 4 have placeholder values, just to test the text appearance
        # likely have these as class properties

        # combine all plotting funcs into a class method?!
        if plot_choice == "Waveform":
            self.plot_wave()
        elif plot_choice == "Low RT60":
            self.plot_rt60(self.data, self.sample_rate, 1000)
        elif plot_choice == "Med RT60":
            self.plot_rt60(self.data, self.sample_rate, 2000)
        elif plot_choice == "High RT60":
            self.plot_rt60(self.data, self.sample_rate, 5000)
        elif plot_choice == "Spectrogram":
            self.plot_spec()
            return

        # displays info, which is not dependent on plot choice
        self.display_info()


    def display_info(self):
        # height=2 means that text displays 4 lines of text
        audio_info = Text(self.master_frame, height=4)
        # row=3 is below the plot (row=2)
        audio_info.grid(row=3, column=1, sticky=(E, W))
        # displaying the required information
        # maybe omit file name if we display it in the plot title?
        # chose the "property: value" format because the FAQ ppt slide 5 uses that format for the RT60 difference
        audio_info.insert(INSERT, f"File name: {self.file_name}\n")
        audio_info.insert(INSERT, f"Length: {self.length}s.\n")
        audio_info.insert(INSERT, f"Resonant frequency: {self.res_freq} Hz.\n")
        audio_info.insert(INSERT, f"RT60 difference: {self.rt60_diff} ")

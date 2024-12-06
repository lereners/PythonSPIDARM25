from tkinter import *
from scipy.io import wavfile
from scipy.signal import butter, filtfilt, welch
import numpy as np
# using Figure to place the plot in the GUI
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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
    def __init__(self, fname, fpath):
        self.file_name = fname
        self.file_path = fpath
        # Load the audio file
        self.samplerate, self.data = wavfile.read(self.file_name)
        print("hello!!! init BaseAudio")

    def plot_wave(self):
            print(f"number of channels = {self.data.shape[len(self.data.shape) - 1]}")
            print(f'this is data shape {self.data.shape}')
            print(f"sample rate = {self.sample_rate}Hz")
            length = self.data.shape[0] / self.sample_rate
            print(f"length = {length}s")

            time = np.linspace(0., length, self.data.shape[0])

            # using matplotlib figures
            fig = Figure(figsize=(7, 5), dpi=100)
            plt = fig.add_subplot(111)

            # plot formatting
            plt.plot(time, self.data[:, 0], label="Left channel")
            plt.set_xlabel("Time [s]")
            plt.set_ylabel("Amplitude")
            # change this to file name + plot type?
            # ex: scream.wav Waveform
            # ex: shout.wav RT60 Combines
            plt.set_title("Audio File Plotted")
            plt.legend()

            # displaying the plot
            plot = FigureCanvasTkAgg(fig, master=gui._plot_frame)
            plot_display = plot.get_tk_widget()
            plot_display.grid(row=2, column=1, sticky=(N, E, S, W))
            plot.draw()
            # maybe to choose low, mid, high rt60 frequencies?
            # not sure if this would actually work, just using dummy numbers (2000, 5000)

    # plot_choice from combobox - new argument
    def plot_as_chosen(self, data, sample_rate, plot_choice):
        # these 4 have placeholder values, just to test the text appearance
        # likely have these as class properties
        file_name = "FILE NAME!!"
        audio_length = 34
        frequencies, power = welch(data, sample_rate, nperseg=4096)
        dominant_frequency = frequencies[np.argmax(power)]
        print(f'dominant_frequency is {round(dominant_frequency)}Hz')
        res_freq = dominant_frequency
        rt60_diff = 0.7

        # combine all plotting funcs into a class method?!
        if plot_choice == "Waveform":
            BaseAudio.plot_wave()
        elif plot_choice == "Low RT60":
            PlotRT60.plot_rt60(1000)
        elif plot_choice == "Med RT60":
            PlotRT60.plot_rt60(2000)
        elif plot_choice == "High RT60":
            PlotRT60.plot_rt60(5000)
        elif plot_choice == "Spectrogram":
            PlotRT60.plot_spec()

        # height=2 means that text displays 4 lines of text
        audio_info = Text(gui._plot_frame, height=4)
        # row=3 is below the plot (row=2)
        audio_info.grid(row=3, column=1, sticky=(E, W))
        # displaying the required information
        # maybe omit file name if we display it in the plot title?
        # chose the "property: value" format because the FAQ ppt slide 5 uses that format for the RT60 difference
        audio_info.insert(INSERT, f"File name: {file_name}\n")
        audio_info.insert(INSERT, f"Length: {audio_length}s.\n")
        audio_info.insert(INSERT, f"Resonant frequency: {res_freq} Hz.\n")
        audio_info.insert(INSERT, f"RT60 difference: {rt60_diff} ")


class PlotRT60(BaseAudio):
    def __init__(self, wav_fname, data, sample_rate):
        self.wav_fname = wav_fname
        self.sample_rate = sample_rate
        self.data = data

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
            plot = FigureCanvasTkAgg(fig_rt60, master=gui._plot_frame)
            plot_display = plot.get_tk_widget()
            plot_display.grid(row=2, column=1, sticky=(N, E, S, W))
            plot.draw()

    def plot_all_rt60(self):
        # Placeholder values for testing
        file_name = "FILE NAME!!"
        audio_length = 34
        res_freq = 24
        rt60_diff = 0.7

        # Load the audio file
        sample_rate, data = wavfile.read("16bit1chan.wav")

        # Target frequencies to analyze
        targets = [250, 2000, 8000]

        # Create a single figure for all RT60 plots
        fig_rt60 = Figure(figsize=(7, 5), dpi=100)
        plt = fig_rt60.add_subplot(111)

        # Define the time vector
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
        plot = FigureCanvasTkAgg(fig_rt60, master=gui._plot_frame)
        plot_display = plot.get_tk_widget()
        plot_display.grid(row=2, column=1, sticky=(N, E, S, W))
        plot.draw()        

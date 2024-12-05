from tkinter import *
from tkinter import ttk
import tkinter as tk

from scipy.io import wavfile
from scipy.signal import butter, filtfilt

import numpy as np
# using Figure to place the plot in the GUI
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Band-pass filter function
def bandpass_filter(data, lowcut, highcut, fs, order=4):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return filtfilt(b, a, data)

# Find the target frequency closest to target Hz
def find_target_frequency(freqs, target):
    nearest_freq = freqs[np.abs(freqs - target).argmin()]
    return nearest_freq

# Function to find the nearest value in the array
def find_nearest_value(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

def plot_wave():
    wav_fname = '16bit2chan.wav'
    samplerate, data = wavfile.read(wav_fname)
    print(f"number of channels = {data.shape[len(data.shape) - 1]}")
    print(f'this is data shape {data.shape}')
    print(f"sample rate = {samplerate}Hz")
    length = data.shape[0] / samplerate
    print(f"length = {length}s")

    time = np.linspace(0., length, data.shape[0])

    # using matplotlib figures
    fig = Figure(figsize=(7, 5), dpi=100)
    plt = fig.add_subplot(111)

    # plot formatting
    plt.plot(time, data[:, 0], label="Left channel")
    plt.set_xlabel("Time [s]")
    plt.set_ylabel("Amplitude")
    # change this to file name + plot type?
    # ex: scream.wav Waveform
    # ex: shout.wav RT60 Combines
    plt.set_title("Audio File Plotted")
    plt.legend()

    # displaying the plot
    plot = FigureCanvasTkAgg(fig, master=_plot_frame)
    plot_display = plot.get_tk_widget()
    plot_display.grid(row=2, column=1, sticky=(N, E, S, W))
    plot.draw()

# taken from colab, added target argument to choose the target frequency (possibly to plot the low, mid, high)
# have not modified a lot of this code, just the stuff to use the matplotlib figure
def plot_rt60(target):
    # Load the audio file
    sample_rate, data = wavfile.read("16bit1chan.wav")

    # Define the time vector
    t = np.linspace(0, len(data) / sample_rate, len(data), endpoint=False)

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
    plot = FigureCanvasTkAgg(fig_rt60, master=_plot_frame)
    plot_display = plot.get_tk_widget()
    plot_display.grid(row=2, column=1, sticky=(N, E, S, W))
    plot.draw()
def plot_all_rt60():
    # Placeholder values for testing
    file_name = "FILE NAME!!"
    audio_length = 34
    res_freq = 24
    rt60_diff = 0.7

    # Load the audio file
    sample_rate, data = wavfile.read("16bit1chan.wav")

    # Target frequencies to analyze
    targets = [1000, 2000, 5000]

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
    plot = FigureCanvasTkAgg(fig_rt60, master=_plot_frame)
    plot_display = plot.get_tk_widget()
    plot_display.grid(row=2, column=1, sticky=(N, E, S, W))
    plot.draw()

# maybe to choose low, mid, high rt60 frequencies?
# not sure if this would actually work, just using dummy numbers (2000, 5000)
def plot_as_chosen():
    # these 4 have placeholder values, just to test the text appearance
    # likely have these as class properties
    file_name = "FILE NAME!!"
    audio_length = 34
    res_freq = 24
    rt60_diff = 0.7

    plot_choice = plot_var.get()

    # combine all plotting funcs into a class method?!
    if plot_choice == "Waveform":
        plot_wave()
    elif plot_choice == "Low RT60":
        plot_rt60(1000)
    elif plot_choice == "Med RT60":
        plot_rt60(2000)
    elif plot_choice == "High RT60":
        plot_rt60(5000)
    elif plot_choice == "Spectrogram":
        plot_spec()

    # height=2 means that text displays 4 lines of text
    audio_info = Text (_plot_frame, height=4)
    # row=3 is below the plot (row=2)
    audio_info.grid(row=3, column=1, sticky=(E, W))
    # displaying the required information
    # maybe omit file name if we display it in the plot title?
    # chose the "property: value" format because the FAQ ppt slide 5 uses that format for the RT60 difference
    audio_info.insert(INSERT, f"File name: {file_name}\n")
    audio_info.insert(INSERT, f"Length: {audio_length}s.\n")
    audio_info.insert(INSERT, f"Resonant frequency: {res_freq} Hz.\n")
    audio_info.insert(INSERT, f"RT60 difference: {rt60_diff} ")

# just a placeholder for plot_as_chosen ....
def plot_spec():
    return "this is not implemented ! hahaha"

if __name__ == "__main__":
    _root = Tk()
    _root.title ("Scientific Python Interactive Data Acoustic Modeling")
    _root.resizable(True, True)

    _base = ttk.Frame(_root, padding='5 5 8 8')
    _base.grid(row=0, column=0, sticky=(N, E, S, W))

    # frame to hold the buttons
    _button_frame = ttk.LabelFrame(_base, text="Buttons")
    _button_frame.grid(row=1, column=1, sticky=(E, W))

    # button to load + plot audio
    # currently hooked up with the plot function (just plotting the audio file bc it is currently hard coded to open a specific file)
    _load_btn = ttk.Button(_button_frame, text="Load and Plot Audio File", command=plot_wave)
    _load_btn.grid(row=1, column=1, sticky=W)

    # frame to hold the plots
    _plot_frame = ttk.LabelFrame(_base, text="Plots")
    _plot_frame.grid(row=3, column=1, sticky=(E, W))

    # combobox to choose which plot to display
    plot_var = tk.StringVar(value='Choose a Plot')  # holds choice
    plot_label = tk.Label(_plot_frame, text='Plot Display Choice')
    plot_choices = ("Waveform", "Low RT60", "Med RT60", "High RT60", "Spectrogram", "Creative Choice")
    plot_choice_input = ttk.Combobox(_button_frame, values=plot_choices, textvariable=plot_var, state='readonly')
    plot_choice_input.grid(row=2, column=1, sticky=E)

    # depending on the plot chosen in the combobox, plot_as_chosen will plot the specific plot
    # currently, it is set up that we have one window that displays plots, and the window will change its display depending on the combobox choice
    # maybe choose to have all the plots at once? the display selector seems cool, though...
    load_btn_2 = ttk.Button(_button_frame, text="Display Plot", command=plot_as_chosen)
    load_btn_2.grid(row=2, column=2, sticky=W)

    # button to combine rt60 plots
    rt60_combo_btn = ttk.Button(_button_frame, text="Combine RT60 Frequencies", command=plot_all_rt60)
    rt60_combo_btn.grid(row=1, column=2, sticky=W)


    _root.mainloop()

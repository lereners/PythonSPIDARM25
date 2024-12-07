# maybe to choose low, mid, high rt60 frequencies?
# not sure if this would actually work, just using dummy numbers (2000, 5000)
from tkinter import *
from tkinter import ttk
import tkinter as tk
# using Figure to place the plot in the GUI
from tkinter.filedialog import askopenfilename
from pydub import AudioSegment
from pathlib import Path
from PlotClass import BaseAudio

global chosen_file_path, working_audio
working_audio = None

# tk.Tk().withdraw() # part of the import if you are not using other tkinter functions
# allows the user to select either a WAV or MP3 file and returns a .wav file
def findFile():
    # opens File Explorer and allows the user to find and select either a WAV or MP3 file, then stores it in "fn"
    fn = askopenfilename(filetypes=[("WAV Files", "*.wav"), ('MP3 Files', '*.mp3')])
    extension = Path(fn).suffix  # holds the extension of the selected file
    filePath = fn  # stores a copy of the selected file's path

    # checks to see if the file is an MP3
    if (extension == ".mp3"):
        # makes a dummy WAV file to store the converted audio
        dst = "Converted Sound File.wav"

        # converts the selected MP3 file into WAV format
        sound = AudioSegment.from_mp3(fn)
        sound.export(dst, format="wav")
        filePath = dst

    chosen_file_path = filePath
    working_audio = BaseAudio(chosen_file_path, _plot_frame)

    # sw = 0
    # with wave.open(filePath, "rb") as waveFile:
    #     sw = waveFile.getsampwidth()
    #     waveFile.close()

    # with wave.open(filePath, "w") as waveFile:
    #     waveFile.setnchannels(1)
    #     #waveFile.setsampwidth(16)
    #     waveFile.close()
    # returns a WAV file

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

    # frame to hold the plots
    _plot_frame = ttk.LabelFrame(_base, text="Plots")
    _plot_frame.grid(row=3, column=1, sticky=(E, W))

    # combobox to choose which plot to display
    plot_var = tk.StringVar(value='Choose a Plot')  # holds choice
    plot_label = tk.Label(_plot_frame, text='Plot Display Choice')
    plot_choices = ("Waveform", "Low RT60", "Med RT60", "High RT60", "Spectrogram", "Creative Choice")
    plot_choice_input = ttk.Combobox(_button_frame, values=plot_choices, textvariable=plot_var, state='readonly')
    plot_choice_input.grid(row=2, column=1, sticky=E)

    # button to load an audio file
    _load_btn = ttk.Button(_button_frame, text="Load Audio File", command=findFile)
    _load_btn.grid(row=1, column=1, sticky=W)


    # depending on the plot chosen in the combobox, plot_as_chosen will plot the specific plot
    # currently, it is set up that we have one window that displays plots, and the window will change its display depending on the combobox choice
    # lambda so that the button's function doesn't run immediately
    load_btn_2 = ttk.Button(_button_frame, text="Display Plot", command=lambda : working_audio.plot_as_chosen(plot_choice_input.get()) if working_audio else None)
    load_btn_2.grid(row=2, column=2, sticky=W)

    # button to combine rt60 plots
    rt60_combo_btn = ttk.Button(_button_frame, text="Combine RT60 Frequencies", command=working_audio.plot_all_rt60 if working_audio else None)
    rt60_combo_btn.grid(row=1, column=2, sticky=W)

    _root.mainloop()
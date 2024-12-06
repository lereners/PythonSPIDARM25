# maybe to choose low, mid, high rt60 frequencies?
# not sure if this would actually work, just using dummy numbers (2000, 5000)
from tkinter import *
from tkinter import ttk
import tkinter as tk
# using Figure to place the plot in the GUI
import PlotClass
from tkinter.filedialog import askopenfilename
from pydub import AudioSegment
from pathlib import Path
import os
from PlotClass import BaseAudio

# tk.Tk().withdraw() # part of the import if you are not using other tkinter functions

# allows the user to select either a WAV or MP3 file and returns a .wav file
def findFile():
    # opens File Explorer and allows the user to find and select either a WAV or MP3 file, then stores it in "fn"
    fn = askopenfilename(filetypes=[("WAV Files", "*.wav"), ('MP3 Files', '*.mp3')])
    extension = Path(fn).suffix  # holds the extension of the selected file
    filePath = fn  # stores a copy of the selected file's path
    fileName = os.path.basename(filePath)

    # checks to see if the file is an MP3
    if (extension == ".mp3"):
        # makes a dummy WAV file to store the converted audio
        dst = "Converted Sound File.wav"

        # converts the selected MP3 file into WAV format
        sound = AudioSegment.from_mp3(fn)
        sound.export(dst, format="wav")
        filePath = dst

    # sw = 0
    # with wave.open(filePath, "rb") as waveFile:
    #     sw = waveFile.getsampwidth()
    #     waveFile.close()

    # with wave.open(filePath, "w") as waveFile:
    #     waveFile.setnchannels(1)
    #     #waveFile.setsampwidth(16)
    #     waveFile.close()
    # returns a WAV file

    return filePath

def chooseName():
    # GLOBAL!! TO ACCESS FILE NAME WHEREVER I GUESS............
    global chosen_file_path
    chosen_file_path = findFile()

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

    # button to load + plot audio
    # currently hooked up with the plot function (just plotting the audio file bc it is currently hard coded to open a specific file)
    _load_btn = ttk.Button(_button_frame, text="Load Audio File", command=chooseName())
    _load_btn.grid(row=1, column=1, sticky=W)

    working_audio = BaseAudio(chosen_file_path, _plot_frame)

    # depending on the plot chosen in the combobox, plot_as_chosen will plot the specific plot
    # currently, it is set up that we have one window that displays plots, and the window will change its display depending on the combobox choice
    # maybe choose to have all the plots at once? the display selector seems cool, though...
    load_btn_2 = ttk.Button(_button_frame, text="Display Plot", command=working_audio.plot_as_chosen(plot_var.get()))
    load_btn_2.grid(row=2, column=2, sticky=W)

    # button to combine rt60 plots, not implemented at all! just placeholder
    rt60_combo_btn = ttk.Button(_button_frame, text="Combine RT60 Frequencies", command=working_audio.plot_all_rt60)
    rt60_combo_btn.grid(row=1, column=2, sticky=W)

    _root.mainloop()
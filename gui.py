
# maybe to choose low, mid, high rt60 frequencies?
# not sure if this would actually work, just using dummy numbers (2000, 5000)
from tkinter import *
from tkinter import ttk
import tkinter as tk

import os
from audio_handling import findFile

from scipy.io import wavfile
from scipy.signal import butter, filtfilt, welch

import numpy as np
# using Figure to place the plot in the GUI
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PlotClass

from audio_handling import *
from pathlib import Path

currentFile = ''

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
    # _load_btn = ttk.Button(_button_frame, text="Load and Plot Audio File", command=plot_wave)
    _load_btn = ttk.Button(_button_frame, text="Load and Plot Audio File", command=find_and_plot)
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
    load_btn_2 = ttk.Button(_button_frame, text="Display Plot", command=PlotClass.PlotWave.plot_as_chosen)
    load_btn_2.grid(row=2, column=2, sticky=W)


    # button to combine rt60 plots, not implemented at all! just placeholder
    rt60_combo_btn = ttk.Button(_button_frame, text="Combine RT60 Frequencies", command=PlotClass.PlotRT60.plot_all_rt60)

    # button to combine rt60 plots
    rt60_combo_btn = ttk.Button(_button_frame, text="Combine RT60 Frequencies", command=plot_all_rt60)



    _root.mainloop()

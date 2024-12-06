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
    extension = Path(fn).suffix # holds the extension of the selected file
    filePath = fn # stores a copy of the selected file's path
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

    return BaseAudio(filePath, fileName)


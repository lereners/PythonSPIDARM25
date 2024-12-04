from pathlib import Path
from scipy.io import wavfile
import os
def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)
# with open("IMG_3016.mp3") as test:
pSome = Path("IMG_3016.mp3")
path = pSome.parent.absolute()
# another = Path('C:\Users\nat52\Python Final Project\PythonSPIDARM25')
# print(pSome)
# print(path)
# print(another)
# pSome.open()
wav_fname = '16bit2chan.wav'
# path = r'{C:\Users\nat52\Python Final Project}'
path = r"C:\Users\nat52\Documents"
samplerate, data = wavfile.read(find("16bit2chan.wav", path))
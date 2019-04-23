from scipy.io import wavfile
import numpy as np

def dB_extraction():
    fs, data = wavfile.read('test2.wav')
    abs_data=np.absolute(data)
    amp=np.divide(abs_data,32767)
    #print(amp)
    decibels=20*np.log10(amp)
    dB=np.absolute(decibels)
    #print(dB)
    dB_x=np.delete(dB,np.where(dB==[np.inf]))
    mean_dB=np.median(dB_x)
    print(mean_dB)
    return mean_dB

dB_extraction()


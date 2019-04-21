import soundfile as sf 
import numpy as np 
import math

def dB_extraction():
    data,samplerate=sf.read('test4.wav')
    decibels=np.absolute(20*(np.log10(abs(data))))
    dB=np.delete(decibels,np.where(decibels==[np.inf]))
    mean_dB=np.mean(dB)
    print(mean_dB)
    return mean_dB

dB_extraction()
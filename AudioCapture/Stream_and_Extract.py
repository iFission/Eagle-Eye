import pyaudio
import numpy as np

def dB_extraction():
    CHUNK = 2**11
    RATE = 44100

    p=pyaudio.PyAudio()
    stream=p.open(format=pyaudio.paInt16,rate=RATE,channels=1,input_device_index = 2,input=True,
              frames_per_buffer=CHUNK)
    peaks=0
    counter=0
    print('Recording')
    for i in range(int(44100/1024)): #go for a few seconds  #Make sure you change the seconds
        data = np.fromstring(stream.read(CHUNK,exception_on_overflow = False),dtype=np.int16)
        peak=np.average(np.abs(data))*2
        peaks+=peak
        counter+=1
        bars="#"*int(50*peak/2**16)
    print('Finished recording')
    mean_peak=peaks/counter

    stream.stop_stream()
    stream.close()
    p.terminate()
    
    return mean_peak
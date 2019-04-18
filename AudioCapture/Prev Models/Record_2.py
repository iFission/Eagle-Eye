import pyaudio
import numpy as np

#Recheck if peak is actually the decibel of the voice

CHUNK = 2**11
RATE = 44100

p=pyaudio.PyAudio()
stream=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input_device_index = 2,input=True,
              frames_per_buffer=CHUNK)

print('recording')
for i in range(int(3*44100/1024)): #go for a few seconds
    data = np.fromstring(stream.read(CHUNK,exception_on_overflow = False),dtype=np.int16)
    peak=np.average(np.abs(data))*2
    print(peak)
    #bars="#"*int(50*peak/2**16)
    #print("%04d %05d %s"%(i,peak,bars))
print('done')
stream.stop_stream()
stream.close()
p.terminate()
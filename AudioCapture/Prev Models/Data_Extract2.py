from scipy.io.wavfile import read
samprate, wavdata = read('test2.wav')
import numpy as np
from math import sqrt
numchunks=4096
chunks = np.array_split(wavdata, numchunks)
for chunk in chunks:
    if abs(np.sum(chunk))==np.inf:
        np.delete(chunk,np.where(chunk==[np.inf]))
        print(chunk)
dbs = np.array([20*np.log10(sqrt(np.mean(chunk**2))) for chunk in chunks])
print(np.mean(dbs))
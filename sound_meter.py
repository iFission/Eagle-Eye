import time
import backend
from AudioCapture.Data_Extract import dB_extraction
from AudioCapture.Record_Sound import record_and_write
def main():
    node = backend.FireBaseNode('Noise')
    while True:
        #Records an audio file for 3 seconds for noise level
        record_and_write()

        #Gets the average decibel in that audio file
        noise=dB_extraction()
        
        # Upload to firebase
        node.val = noise
        localtime = time.asctime(time.localtime(time.time()))
        print(f'{localtime}: Noise={node.val}')

        # sleep
        time.sleep(60)

if __name__ == "__main__":
    main()

import random
import time
import backend

def main():
    node = backend.FireBaseNode('Noise')
    while True:
        # Get noise level
        # Write your code here
        noise = 0

        # Upload to firebase
        node.val = noise
        localtime = time.asctime(time.localtime(time.time()))
        print(f'{localtime}: Noise={node.val}')

        # sleep
        time.sleep(10)

if __name__ == "__main__":
    main()

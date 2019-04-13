import time
import backend

def main():
    node = backend.FireBaseNode('NumberOfPeople', mode='a')
    while True:
        # Write your code here
        num_people = 0

        # Upload to firebase
        node.append(num_people)
        localtime = time.asctime(time.localtime(time.time()))
        print(f'{localtime}: NumberOfPeople={num_people}')

        # sleep
        time.sleep(60)

if __name__ == "__main__":
    main()

from PIL import Image as PImage
from IPython.display import display
from pprint import pprint
import os
import time
from tqdm import tqdm
import numpy as np
import time
import cv2
print(cv2.__version__)

import backend

# define current working directory path
cwd = os.getcwd()
print(cwd)

# define the path of incoming photos to be analysed
path = f'{cwd}/counter/images/photos'

# load HAAR cascade classifier
headshoulder_cascade = cv2.CascadeClassifier(f'{cwd}/counter/reference/HS.xml')

# define global variables
files = []
images_path = []
background = []
count_dict = {}


def count_people(background, frame, index):

    diff = cv2.absdiff(background, frame)

    # detect people in the image using the classifier with 2 sets of parameters
    headshoulder_rects = headshoulder_cascade.detectMultiScale(
        diff, scaleFactor=1.05, minNeighbors=4, flags=cv2.CASCADE_SCALE_IMAGE)
    headshoulder_rects_2 = headshoulder_cascade.detectMultiScale(
        diff, scaleFactor=1.02, minNeighbors=6, flags=cv2.CASCADE_SCALE_IMAGE)

    # draw the bounding boxes
    for (x, y, w, h) in headshoulder_rects:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
    for (x, y, w, h) in headshoulder_rects_2:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # overlay text, Count: #number
    cv2.putText(frame, "Count: " + str(len(headshoulder_rects)), (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 3, cv2.LINE_AA)
    cv2.putText(frame, "Count: " + str(len(headshoulder_rects_2)), (10, 110),
                cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 3, cv2.LINE_AA)

    save_im(
        frame, f'{images_path[index]}.jpg'.replace('/photos/',
                                                   '/photos_old_cv/').replace(
                                                       'jpg', 'cv.jpg'))

    # output the average count
    return (len(headshoulder_rects) + len(headshoulder_rects_2)) / 2


# code to display image in jupyter notebook during debugging
def dis_im(img):
    try:
        display(PImage.fromarray(img))
    except AttributeError:
        pass


# code to save image to folder
def save_im(img, path):
    cv2.imwrite(f"{path}", img)


# takes in path to an image folder, parse full image path, output as list
def get_images_path(path):
    global files, images_path

    files = os.listdir(f'{path}')
    files.sort()

    files = [file.rstrip('.jpg') for file in files if file.endswith('0.jpg')]
    images_path = [f'{path}/{file}' for file in files]
    return files, images_path


# append current count to a dictionary
def append_dict(file, count):
    global count_dict
    count_dict[file] = count
    return True


# update background if the last 2 readings have no people
def update_background(index):
    global background
    for i in list(count_dict.values())[-2:]:
        if i != 0:
            return False
    index = 0 if index - 1 < 0 else index - 1
    background = cv2.imread(f'{images_path[index]}.jpg')
    save_im(
        background, f'{images_path[index]}_background.jpg'.replace(
            '/photos/', '/photos_old_cv/'))
    print(f'updated background to {files[index]}')
    return True


def count_people_now(timestamp, path):
    get_images_path(path)

    counted = False
    timestamp = str(timestamp)

    # keep looping until the timestamp file appears and is counted
    while not counted:
        if str(timestamp) in files:
            index = files.index(
                timestamp)  # get the index of the current timestamp
            update_background(index)  # update background if necessary
            frame = cv2.imread(
                f'{images_path[index]}.jpg')  # load frame to opencv object
            count = count_people(background, frame,
                                 index)  # call count people cv
            append_dict(timestamp,
                        count)  # append the count to local dictionary
            counted = True
            return count
        else:
            time.sleep(1)
            get_images_path(path)


def main():
    node = backend.FireBaseNode('NumberOfPeople', mode='a')
    while True:
        t_ls, i_ls = get_images_path(path)
        print(t_ls, i_ls)

        for timestamp in tqdm(t_ls):
            try:
                num_people = count_people_now(timestamp, path)
            except Exception as e:
                print(e)
                print(timestamp)
                # input("Press anykey to continue")
                num_people = 0

            # upload to firebase
            node.append(num_people, timestamp=timestamp)
            localtime = time.strftime('%Y-%m-%d %a %H:%M:%S',
                                      time.localtime(int(timestamp)))
            print(f'{localtime}: NumberOfPeople={num_people}')


if __name__ == "__main__":
    main()
import sys, os
import time

import cv2

from collections import deque
from PIL import Image as PImage
from IPython.display import display
from pprint import pprint
from tqdm import tqdm
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import backend

# check opencv has been successfully imported
print(cv2.__version__)

# define current working directory path
cwd = os.getcwd()
print(cwd)

# define the path of incoming photos to be analysed
path = f"{cwd}/counter/images/photos"

# load HAAR cascade classifier
headshoulder_cascade = cv2.CascadeClassifier(f"{cwd}/counter/reference/HS.xml")

# define global variables
files = []
images_path = []
background = []
count_dict = {}


def count_people(background, frame, index):
    """Counts the number of people in a frame using 2 HAAR Cascade classifiers, saves analysed photo to a folder.

    Args:
        background frame: cv2 object containing the background.
        frame: cv2 object of the new frame.
        index: The current index of the frame, for saving the analysed photo to a folder.

    Returns:
        The number of people in the given frame in float, as an average of 2 classifiers.

    """

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
        frame,
        f"{images_path[index]}.jpg".replace("/photos/", "/photos_cv/").replace(
            "jpg", "cv.jpg"),
    )

    # output the average count
    return (len(headshoulder_rects) + len(headshoulder_rects_2)) / 2


def dis_im(img):
    """Display image in jupyter notebook during debugging.

    Args:
        img: Image file in the form of numpy array.

    Returns:
        None

    """
    try:
        display(PImage.fromarray(img))
    except AttributeError:
        pass


def save_im(img, path):
    """Saves cv image to a given path.

    Args:
        img: Image file in the form of numpy array.
        path: The exact path of the folder for the image to be saved to.

    Returns:
        The number of people in the given frame in float, as an average of 2 classifiers.

    """
    cv2.imwrite(f"{path}", img)


def get_images_path(path):
    """Parses the full image path, given the relative path. Outputs as a list.

    Args:
        path: The relative path of the folder containing images. The images are named in unix timestamp format.
        example:
        1556076600.jpg


    Returns:
        files: The file names of the images in a list.
        ['1556076600', ...]

        images_path: The exact path of the images in a list.
        ['~/photos/1556076600.jpg', ...]

    """
    global files, images_path

    files = os.listdir(f"{path}")
    files.sort()

    files = [file.rstrip(".jpg") for file in files if file.endswith(".jpg")]
    images_path = [f"{path}/{file}" for file in files]
    return files, images_path


# append current count to a dictionary
def append_dict(file, count):
    """Appends current count (number of people) into a global dictionary

    Args:
        file: The file name of the images, also the unix timestamp

    Returns:
        None

        Modifies global count_dict
        example

        {'1556076600': 2.0}

    """

    global count_dict
    count_dict[file] = count
    return True


# update background if the last 2 readings have no people
def update_background(index):
    """Update background if the last 2 readings of global count_dict are 0.

    Args:
        global background frame: cv2 object containing the background.
        global count_dict: Dictionary containing timestamp and count as key-value pair.
        index: The current index of the frame.

    Modifies global background, set it to the second last frame.

    Returns:
        None

    """

    global background
    for i in list(count_dict.values())[-2:]:
        if i != 0:
            return None

    index = 0 if index - 1 < 0 else index - 1
    background = cv2.imread(f"{images_path[index]}.jpg")
    save_im(
        background,
        f"{images_path[index]}_background.jpg".replace("/photos/",
                                                       "/photos_cv/"),
    )
    print(f"updated background to {files[index]}")
    return None


def count_people_now(timestamp, path):
    """Counts the number of people given timestamp. If the timestamp file is not found, keep scanning.

    Args:
        timestamp: Unix timestamp of the image, also the file name
        path: The relative path of the folder containing images. The images are named in unix timestamp format.

    Updates global images_path to scan for new images
    Updates global count_dict

    Returns:
        The number of people in the given frame in float, as an average of 2 classifiers

    """

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
                f"{images_path[index]}.jpg")  # load frame to opencv object
            count = count_people(background, frame,
                                 index)  # call count people cv
            append_dict(timestamp,
                        count)  # append the count to local dictionary
            counted = True
            return count
        else:
            time.sleep(1)
            get_images_path(path)


def mean(lst):
    """Calculates the mean of a list of floats.

    Args:
        lst: List containing floats

    Returns:
        The average of the list of floats

    """

    if len(lst) == 0:
        return 0
    else:
        return sum(lst) / len(lst)


def main():
    """Calculates current number of people and updates to Firebase.

    Args:
        None

    Creates a Firebase node given the specified room
    Calls count_people_now() every minute
    Updates the number of people to Firebase

    Returns:
        None

    """

    room = "MiniTT6"
    node = backend.FireBaseNode("NumberOfPeople", room, mode="a")
    node_realtime = backend.FireBaseNode("CurrentNumberOfPeople", room)
    num_buffer = deque(maxlen=5)
    while True:
        # define timestamp
        timestamp = int(time.time() // 60 * 60)
        print(timestamp)

        # count people using CV
        num_people = count_people_now(timestamp, path)
        num_buffer.append(num_people)

        # upload to firebase
        node.append(num_people, timestamp=timestamp)
        node_realtime.val = int(mean(num_buffer))
        localtime = time.strftime("%Y-%m-%d %a %H:%M:%S",
                                  time.localtime(int(timestamp)))
        print(f"{localtime}: NumberOfPeople={num_people}")


if __name__ == "__main__":
    main()
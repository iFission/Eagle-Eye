#%%
from PIL import Image as PImage
from IPython.display import display
from pprint import pprint
import os
import time
from tqdm import tqdm

#%%

import numpy as np
import cv2
from imutils.object_detection import non_max_suppression
print(cv2.__version__)

cwd = os.getcwd()
print(cwd)

headshoulder_cascade = cv2.CascadeClassifier(f'{cwd}/counter/reference/HS.xml')


def count_people(background, frame):

    # dis_im(background)
    # dis_im(frame)
    diff = cv2.absdiff(background, frame)
    # dis_im(diff)
    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # frame = imutils.resize(frame, width=min(400, frame.shape[1]))
    # dis_im(frame)

    # detect people in the image
    headshoulder_rects = headshoulder_cascade.detectMultiScale(
        diff, scaleFactor=1.05, minNeighbors=4, flags=cv2.CASCADE_SCALE_IMAGE)
    headshoulder_rects_2 = headshoulder_cascade.detectMultiScale(
        diff, scaleFactor=1.02, minNeighbors=6, flags=cv2.CASCADE_SCALE_IMAGE)

    # draw the original bounding boxes
    for (x, y, w, h) in headshoulder_rects:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
    for (x, y, w, h) in headshoulder_rects_2:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # non-max supression combines multiple, overlapping bounding boxes to a single bounding box
    # apply non-maxima suppression to the bounding boxes using a
    # fairly large overlap threshold to try to maintain overlapping
    # boxes that are still people
    # rects1 = np.array([[x, y, x + w, y + h] for (x, y, w, h) in headshoulder_rects])
    # rects2 = np.array([[x, y, x + w, y + h] for (x, y, w, h) in upperbody_rects])
    # rects = np.vstack((rects1, rects2))
    # pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)
    # pick = headshoulder_rects

    # # draw the final bounding boxes
    # for (xA, yA, xB, yB) in pick:
    #     cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 2)

    # overlay text, Count: #number
    cv2.putText(frame, "Count: " + str(len(headshoulder_rects)), (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 3, cv2.LINE_AA)
    cv2.putText(frame, "Count: " + str(len(headshoulder_rects_2)), (10, 110),
                cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 3, cv2.LINE_AA)
    # dis_im(diff)
    # dis_im(frame)
    # save_im(frame, path)
    return (len(headshoulder_rects) + len(headshoulder_rects_2)) / 2


def dis_im(img):
    try:
        display(PImage.fromarray(img))
    except AttributeError:
        pass


#%%
def save_im(img, path):
    cv2.imwrite(f"{path.replace('jpg', 'cv.jpg')}", img)


# takes in path to an image folder, parse full image path, output as list
def get_images_path(path):
    global files, images_path

    files = os.listdir(f'{path}')
    files.sort()

    files = [file.rstrip('.jpg') for file in files if file.endswith('.jpg')]
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
    dis_im(backend)
    print(f'updated background to index {index}')
    return True


#%%
# get_images_path(
#     '/Volumes/Media/Docs/Cloud/Drive/Eagle-Eye/counter/images/photo1')
# print(files, images_path)

#%%
files = []
images_path = []
background = []
count_dict = {}
#%%
# pprint(count_dict)
# dis_im(background)
# update_background()
# dis_im(background)


def count_people_now(timestamp, path):
    get_images_path(path)
    # print(files)
    counted = False
    timestamp = str(timestamp)
    while not counted:
        if str(timestamp) in files:
            index = files.index(timestamp)
            update_background(index)
            frame = cv2.imread(f'{images_path[index]}.jpg')
            # count = count_people(background, frame)
            count = count_people(background, frame)
            # print(count)
            # count = np.random.randint(0, 2)
            append_dict(timestamp, count)
            counted = True
            return count
        else:
            time.sleep(1)


# print(
#     count_people_now(
#         '/Volumes/Media/Docs/Cloud/Drive/Eagle-Eye/counter/images/photo1',
#         1554438540))
# print(count_dict)

#%%
# %time print(count_people_path('/Volumes/Media/Docs/Cloud/Drive/Eagle-Eye/counter/images/webcam_photos', 2000,2010)) # jupyter magic function, times the execution
# dict = count_people_path(
#     '/Volumes/Media/Docs/Cloud/Drive/Eagle-Eye/counter/images/photo1', 0, 3)

#%%
# print(dict)

#%%
import time

# print(int(time.time() // 60 * 60))
# print(time.asctime(time.localtime(time.time())))
#%%
import backend

path = f'{cwd}/counter/images/photos'


def main():
    node = backend.FireBaseNode('NumberOfPeople', mode='a')
    while True:
        # Write your code here
        # timestamp = int(time.time() // 60 * 60)
        t_ls, i_ls = get_images_path(path)
        print(t_ls, i_ls)

        for timestamp in tqdm(t_ls):
            try:
                num_people = count_people_now(timestamp, path)
            except Exception as e:
                print(e)
                print(timestamp)
                input("Press anykey to continue")
                num_people = 0
            # num_people = np.random.randint(0, 2)

            # Upload to firebase
            node.append(num_people, timestamp=timestamp)
            localtime = time.asctime(time.localtime(time.time()))
            # print(f'{localtime}: NumberOfPeople={num_people}')


if __name__ == "__main__":
    main()
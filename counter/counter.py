#%%
from PIL import Image as PImage
from IPython.display import display


def dis_im(img):
    display(PImage.fromarray(img))


#%%
import os


# takes in path to an image folder, parse full image path, output as list
def get_images_path(path):
    images_path = []

    files = os.listdir(f'{path}')
    files.sort()

    for file in files:
        images_path.append(f'{path}/{file}')

    return files, images_path


#%%
from tqdm import tqdm


# count the number of people, from list of image paths
def count_people_list(images_path):
    count_list = []
    for image_path in tqdm(images_path):
        count_list.append(count_people(image_path))
    return count_list


#%%
# count the number of people, from path provided
def count_people_path(path, start=0, end=-1):
    files, images_path = get_images_path(path)
    files, images_path = files[start:end], images_path[start:end]
    count_list = count_people_list(images_path)

    print(np.median(count_list))
    print(int(np.median(count_list)))

    count_dict = {}
    for file, count in zip(files, count_list):
        # print(file, count)
        count_dict[f"{file.rstrip('.jpg')}"] = count

    return count_dict


#%%
import numpy as np
import cv2
from imutils.object_detection import non_max_suppression
print(cv2.__version__)

headshoulder_cascade = cv2.CascadeClassifier('counter/reference/HS.xml')


#%%
def count_people(path):
    background = cv2.imread('counter/images/photo2/2019-04-04_1232.jpg')
    frame = cv2.imread(path)
    diff = cv2.absdiff(background, frame)
    # dis_im(diff)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

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
    dis_im(frame)
    return (len(headshoulder_rects) + len(headshoulder_rects_2)) / 2


#%%
from pprint import pprint
# %time print(count_people_path('/Volumes/Media/Docs/Cloud/Drive/Eagle-Eye/counter/images/webcam_photos', 2000,2010)) # jupyter magic function, times the execution
pprint(
    count_people_path(
        '/Volumes/Media/Docs/Cloud/Drive/Eagle-Eye/counter/images/photo2'))

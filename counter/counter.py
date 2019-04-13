#%%
from PIL import Image as PImage
from IPython.display import display


def dis_im(img):
    display(PImage.fromarray(img))


#%%
import numpy as np
import cv2
print(cv2.__version__)
import imutils
from imutils.object_detection import non_max_suppression
from imutils import paths

# initialise Histogram of Oriented Gradients descriptor
# set Support Vector Machine to be pre-trained detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())


#%%
def count_people(path):
    frame = cv2.imread(path)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # frame = imutils.resize(frame, width=min(400, frame.shape[1]))
    # dis_im(frame)

    # detect people in the image
    (rects, weights) = hog.detectMultiScale(
        frame, winStride=(4, 4), padding=(8, 8), scale=1.05)

    # draw the original bounding boxes
    for (x, y, w, h) in rects:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # non-max supression combines multiple, overlapping bounding boxes to a single bounding box
    # apply non-maxima suppression to the bounding boxes using a
    # fairly large overlap threshold to try to maintain overlapping
    # boxes that are still peoplem
    rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
    pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)

    # draw the final bounding boxes
    for (xA, yA, xB, yB) in pick:
        cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 2)

    # overlay text
    cv2.putText(frame, "Count: " + str(len(pick)), (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    dis_im(frame)
    return len(pick)


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
    count_list = count_people_list(images_path[start:end])

    count_dict = {}
    for file, count in zip(files, count_list):
        # print(file, count)
        count_dict[f"{file.rstrip('.jpg')}"] = count

    return count_dict


#%%
from pprint import pprint
# %time print(count_people_path('/Volumes/Media/Docs/Cloud/Drive/Eagle-Eye/counter/images/webcam_photos', 2000,2010)) # jupyter magic function, times the execution
pprint(
    count_people_path(
        '/Volumes/Media/Docs/Cloud/Drive/Eagle-Eye/counter/images/photo2'))
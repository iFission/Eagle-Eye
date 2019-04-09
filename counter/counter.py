#%%
import numpy as np
import cv2
print(cv2.__version__)

#%%
from matplotlib import pyplot as plt


def dis_im(img):  # display opencv image using plt
    plt.figure(figsize=(20, 20))  # show multiple images inline in jupyter
    plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
    # to convert cv's BGR to RGB, add [...,::-1]
    plt.imshow(img, cmap='gray')  # display image using plot


#%%
class Person:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.counted = False

    def updateCoords(self, newX, newY):
        self.x = newX
        self.y = newY


#%%
import imutils
from imutils.object_detection import non_max_suppression
from imutils import paths

# initialise Histogram of Oriented Gradients descriptor
# set Support Vector Machine to be pre-trained detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
#%%
background = cv2.imread('counter/photo1/background.jpg',
                        0)  # read image file in grayscale, to np array
# dis_im(background)
frame1 = cv2.imread('counter/photo1/2019-04-05_1232.jpg', 0)
# dis_im(frame1)
frame = cv2.imread('/Volumes/Media/Dls/persons/person_266.bmp')
frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
frame = imutils.resize(frame, width=min(400, frame.shape[1]))
# dis_im(frame)

# non-max supression combines multiple, overlapping bounding boxes to a single bounding box

# detect people in the image
(rects, weights) = hog.detectMultiScale(
    frame, winStride=(4, 4), padding=(8, 8), scale=1.05)

# draw the original bounding boxes
for (x, y, w, h) in rects:
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

# apply non-maxima suppression to the bounding boxes using a
# fairly large overlap threshold to try to maintain overlapping
# boxes that are still people
rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)

# draw the final bounding boxes
for (xA, yA, xB, yB) in pick:
    cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 2)

dis_im(frame)
print(len(pick))
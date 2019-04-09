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
background = cv2.imread('counter/photo1/background.jpg',
                        0)  # read image file in grayscale, to np array
# dis_im(background)
frame1 = cv2.imread('counter/photo1/2019-04-05_1232.jpg', 0)
# dis_im(frame1)
frame = cv2.imread('counter/photo1/2019-04-05_1232.jpg')
frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
# dis_im(frame)

frame_delta = cv2.absdiff(background, frame1)

# dis_im(frame_delta)
thresh = cv2.threshold(frame_delta, 200, 255, cv2.THRESH_BINARY)[1]
thresh = cv2.dilate(thresh, None, iterations=2)
# dis_im(thresh)
contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)[0]
dis_im(thresh)

print(len(contours))
ppl = 0
for c in contours:
    # dis_im(c)
    # print(c.shape)
    if cv2.contourArea(c) < 1000:  # proceed to next loop if area too small
        continue
    ppl += 1
    (x, y, w, h) = cv2.boundingRect(c)
    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
    rectagleCenterPont = ((x + x + w) // 2, (y + y + h) // 2)
    cv2.circle(frame, rectagleCenterPont, 1, (0, 0, 255), 5)
    # dis_im(frame1)

dis_im(frame)
print(ppl)
#%%

import math
import requests
import threading
import datetime
import time

from kivy.graphics import Color, Rectangle
from kivy.properties import StringProperty, NumericProperty
from kivy.core.text import Label as CoreLabel
from kivy.clock import Clock
from kivy.graphics import *
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.core.window import Window
Window.clearcolor = (0.93, 0.93, 0.93, 1)

exit_flag = False

def set_color(color):
    '''Set RGB color with corresponding given HEX color code
    Args:
        color: A string representing a HEX color code, e.g.: "#ffffff"
    '''
    
    #Convert HEX color code to RGB color code
    r = float(int(color[1:3], 16)) / 255
    g = float(int(color[3:5], 16)) / 255
    b = float(int(color[5:7], 16)) / 255
    #Set color
    Color(r, g, b)


def draw_text(text, pos, font_size, x_offset=0, y_offset=0):
    '''Draw text in canvas in kivy
    Args:
        text: A string represneting the text to be drew on the canvas
        pos: A 2 elements tuple representing the absolute (x,y) position of the text
        font_size: An integer represneting the font size of the text
        x_offset: offset of text's x coordinate
        y_offset: offset of text's y coordinate
        '''
    label = CoreLabel(text=text, font_size=font_size)
    label.refresh()
    pos = (pos[0] - label.texture.size[0]/2 + x_offset,
           pos[1] - label.texture.size[1] + y_offset)
    Rectangle(size=label.texture.size, pos=pos, texture=label.texture)


class GetValThreading(threading.Thread):
    '''Continuously get newest firebase reading for progress ring'''
    def __init__(self, progressring):
        threading.Thread.__init__(self)
        self.content = "text"
        self.progressring = progressring
        self.percentage = 0.7

    def run(self):
        while not exit_flag:
            self.volume = self.progressring.maxcapacity
            # send requests to firebase
            # build the url
            val_url = 'https://eagle-eye-c1e58.firebaseio.com/{}/{}/.json'.format(
                self.progressring.roomname, self.progressring.ringtype)
            # get response
            val = requests.get(val_url)
            if self.progressring.ringtype == "CurrentNumberOfPeople":
                if val.json() != None:
                    # update ring text
                    self.content = str(val.json()) + "/" + self.volume + "pax"
                    # update ring percentage
                    self.percentage = float(val.json())/int(self.volume)
                else:
                    # default value
                    self.content = "8/10 pax"
            elif self.progressring.ringtype == "Noise":
                if val.json() != None:
                    noise = round(math.log(val.json()), 2)
                    self.percentage = noise/5
                    if noise <= 1.6:
                        self.content = "Low"
                    elif noise <= 3:
                        self.content = "Median"
                    else:
                        self.content = "High"
                else:
                    # default value
                    self.content = "Median"
            time.sleep(1)


class ProgressRing(Widget):
    ''' Widget to draw a progress ring
    Kivy properties:
        color: color of the ring
        color_unoccupied: color of the unoccupied part of the ring
        background: background of the widget
        text: text in the middle of the ring
        percentage: a float number from 0 to 1
        roomname: roomname saved in firebase
        ringtype: "CurrentNumberOfPeople" / "Noise"
        maxcapacity: max capacity of the room
    '''
    color = StringProperty('#42a5f5')
    color_unoccupied = StringProperty('#cccccc')
    background = StringProperty('#ffffff')
    text = StringProperty('Hello')
    percentage = NumericProperty(0.7)
    roomname = StringProperty('Location')
    ringtype = StringProperty('CurrentNumberOfPeople')
    maxcapacity = StringProperty('6')

    def __init__(self, **kwargs):
        Widget.__init__(self)
        # bind related properties to update_canvas
        # so it will redraw when property changes
        self.bind(pos=self.update_canvas, size=self.update_canvas)
        self.bind(text=self.update_canvas)
        self.bind(percentage=self.update_canvas)
        self.getvalthreading = GetValThreading(self)
        # start a new thread to get firebase reading at background
        self.getvalthreading.start()
        # refresh text and percentage every 3 seconds
        Clock.schedule_interval(self.text_percentage_update, 3)

    def text_percentage_update(self, *kwargs):
        ''' Read from firebase thread and update text and percontage  '''
        self.text = str(self.getvalthreading.content)
        self.percentage = self.getvalthreading.percentage

    def _center(self, diameter):
        ''' Get the lower left point of a ring in the middle of the widget '''
        return self.pos[0] + self.size[0]/2 - diameter/2, self.pos[1] + self.size[1]/2 - diameter/2

    def update_canvas(self, *args):
        ''' draw progress ring on the canvas of the widget '''
        diameter = min(self.size) * 1
        with self.canvas:
            # clear canvas
            self.canvas.clear()
            # draw background
            set_color(self.background)
            Rectangle(pos=self.pos, size=self.size)

            # draw the ring
            set_color(self.color_unoccupied)
            Ellipse(pos=self._center(diameter), size=(diameter, diameter))

            # only draw the occupied part when percentage is not 0
            if self.percentage > 0.001:
                set_color(self.color)
                Ellipse(pos=self._center(diameter), size=(
                    diameter, diameter), angle_end=self.percentage*360)

            set_color(self.background)
            d = diameter * 0.85
            Ellipse(pos=self._center(d), size=(d, d))

            # draw the smaller ring inside
            set_color(self.color_unoccupied)
            d = diameter * 0.8
            Ellipse(pos=self._center(d), size=(d, d))

            set_color(self.background)
            d -= 5
            Ellipse(pos=self._center(d), size=(d, d))

            # draw text in the middle
            set_color('#000000')
            draw_text(self.text, self._center(0), 40, y_offset=20)


class GetPredictionThreading(threading.Thread):
    '''Continuously get newest firebase reading for histogram view'''
    def __init__(self, histogram):
        threading.Thread.__init__(self)
        self.histogram = histogram
        # default value
        self.prediction = [3, 3, 5, 0, 0, 0, 0, 0, 3,
                           0, 5, 6, 5, 5, 4, 5, 6, 7, 8, 6, 5, 4, 3, 5]

    def run(self):
        while not exit_flag:
            week = {0: "Monday", 1: "Tuesday", 2: "Wednesday",
                    3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}
            # get current weekday
            today = datetime.datetime.today().weekday()
            self.day = week[today]
            # build requests
            url = 'https://eagle-eye-c1e58.firebaseio.com/{}/Prediction/{}/.json'.format(
                self.histogram.roomname, self.day)
            # get response from firebase
            predict_dict = requests.get(url).json()
            if predict_dict != None:
                self.prediction = predict_dict
            time.sleep(1)


class HistogramView(Widget):
    ''' Widget to show histogram graph
    Kivy property:
        roomname: a string property refer to the name saved in firebase
     '''
    roomname = StringProperty('Location')

    def __init__(self, **kwargs):
        Widget.__init__(self)
        self.bind(pos=self.update_canvas, size=self.update_canvas)

        # inits default value for drawing
        current_hour = datetime.datetime.now().hour
        self.x_list = list(range(24))
        self.y_list = [1 for _ in self.x_list]
        self.x_label = ["{}{}".format(
            (x - 1) % 12 + 1, 'a' if x < 12 else 'p') if x % 3 == 0 else None for x in self.x_list]
        self.x_color = ['#f06292' if x ==
                        current_hour else '#42a5f5' for x in self.x_list]
        # launch background thread to get firebase value
        self.getpredictionthreading = GetPredictionThreading(self)
        self.getpredictionthreading.start()
        # schedule kivy to update the view every 5 seconds
        Clock.schedule_interval(self.update_prediction, 5)

    def update_prediction(self, *args):
        ''' Update y_list from firebase'''
        self.y_list = self.getpredictionthreading.prediction
        self.update_canvas() # refresh the graph

    def update_canvas(self, *args):
        # find the minimum and maximum value for giving list
        # so later can map it to full widget
        x_min, x_max = min(self.x_list), max(self.x_list)
        y_min, y_max = 0, max(self.y_list)
        
        # map value in list to coordinates on screen
        x = [float((x - x_min)) / (x_max - x_min) *
             self.size[0] + self.pos[0] for x in self.x_list]
        y = [float((y - y_min)) / (y_max - y_min) * 1 * self.size[1]
             for y in self.y_list]

        with self.canvas:
            # clear canvas
            self.canvas.clear()
            # set background
            set_color('#ffffff')
            Rectangle(pos=self.pos, size=self.size)

            shift = 20 # shift of the whole graph in y direction in pixels
            gap = 2 # gap between columns
            for i in range(1, len(x)):
                # draw column
                set_color(self.x_color[i])
                Rectangle(pos=(x[i-1] + gap/2, shift + self.pos[1]),
                          size=(x[i]-x[i-1] - gap, y[i]))
                set_color('#777777')
                mid_x = (x[i-1]+x[i])/2
                # draw short vertical line below
                Line(points=[mid_x, shift + self.pos[1], mid_x, shift - 3 + self.pos[1]
                             if self.x_label[i] is None else shift - 5 + self.pos[1]], width=1)
                # draw text
                if self.x_label[i] is not None:
                    draw_text(self.x_label[i], pos=(
                        mid_x, shift - 5 + self.pos[1]), font_size=30)
            # draw horizontal line below
            set_color('#777777')
            Line(points=[self.pos[0], shift + self.pos[1],
                         self.pos[0]+self.size[0], shift + self.pos[1]], width=1)


#Load file "main.kv" about the UI of the 5 screens 
Builder.load_file("main.kv")

#Create 5 screens including 1 menuscreen and 4 screen for every building
class MenuScreen(Screen):
    pass


class BD2(Screen):
    pass


class Blk_55(Screen):
    pass


class Blk_57(Screen):
    pass


class Blk_59(Screen):
    pass


# Create the screen manager
sm = ScreenManager()
# Add all screens to the screen manager
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(BD2(name='Building2'))
sm.add_widget(Blk_55(name='Block_55'))
sm.add_widget(Blk_57(name='Block_57'))
sm.add_widget(Blk_59(name='Block_59'))


class TestApp(App):

    def build(self):
        return sm


try:
    if __name__ == '__main__':
        TestApp().run()
finally:
    # set exit_flag
    # so all subprocess can exit
    exit_flag = True

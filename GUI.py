from kivy.config import Config
Config.set('graphics', 'width', '700')
Config.set('graphics', 'height', '200')
Config.write()

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.properties import BooleanProperty, StringProperty
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
import sys
import datetime
import random
import numpy as np



######
# How to use?
# ===========
#
# start script like: python timer.py 5m
# This will set the timer to 5minutes.
#
# Syntax: timer.py <minutes>m
######

__alphabet__ = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L",
                "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X",
                "Y", "Z"]

__codes__ = [203, 529, 394, 481, 839, 576, 416, 729, 495, 582, 227, 605, 
             656, 535, 811, 878, 204, 822, 316, 763, 117, 884, 777, 766, 
             601, 787]

def code_is_correct(letter, code):
    if letter in __alphabet__ and code in __codes__:
        return __alphabet__.index(letter) == __codes__.index(code)
    return False

def select_random_letter(size):
    assert size > 0 and size <= 26
    selection = np.random.choice(__alphabet__[:size])
    return selection

def get_random_time():
    return random.randint(30, 60)

"""
<MainLayout>
    button: button
    Button:
        id: button
        on_press: root.toggle() 
    GridLayout:
        rows: 2
        cols: 2
    
"""

Builder.load_string("""
<MainLayout>:
    rows: 3
    cols: 2
    Label:
        text: "Timer: "
        font_size: 30
    Label:
        text: "%s:%s" % (root.minutes, root.seconds)
        font_size: 30
    Label:
        text: "Enter code for %s: " % root.letter
        font_size: 30
    TextInput:
        on_text_validate: root.send_entry(args[0])
        multiline: False
    Label:
        text: "Explosions: "
        font_size: 30
    Label:
        text: "%s" % root.nb_explosions
        font_size: 30
""")


class MainLayout(GridLayout):
    minutes = StringProperty()
    seconds = StringProperty()
    running = BooleanProperty(False)
    #config  = CountdownPuzzleConfig()
    letter  = StringProperty("A")
    nb_explosions = StringProperty("0")

    def __init__(self, **kwargs):
        super(MainLayout, self).__init__(**kwargs)
        #self.sound = SoundLoader.load('bell.wav')
        self.deadline = datetime.datetime.now()+datetime.timedelta(0, get_random_time())
        self.group_size = kwargs['group_size'] # from kwargs
        self.letter = select_random_letter(self.group_size)
        #self.letter = letter # from kwargs
        
        self.update()
        self.start()
        

    def start(self):
        if not self.running:
            print("Start called successfully")
            self.running = True
            Clock.schedule_interval(self.update, 0.05)

    def stop(self):
        if self.running:
            print("Stop called")
            self.running = False
            Clock.unschedule(self.update)

    def update(self, *kwargs):
        time_left = self.deadline - datetime.datetime.now()
        self.minutes, seconds = str(time_left).split(":")[1:]
        self.seconds = seconds[:5]

        if int(self.minutes) == 0:
            if int(self.seconds.split(".")[0]) == 0:
                if int(self.seconds.split(".")[1]) < 20:
                    self.seconds = "00.00"
                
                    self.nb_explosions = str(int(self.nb_explosions) + 1)
                    # Refresh timer

                    self.stop()
                    self.deadline = datetime.datetime.now()+datetime.timedelta(0, get_random_time())
                    self.letter = select_random_letter(self.group_size)
                    self.update()
                    self.start()

    def toggle(self):
        if self.running:
            self.stop()
        else:
            self.start()

    def send_entry(self, code):
        code = code.text
        print("Send entry! entered %s" % str(code))

        if code.isdigit():
            code = int(code)
            correct = code_is_correct(self.letter, code)
            print("the code was correct: %s" % str(correct))
            time_is_low = float(self.seconds) < 10.
            print("Time is low: %s" % str(time_is_low))

            if correct and time_is_low: 
                print("The clock is running, ", self.running)
                self.stop()
                self.deadline = datetime.datetime.now()+datetime.timedelta(0, get_random_time())
                self.letter = select_random_letter(self.group_size)
                self.update()
                self.start()
        else:
            print("Nope not an int")



def get_number_students():
    while True:
        size = input("How many people in the group? (1-26): ")
        if type(size) is not int:
            continue
        if size > 26 or size < 1:
            continue
        break
    return size


if __name__ == '__main__':
    
    size = get_number_students()

    class TimerApp(App):
        def build(self):
            self.layout = MainLayout(group_size=size)
            return self.layout
                

    TimerApp().run()

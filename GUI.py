from kivy.config import Config
Config.set('graphics', 'width', '700')
Config.set('graphics', 'height', '200')
Config.write()

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
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

from countdown_puzzle import CountdownPuzzleConfig


######
# How to use?
# ===========
#
# start script like: python timer.py 5m
# This will set the timer to 5minutes.
#
# Syntax: timer.py <minutes>m
######


def get_random_time():
    return random.randint(30, 120)/60
countdown = get_random_time

Builder.load_string("""
<MainLayout>:
    button: button
    Button:
        id: button
        on_press: root.toggle()
    AnchorLayout:
        Label:
            text: "%s:%s" % (root.minutes, root.seconds)
            font_size: 120
""")


class MainLayout(FloatLayout):
    minutes = StringProperty()
    seconds = StringProperty()
    running = BooleanProperty(False)
    config  = CountdownPuzzleConfig()

    def __init__(self, **kwargs):
        super(MainLayout, self).__init__(**kwargs)
        self.sound = SoundLoader.load('bell.wav')
        self.delta = datetime.datetime.now()+datetime.timedelta(0, 60*countdown())
        self.update()
        

    def start(self):
        if not self.running:
            self.running = True
            Clock.schedule_interval(self.update, 0.05)

    def stop(self):
        if self.running:
            self.running = False
            Clock.unschedule(self.update)

    def update(self, *kwargs):
        delta = self.delta - datetime.datetime.now()
        self.minutes, seconds = str(delta).split(":")[1:]
        self.seconds = seconds[:5]
	
        if int(self.minutes) == 0:
            if int(self.seconds.split(".")[0]) == 0:
                if int(self.seconds.split(".")[1]) < 20:
                    self.seconds = "00.00"
                    self.button.background_color = (1,0,0,1)
                    self.sound.play()
                    self.stop()

    def toggle(self):
        if self.running:
            #self.stop()
            pass
        else:
            self.start()

if __name__ == '__main__':
    size = int(input("How many people in the group? (1-26):"))

    class TimerApp(App):
        def build(self):
            self.config = CountdownPuzzleConfig()

            self.layout = MainLayout()
            self.group_size = size
            
            self.letter = config.select_random_letter(self.group_size)

            self.prompt_label = Label(text="Enter the code for %s:" % self.letter)
            self.layout.add_widget(prompt_label)

            self.txt = TextInput(text='', multiline=False)
            self.layout.add_widget(txt)

            self.confirm_button = Button("Enter")
            self.confirm_button.bind(on_press=self.send_entry)
            self.layout.add_widget(confirm_button)

            return self.layout
        
        def send_entry(self, button):
            self.entered_code = self.txt.text
            if self.entered_code.isdigit():
                code = int(self.entered_code)
                correct = self.config.code_is_correct(self.letter, code)

                if correct: 
                    self.delta = datetime.datetime.now()+datetime.timedelta(0, 60*countdown())
                    self.layout.update()
                    

    TimerApp().run()

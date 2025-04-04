from kivy.app import App
from kivy.lang import Builder
from kivy.config import Config
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.slider import Slider
from kivy.factory import Factory
from kivy.clock import Clock

from mediaplayer import MediaPlayer
from carplay_window import CarplayScreen
from reverse_window import ReverseScreen

#from obd_data import get_obd2_rpm

# Builder.load_file('progressbar.kv')

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        reverse_cam_btn = Factory.RoundedButton(text="Reverse Camera",
                            size_hint=(0.3, 0.1),
                            pos_hint={'center_x': 0.5, 'center_y': 0.8})
        reverse_cam_btn.bind(on_press=self.open_reverse_cam)
        self.add_widget(reverse_cam_btn)

#        carplay_btn = Factory.RoundedButton(text="Carplay - UNDER DEVELOPMENT", 
#                            size_hint=(0.3, 0.1), 
#                            pos_hint={'center_x': 0.5, 'center_y': 0.65})
#        carplay_btn.bind(on_press=self.carplayMode)
#        self.add_widget(carplay_btn)

        open_btn = Factory.RoundedButton(text="Idle Mode - UNDER DEVELOPMENT", 
                            size_hint=(0.3, 0.1), 
                            pos_hint={'center_x': 0.5, 'center_y': 0.65})
        open_btn.bind(on_press=self.go_to_info_screen)
        self.add_widget(open_btn)

        airplay_media_btn = Factory.RoundedButton(text="Airplay Media - UNDER DEVELOPMENT",
                            size_hint=(0.3, 0.1),
                            pos_hint={'center_x': 0.5, 'center_y': 0.5})
        airplay_media_btn.bind(on_press=self.open_airplay_media)
        self.add_widget(airplay_media_btn)

        close_btn = Factory.CloseButton(text="Exit Program", 
                            size_hint=(0.3, 0.1), 
                            pos_hint={'center_x': 0.5, 'center_y': 0.2})
        close_btn.bind(on_press=self.close_program)
        self.add_widget(close_btn)

    def carplayMode(self, *args):
        self.manager.current = 'carplay'
        
    def go_to_info_screen(self, *args):
        self.manager.current = 'info'

    def go_to_sport_screen(self, *args):
        self.manager.current = 'track'

    def open_reverse_cam(self, *args):
        self.manager.current = 'reverse'

    def open_airplay_media(self, *args):
        self.manager.current = 'mediaplayer'

    def close_program(self, *args):
        App.get_running_app().stop()

class InfoScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        label = Label(text="Idle Mode - UNDER DEVELOPMENT", pos_hint={'center_x': 0.5, 'center_y': 0.9})
        
        back_btn = Factory.CloseButton(text="Back", size_hint=(0.3, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.2})
        back_btn.bind(on_press=self.go_back)
        
        self.add_widget(label)
        self.add_widget(back_btn)

    def go_back(self, *args):
        self.manager.current = 'main'


class TrackScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        label = Label(text="Track Mode", 
                      pos_hint={'center_x': 0.5, 'center_y': 0.9})

        self.progress_bar = ProgressBar(max=100, value=50, size_hint=(0.6, 10), pos_hint={'center_x': 0.5, 'center_y': 0.7})
        
        slider = Slider(min=0, max=100, value=50, size_hint=(0.6, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.6})
        slider.bind(value=self.update_progress)

        self.rpm_bar = ProgressBar(max=100, value=50, size_hint=(0.6, 10), pos_hint={'center_x': 0.5, 'center_y': 0.5})


        back_btn = Factory.CloseButton(text="Back", size_hint=(0.3, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.2})
        back_btn.bind(on_press=self.go_back)

        self.add_widget(label)
        self.add_widget(self.progress_bar)  # Add the ProgressBar to the screen
        self.add_widget(slider)
        #self.add_widget(self.rpm_bar)
        self.add_widget(back_btn)

        Clock.schedule_interval(self.update_progress_obd, 0.5)
        
    def go_back(self, *args):
        Clock.unschedule(self.update_progress_obd)
        self.manager.current = 'main'
    
    def update_progress_obd(self, dt):
        #obd2_RPM = get_obd2_rpm()

        self.rpm_bar.value = 0

    def update_progress(self, instance, value):
        self.progress_bar.value = value

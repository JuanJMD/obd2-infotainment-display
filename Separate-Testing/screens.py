from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.slider import Slider
import os
import subprocess
from kivy.factory import Factory

import cv2
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
from kivy.clock import Clock

from obd_data import get_obd2_rpm



class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        carplay_btn = Factory.RoundedButton(text="Carplay", 
                                            size_hint=(0.3, 0.1), 
                                            pos_hint={'center_x': 0.5, 'center_y': 0.65})
        
        carplay_btn.bind(on_press=self.carplayMode)
        self.add_widget(carplay_btn)

        open_btn = Factory.RoundedButton(text="Car Data", 
                          size_hint=(0.3, 0.1), 
                          pos_hint={'center_x': 0.5, 'center_y': 0.5})
        open_btn.bind(on_press=self.go_to_info_screen)
        self.add_widget(open_btn)

        track_btn = Factory.RoundedButton(text="Track Mode", 
                           size_hint=(0.3, 0.1), 
                           pos_hint={'center_x': 0.5, 'center_y': 0.35})
        track_btn.bind(on_press=self.go_to_sport_screen)
        self.add_widget(track_btn)

        reverse_cam_btn = Factory.RoundedButton(text="Reverse Camera",
                                 size_hint=(0.3, 0.1),
                                 pos_hint={'center_x': 0.5, 'center_y': 0.8})
        reverse_cam_btn.bind(on_press=self.open_reverse_cam)
        self.add_widget(reverse_cam_btn)

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

    def close_program(self, *args):
        App.get_running_app().stop()

class CarplayScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        label = Label(text="Carplay Mode", pos_hint={'center_x': 0.5, 'center_y': 0.9})
        self.add_widget(label)

        carplay_btn = Button(text="Carplay", size_hint=(0.3, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.65})
        carplay_btn.bind(on_press=self.carplayMode)
        self.add_widget(carplay_btn)

        back_btn = Factory.CloseButton(text="Back", size_hint=(0.3, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.2})
        back_btn.bind(on_press=self.go_back)
        self.add_widget(back_btn)

    def carplayMode(self, *args):
        carplay_options_layout = BoxLayout(orientation='vertical')
        openCarplay_button = Button(text='Launch Carplay (Beta)')
        openCarplay_button.bind(on_press=self.openFile)
        carplay_options_layout.add_widget(openCarplay_button)

        no_launch_button = Button(text='Return to Main Menu')
        no_launch_button.bind(on_press=lambda x: self.carplay_popup.dismiss())
        carplay_options_layout.add_widget(no_launch_button)

        self.carplay_popup = Popup(title='LAUNCHING CARPLAY (WARNING)',
                            content=carplay_options_layout,
                            size_hint=(None, None),
                            size=(600, 400))
        self.carplay_popup.open()
    
    def openFile(self, instance):
        filePath = os.path.join('/home', 'jnito', 'Desktop', 'Carplay.AppImage')
        # subprocess.run([filePath], check=True)
        subprocess.Popen([filePath])

    def go_back(self, *args):
        self.manager.current = 'main'

class InfoScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        label = Label(text="This is the info screen", pos_hint={'center_x': 0.5, 'center_y': 0.9})
        
        back_btn = Factory.CloseButton(text="Back", size_hint=(0.3, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.2})
        back_btn.bind(on_press=self.go_back)
        
        self.add_widget(label)
        self.add_widget(back_btn)

    def go_back(self, *args):
        self.manager.current = 'main'


Builder.load_file('progressbar.kv')

class TrackScreen(Screen):
    def __init__(self, **kwargs):
    
        super().__init__(**kwargs)
        label = Label(text="Track Mode", pos_hint={'center_x': 0.5, 'center_y': 0.9})
        back_btn = Factory.CloseButton(text="Back", size_hint=(0.3, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.2})
        back_btn.bind(on_press=self.go_back)

        self.progress_bar = ProgressBar(max=100, value=50, size_hint=(0.6, 10), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.rpm_bar = ProgressBar(max=100, value=50, size_hint=(0.6, 10), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        

        slider = Slider(min=0, max=100, value=50, size_hint=(0.6, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.4})
        slider.bind(value=self.update_progress)

        self.add_widget(label)
        self.add_widget(self.progress_bar)  # Add the ProgressBar to the screen
        self.add_widget(slider)
        self.add_widget(self.rpm_bar)
        self.add_widget(back_btn)

        Clock.schedule_interval(self.update_progress_obd, 0.5)
        
    def go_back(self, *args):
        Clock.unschedule(self.update_progress_obd)
        self.manager.current = 'main'
    
    def update_progress_obd(self, dt):
        obd2_RPM = get_obd2_rpm()

        self.rpm_bar.value = obd2_RPM

    def update_progress(self, instance, value):
        self.progress_bar.value = value

class ReverseScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        label = Label(text="Reverse Camera", pos_hint={'center_x': 0.5, 'center_y': 0.9})
        back_btn = Factory.CloseButton(text="Back", size_hint=(0.3, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.2})
        back_btn.bind(on_press=self.go_back)

        self.image = Image()

        self.add_widget(label)
        self.add_widget(self.image)
        self.add_widget(back_btn)

    def update(self, dt):
        ret, frame = self.capture.read()

        if ret:
            # convert it to texture
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tostring()
            image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            # display image from the texture
            self.image.texture = image_texture

    def on_enter(self, *args):
        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.update, 1.0/120.0)

    def go_back(self, *args):
        self.capture.release()
        self.manager.current = 'main'

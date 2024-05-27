from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config
from kivy.uix.popup import Popup
from kivy.uix.camera import Camera
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
import os
import time
import subprocess


Config.set('graphics', 'fullscreen', 'auto')
Config.set('kivy', 'window_icon', '')
Config.set('kivy', 'desktop', 1)
Config.set('graphics', 'borderless', 1)

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        carplay_btn = Button(text="Carplay", 
                             size_hint=(0.3, 0.1), 
                             pos_hint={'center_x': 0.5, 'center_y': 0.65})
        carplay_btn.bind(on_press=self.carplayMode)
        self.add_widget(carplay_btn)

        open_btn = Button(text="Car Data", 
                          size_hint=(0.3, 0.1), 
                          pos_hint={'center_x': 0.5, 'center_y': 0.5})
        open_btn.bind(on_press=self.go_to_info_screen)
        self.add_widget(open_btn)

        track_btn = Button(text="Sport Mode", 
                           size_hint=(0.3, 0.1), 
                           pos_hint={'center_x': 0.5, 'center_y': 0.35})
        track_btn.bind(on_press=self.go_to_sport_screen)
        self.add_widget(track_btn)

        reverse_cam_btn = Button(text="Reverse Camera",
                                 size_hint=(0.3, 0.1),
                                 pos_hint={'center_x': 0.5, 'center_y': 0.8})
        reverse_cam_btn.bind(on_press=self.open_reverse_cam)
        self.add_widget(reverse_cam_btn)

        close_btn = Button(text="Exit Program", 
                           size_hint=(0.3, 0.1), 
                           pos_hint={'center_x': 0.5, 'center_y': 0.2},
                           background_color=(1, 0, 0, 1))
        close_btn.bind(on_press=self.close_program)
        self.add_widget(close_btn)


    def carplayMode(self, *args):
        self.manager.current = 'carplay'
        
    def go_to_info_screen(self, *args):
        self.manager.current = 'info'

    def go_to_sport_screen(self, *args):
        self.manager.current = 'sport'

    def open_reverse_cam(self, *args):
        self.manager.current = 'reverse'

    def close_program(self, *args):
        App.get_running_app().stop()

class carplayScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        label = Label(text="Carplay Mode", pos_hint={'center_x': 0.5, 'center_y': 0.9})
        self.add_widget(label)

        carplay_btn = Button(text="Carplay", size_hint=(0.3, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.65})
        carplay_btn.bind(on_press=self.carplayMode)
        self.add_widget(carplay_btn)

        
        back_btn = Button(text="Back", size_hint=(0.3, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.4})
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
        
        back_btn = Button(text="Back", size_hint=(0.3, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.4})
        back_btn.bind(on_press=self.go_back)
        
        self.add_widget(label)
        self.add_widget(back_btn)

    def go_back(self, *args):
        self.manager.current = 'main'

class sportScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        label = Label(text="Track Mode", pos_hint={'center_x': 0.5, 'center_y': 0.9})
        back_btn = Button(text="Back", size_hint=(0.3, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.4})
        back_btn.bind(on_press=self.go_back)

        self.add_widget(label)
        self.add_widget(back_btn)

    def go_back(self, *args):
        self.manager.current = 'main'


import cv2
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
from kivy.clock import Clock

class reverseScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        label = Label(text="Reverse Camera", pos_hint={'center_x': 0.5, 'center_y': 0.9})
        back_btn = Button(text="Back", size_hint=(0.3, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.4})
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
        Clock.schedule_interval(self.update, 1.0/60.0)

    def go_back(self, *args):
        self.capture.release()
        self.manager.current = 'main'

# class reverseScreen(Screen):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         label = Label(text="Reverse Camera", pos_hint={'center_x': 0.5, 'center_y': 0.9})
#         back_btn = Button(text="Back", size_hint=(0.3, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.4})
#         back_btn.bind(on_press=self.go_back)
# 
# 
# 
#         self.add_widget(label)
#         self.add_widget(back_btn)
# 
#     def go_back(self, *args):
#         self.manager.current = 'main'

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(carplayScreen(name='carplay'))
        sm.add_widget(InfoScreen(name='info'))
        sm.add_widget(sportScreen(name='sport'))
        sm.add_widget(reverseScreen(name='reverse'))
        return sm

if __name__ == '__main__':
    MyApp().run()

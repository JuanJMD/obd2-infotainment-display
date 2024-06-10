
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
import os
import subprocess
from kivy.factory import Factory

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
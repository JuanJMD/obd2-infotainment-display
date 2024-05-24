from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import os
import subprocess

class MyApp(App):
    def build(self):
        main_layout = BoxLayout(orientation='vertical')

        launch_carplay = Button(text='Launch Carplay',
                                background_color=(.2, .2, .2, 1))
        launch_carplay.bind(on_press=self.carplayWarning)
        main_layout.add_widget(launch_carplay)

        open_popup_button = Button(text='Launch Car Data',
                                background_color=(.2, .2, .2, 1))
        open_popup_button.bind(on_press=self.open_popup)
        main_layout.add_widget(open_popup_button)

        close_window_button = Button(text='Close Window',
                                background_color=(.2, .2, .2, 1))
        close_window_button.bind(on_press=self.stop)
        main_layout.add_widget(close_window_button)

        return main_layout
    
    def carplayWarning(self, instance):
        carplay_options_layout = BoxLayout(orientation='vertical')

        openCarplay_button = Button(text='Launch Carplay (Beta)')
        # Working on launching Carplay AppImage from repo
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
    def open_popup(self, instance):
        layout = BoxLayout(orientation='vertical')

        button1 = Button(text='Car Infotainment')
        # Currently in the works
        #button1.bind(on_press=lambda x: self.show_number(1))
        layout.add_widget(button1)

        button2 = Button(text='Track Mode')
        # Currently in the works
        #button2.bind(on_press=lambda x: self.show_number(2))
        layout.add_widget(button2)

        close_Button = Button(text='Return to Main Menu')
        close_Button.bind(on_press=lambda x: self.popup.dismiss())
        layout.add_widget(close_Button)

        self.popup = Popup(title='Popup Window', 
                           content=layout, 
                           size_hint=(None, None), 
                           size=(600, 400))
        self.popup.open()

    
if __name__ == '__main__':
    MyApp().run()
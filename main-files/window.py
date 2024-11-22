from kivy.app import App
from kivy.lang import Builder
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, Screen
from screens import MainScreen, CarplayScreen, InfoScreen, TrackScreen, ReverseScreen
from mediaplayer import AirplayMedia


Config.set('graphics', 'fullscreen', 'auto')
Config.set('kivy', 'window_icon', '')
Config.set('kivy', 'desktop', 1)
Config.set('graphics', 'borderless', 1)

Builder.load_string("""
<RoundedButton@Button>:
    background_color: 0, 0, 0, 0  # remove the default white background
    canvas.before:
        Color:
            rgba: (0.1, 0.5, 0.6, 1) if self.state == 'normal' else (0.6, 0.5, 0.1, 1)  # choose a color, you can of course use rgba
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [20,]
                    
<CloseButton@Button>:
    background_color: 0, 0, 0, 0  # remove the default white background
    #background_color: 0.6, 0, 0, 1  # remove the default white background
    canvas.before:
        Color:
            rgba: (0.3, 0, 0, 1) if self.state == 'normal' else (0.6, 0.5, 0.1, 1)  # choose a different color
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [20,]
        Color:
            rgba: 0.3, 0, 0, 1
        Line:
            rounded_rectangle: (self.x, self.y, self.width, self.height, 20)
            width: 1
""")

RoundedButton = Builder.load_string("<RoundedButton@Button>:")
CloseButton = Builder.load_string("<CloseButton@Button>:")


class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(CarplayScreen(name='carplay'))
        sm.add_widget(InfoScreen(name='info'))
        sm.add_widget(TrackScreen(name='track'))
        sm.add_widget(ReverseScreen(name='reverse'))
        sm.add_widget(AirplayMedia(name='airplay'))
        return sm

if __name__ == '__main__':
    MyApp().run()

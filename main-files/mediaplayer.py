from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.factory import Factory

class MediaPlayer(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        label = Label (text="Media Mode",
                       pos_hint={'center_x':0.5, 'center_y':0.9})
        self.add_widget(label)
        self.connection_btn = Factory.RoundedButton(text="Start Bluetooth Connection",
                                               size_hint=(0.3, 0.1),
                                               pos_hint={'center_x': 0.5, 'center_y': 0.35})
        self.connection_btn.bind(on_press=self.connection_bluetooth)
        self.add_widget(self.connection_btn)

        back_btn = Factory.CloseButton(text="Back",
                          size_hint=(0.3, 0.1),
                          pos_hint={'center_x': 0.5, 'center_y': 0.2})
        back_btn.bind(on_press=self.go_back)
        self.add_widget(back_btn)

    def connection_bluetooth(self, *args):
        if self.connection_btn.text == "Start Bluetooth Connection":
            self.connection_btn.text = "Stop Bluetooth Connection"
            # Establish Airplay Connection using shairport-sync
        else:
            self.connection_btn.text = "Start Bluetooth Connection"
            # Stop Airplay

    def go_back(self, *args):
        self.manager.current = 'main'
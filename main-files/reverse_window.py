import cv2
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.factory import Factory
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
from kivy.clock import Clock

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
        self.event = Clock.schedule_interval(self.update, 1.0/120.0)

    def on_leave(self, *args):
        self.capture.release()
        Clock.unschedule(self.event)

    def go_back(self, *args):
        self.capture.release()
        self.manager.current = 'main'

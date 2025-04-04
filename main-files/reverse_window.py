import cv2
import numpy as np
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.factory import Factory
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
from kivy.clock import Clock

class ReverseScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.capture = None  # Initialize capture object
        self.event = None  # Store Clock event

        label = Label(text="Reverse Camera", pos_hint={'center_x': 0.5, 'center_y': 0.9})
        back_btn = Factory.CloseButton(text="Back", size_hint=(0.3, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.2})
        back_btn.bind(on_press=self.go_back)

        self.image = Image()

        self.add_widget(label)
        self.add_widget(self.image)
        self.add_widget(back_btn)

    def draw_guidelines(self, frame):
        """Draws perspective-correct parking guidelines on the frame."""
        height, width, _ = frame.shape
        
        # Define colors
        GREEN = (0, 255, 0)
        RED = (0, 0, 255)
        YELLOW = (0, 255, 255)
        
        # Center guide (Yellow)
        #cv2.line(frame, (width // 2, height), (width // 2, int(height * 0.3)), YELLOW, 4)

        # Wider at bottom, narrow at top
        # ACTUALLY TOP LEFT
        top_left = (int(width * 0.37), int(height*0.42))  # 20% from left at bottom
        # ACTUALLY TOP RIGHT
        top_right = (int(width * 0.63), int(height*0.42))  # 80% from left at bottom
        # ACTUALLY BOTTOM LEFT
        bottom_left = (int(width * 0.05), int(height * 0.1))  # 40% from left at top
        # ACTUALLY BOTTOM RIGHT
        bottom_right = (int(width * 0.95), int(height * 0.1))  # 60% from left at top

        yellow_left_x = int((top_left[0] + bottom_left[0]) // 2)
        yellow_left_y = int((top_left[1] + bottom_left[1]) // 2)

        yellow_right_x = int((top_right[0] + bottom_right[0]) // 2)
        yellow_right_y = int((top_right[1] + bottom_right[1]) // 2)

        yellow_left = (yellow_left_x, yellow_left_y)
        yellow_right = (yellow_right_x, yellow_right_y)

        # Stop zone (Red)
        cv2.line(frame, bottom_left, bottom_right, RED, 10)

        # Yellow Line
        cv2.line(frame, yellow_left, yellow_right, YELLOW, 6)

        # Draw left and right parking guides (Green)
        cv2.line(frame, top_left, bottom_left, GREEN, 8)
        cv2.line(frame, top_right, bottom_right, GREEN, 8)



        return frame

    def update(self, dt):
        if self.capture is not None:
            ret, frame = self.capture.read()
            if ret:
                frame = cv2.flip(frame, -1)  # Flip image
                frame = self.draw_guidelines(frame)  # Draw parking lines

                buf = frame.tobytes()
                image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
                image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
                self.image.texture = image_texture
            else:
                print("Warning: Failed to read frame!")
                self.show_placeholder()  # Call placeholder function
        else:
            self.show_placeholder()  # Call placeholder function if capture is None

    def show_placeholder(self):
        """Displays a black screen or a 'No Camera Feed' message when the camera is unavailable."""
        height, width = 480, 640  # Standard resolution
        placeholder = np.zeros((height, width, 3), dtype=np.uint8)  # Create a black image
        
        # Display text on the placeholder image
        cv2.putText(placeholder, "No Camera Feed", (150, 240), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        # Convert to texture
        buf = placeholder.tobytes()
        image_texture = Texture.create(size=(width, height), colorfmt='bgr')
        image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')

        # Explicitly update the image widget
        self.image.texture = image_texture
        self.image.canvas.ask_update()  # Ensure Kivy updates the UI

    def on_enter(self, *args):
        """Called when the screen is entered. Starts the camera feed."""
        if self.capture is None:
            self.capture = cv2.VideoCapture(0)
            if not self.capture.isOpened():
                self.show_placeholder()
                print("Error: Could not open camera!")
                return
        self.event = Clock.schedule_interval(self.update, 1.0/30.0)  # Run at 30 FPS

    def on_leave(self, *args):
        """Called when the screen is left. Stops the camera feed."""
        if self.capture is not None:
            self.capture.release()
            self.capture = None  # Set to None to avoid issues
        if self.event is not None:
            Clock.unschedule(self.event)
            self.event = None

    def go_back(self, *args):
        """Handles going back to the main screen."""
        self.on_leave()  # Properly release resources
        self.manager.current = 'main'
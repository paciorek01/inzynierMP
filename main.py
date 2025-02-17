from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.anchorlayout import AnchorLayout
from kivy.graphics.texture import Texture
import services.detectionService 
from kivy.clock import Clock

import services.procesingService
import services.detectionService
import services.getImageService

class ObjectDetectionApp(App):
    def build(self):
        root = BoxLayout(orientation="vertical")

        header = BoxLayout(size_hint=(1, 0.1))
        with header.canvas.before:
            Color(0, 0.8, 0, 1)  
            self.rect = Rectangle(size=header.size, pos=header.pos)
        header.bind(size=self.update_rect, pos=self.update_rect)

        header_label = Label(text="Wykrywanie App", color=(0, 0, 0, 1), font_size=24)
        header.add_widget(header_label)
        root.add_widget(header)

        container = BoxLayout(size_hint=(1, 0.8), padding=20)

        frame = AnchorLayout(anchor_x="center", anchor_y="center") 
        with frame.canvas.before:
            Color(0.7, 0.7, 0.7, 1)  
            self.frame_rect = Rectangle(size=(420, 420), pos=(0, 0))  
        frame.bind(size=self.update_frame_rect, pos=self.update_frame_rect)

        self.image = Image(source="test3.jpg", size_hint=(None, None), size=(400, 400))
        with self.image.canvas.before:
            Color(0, 0, 0, 1)  
            self.image_rect = Rectangle(size=self.image.size, pos=self.image.pos)
        self.image.bind(size=self.update_image_rect, pos=self.update_image_rect)

        frame.add_widget(self.image)
        container.add_widget(frame)
        root.add_widget(container)

        self.result_label = Label(text="Detection Results: ", size_hint=(1, 0.1))
        root.add_widget(self.result_label)

        self.perform_detection("test3.jpg")

        return root

    def update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    def update_frame_rect(self, instance, value):
        self.frame_rect.size = instance.size
        self.frame_rect.pos = instance.pos

    def update_image_rect(self, instance, value):
        self.image_rect.size = instance.size
        self.image_rect.pos = instance.pos


    def perform_detection(self, image_path):

        detections, original_image = services.detectionService.detectObject(image_path)

        if detections and original_image is not None:
            detected_image, detected_class = services.procesingService.processDetections(detections, original_image)
            if detected_image:
                Clock.schedule_once(lambda dt: self.update_image(detected_image))
                Clock.schedule_once(lambda dt: self.update_result_label(detected_class))

    def update_image(self, detected_image_path):
        self.image.source = detected_image_path
        self.image.reload()

    def update_result_label(self, detected_class):
        self.result_label.text = f"Wykryta linia numer: {detected_class}" if detected_class else "Brak wykrycia"


if __name__ == "__main__":
    ObjectDetectionApp().run()

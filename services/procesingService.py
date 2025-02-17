import cv2
import pygame

pygame.mixer.init()

SOUND_FILES = {
    0: "files/r_159.mp3",
    1: "files/r_45.mp3",
    2: "files/r_50.mp3",
    3: "files/r_72.mp3"
}

def processDetections(detections, original_image):

    try:
        detected_class = ""

        if original_image is None:
            return None, None  

        for detection in detections:
            x1, y1, x2, y2 = detection["bounding_box"]
            cv2.rectangle(original_image, (x1, y1), (x2, y2), (0, 255, 0), 2)

            class_id = detection["class_id"]
            if class_id in SOUND_FILES:
                try:
                    pygame.mixer.music.load(SOUND_FILES[class_id])
                    pygame.mixer.music.play()
                    detected_class = str(class_id)
                    match class_id:
                        case 0:
                            detected_class = "159"
                        case 1:
                            detected_class = "45"
                        case 2:
                            detected_class = "50"
                        case 3:
                            detected_class = "72"

                except pygame.error as e:
                    print(f"Brak pliku dla klasy {class_id}: {e}")

        detected_image_path = "temp/detected_image.jpg"
        cv2.imwrite(detected_image_path, original_image)

        return detected_image_path, detected_class

    except Exception as e:
        return None, None
import cv2

def capture_image():

    try:
        cam = cv2.VideoCapture(0)  
        if not cam.isOpened():
            raise Exception("Błąd aparatu")

        ret, frame = cam.read()  
        cam.release()  

        if not ret:
            raise Exception("Błąd pobrania zdjęcia")

        image_path = "temp/capturedImage.jpg"
        cv2.imwrite(image_path, frame)  
        return image_path

    except Exception as e:
        print(f"Błąd: {e}")
        return None
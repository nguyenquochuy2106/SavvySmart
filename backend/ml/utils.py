import cv2
import numpy as np
import base64

def preprocess_image(image_base64: str):
    """
    Decode Base64 image and convert to RGB format.
    """
    try:
        img_data = base64.b64decode(image_base64)
        np_arr = np.frombuffer(img_data, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        # Convert BGR to RGB for consistency
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return img_rgb
    except Exception as e:
        print(f"Error processing image: {e}")
        return None

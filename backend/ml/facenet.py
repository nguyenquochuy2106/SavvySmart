import numpy as np
import cv2
import base64
from keras_facenet import FaceNet
from mtcnn import MTCNN
from backend.ml.utils import preprocess_image

# Initialize models
facenet_model = FaceNet()
mtcnn_detector = MTCNN()

def detect_face(image_base64: str):
    """
    Detect a face in the image using MTCNN.
    Returns the cropped face if found, otherwise None.
    """
    img_array = preprocess_image(image_base64)
    if img_array is None:
        return None

    # Convert back to BGR for MTCNN
    img_bgr = (img_array * 255).astype(np.uint8)
    img_bgr = cv2.cvtColor(img_bgr, cv2.COLOR_RGB2BGR)

    # Detect faces
    detections = mtcnn_detector.detect_faces(img_bgr)
    if len(detections) == 0:
        return None

    # Extract bounding box of first detected face
    x, y, width, height = detections[0]["box"]
    x, y = max(0, x), max(0, y)  # Ensure no negative values
    face = img_bgr[y:y+height, x:x+width]

    # Resize face for FaceNet
    face_resized = cv2.resize(face, (160, 160))
    face_normalized = face_resized.astype("float32") / 255.0

    return face_normalized

def generate_embedding(image_base64: str):
    """
    Convert a Base64 image to a FaceNet embedding.
    """
    face_array = detect_face(image_base64)
    if face_array is None:
        return None

    # Generate embedding
    embedding = facenet_model.embeddings([face_array])
    return embedding.tolist()[0]  # Convert to list for storage

def compare_embeddings(embedding1, embedding2, threshold=0.6):
    """
    Compare two embeddings to determine if they match.
    """
    distance = np.linalg.norm(np.array(embedding1) - np.array(embedding2))
    return distance < threshold  # True if embeddings are similar

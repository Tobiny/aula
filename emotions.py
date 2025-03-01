import cv2
from deepface import DeepFace
import numpy as np

def detect_emotion(camera_index=0):
    """
    Capture an image from the specified camera and detect the dominant emotion.
    
    Args:
        camera_index (int): Index of the camera to use
        
    Returns:
        str: The dominant emotion detected, or None if no faces/emotions were detected
    """
    try:
        # Initialize camera
        cap = cv2.VideoCapture(camera_index)
        
        if not cap.isOpened():
            print(f"Error: Could not open camera {camera_index}")
            return None
        
        # Capture frame
        ret, frame = cap.read()
        
        if not ret:
            print("Error: Could not read frame from camera")
            cap.release()
            return None
        
        # Analyze emotions using DeepFace
        result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        
        # Release camera
        cap.release()
        
        # Count emotions across all detected faces
        emotion_counts = {}
        
        # Handle both single face and multiple faces
        if isinstance(result, list):
            faces = result
        else:
            faces = [result]
            
        for face in faces:
            dominant_emotion = face['dominant_emotion']
            emotion_counts[dominant_emotion] = emotion_counts.get(dominant_emotion, 0) + 1
        
        # Determine the dominant emotion overall
        if emotion_counts:
            dominant_emotion = max(emotion_counts, key=emotion_counts.get)
            print(f"Dominant emotion detected: {dominant_emotion}")
            return dominant_emotion
        else:
            print("No emotions detected")
            return None
            
    except Exception as e:
        print(f"Error in emotion detection: {str(e)}")
        return None

def get_emotion_color(emotion):
    """
    Returns a color (BGR format) associated with each emotion for visualization
    
    Args:
        emotion (str): Detected emotion
        
    Returns:
        tuple: BGR color values
    """
    emotion_colors = {
        'happy': (0, 255, 255),    # Yellow
        'sad': (255, 0, 0),        # Blue
        'angry': (0, 0, 255),      # Red
        'fear': (255, 0, 255),     # Magenta
        'surprise': (0, 255, 0),   # Green
        'neutral': (255, 255, 255), # White
        'disgust': (0, 165, 255)   # Orange
    }
    
    return emotion_colors.get(emotion, (200, 200, 200))  # Default gray
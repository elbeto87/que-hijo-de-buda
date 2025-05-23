import cv2
import numpy as np
from deepface import DeepFace

from constants import FACE_TO_ANALYZE_PATH
from logger import logger


def face_emotions(face: np.ndarray) -> str | None:
    try:
        face_for_emotion = cv2.cvtColor(face, cv2.COLOR_RGB2BGR)
        cv2.imwrite(FACE_TO_ANALYZE_PATH, face_for_emotion)
        emotion_result = DeepFace.analyze(face_for_emotion, actions=['emotion'], enforce_detection=True)
        emotion = emotion_result[0]['dominant_emotion']
        return f" | Mood: {emotion}"
    except Exception as e:
        logger.error(f"Error analyzing emotion: {e}")
        return " | Mood: Unknown"

import cv2
from deepface import DeepFace

from logger import logger

video_path = "/home/elbeto87/Desktop/projects/que-hijo-de-buda/milei.mp4"
cap = cv2.VideoCapture(video_path)

db_path = "/home/elbeto87/Desktop/projects/que-hijo-de-buda/dataset/milei"

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_path = "temp_frame.jpg"
    cv2.imwrite(frame_path, frame)

    try:
        results = DeepFace.find(img_path=frame_path, db_path=db_path, model_name="ArcFace", enforce_detection=False)

        if len(results) > 0 and len(results[0]) > 0:
            logger.info("Milei has been detected")
            cv2.putText(frame, "Milei detected", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    except Exception as e:
        print("Error:", e)

    cv2.imshow("Video", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
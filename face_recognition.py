import cv2
from deepface import DeepFace

from logger import logger

def recognize_mile_face():
    video_path = "/home/elbeto87/Desktop/projects/que-hijo-de-buda/milei.mp4"
    cap = cv2.VideoCapture(video_path)

    db_path = "/home/elbeto87/Desktop/projects/que-hijo-de-buda/dataset/milei"
    frame_count = 0
    process_interval = 10

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        if frame_count % process_interval == 0:
            frame_path = "temp_frame.jpg"
            frame = cv2.resize(frame, (640, 480))
            cv2.imwrite(frame_path, frame)

            try:
                results = DeepFace.find(img_path=frame_path, db_path=db_path, model_name="ArcFace", enforce_detection=False)

                if len(results) > 0 and len(results[0]) > 0:
                    for result in results:
                        logger.info("Milei's probability: ", result["distance"])
                        if result["distance"] < 0.4:
                            logger.info(f"Milei has been detected: {result}")
                            cv2.putText(frame, f"Match found: {result}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                            break

            except Exception as e:
                print("Error:", e)

        cv2.imshow("Video", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

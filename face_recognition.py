import cv2
import time

from deepface import DeepFace

from logger import logger

def recognize_mile_face():
    video_path = "/home/elbeto87/Desktop/projects/que-hijo-de-buda/milei.mp4"
    cap = cv2.VideoCapture(video_path)

    db_path = "/home/elbeto87/Desktop/projects/que-hijo-de-buda/dataset/milei"
    frame_count = 0
    process_interval = 2
    video_duration = 5
    start_time = time.time()
    out = cv2.VideoWriter("/home/elbeto87/Desktop/projects/que-hijo-de-buda/milei_analysis.mp4", cv2.VideoWriter.fourcc('M','P','4','V'), 20.0, (int(cap.get(3)), int(cap.get(4))))

    while cap.isOpened():

        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        if frame_count % process_interval == 0:

            try:
                results = DeepFace.find(img_path=frame, db_path=db_path, model_name="ArcFace", enforce_detection=False)
                if len(results) > 0 and len(results[0]) > 0:
                    for result in results:
                        if (result["distance"] > 0.6).any():
                            x, y, w, h = result["target_x"].iloc[0], result["target_y"].iloc[0], result["target_w"].iloc[0], result["target_h"].iloc[0]
                            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                            cv2.putText(
                                frame,
                                f"Match found: {result['identity']}",
                                (50, 50),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                1,
                                (0, 255, 0),
                                2,
                                cv2.LINE_AA
                            )
                            break  # Solo mostrar el primer resultado
            except Exception as e:
                print("Error:", e)

        cv2.imshow("Video", frame)
        out.write(frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

        if start_time and time.time() - start_time >= video_duration:
            logger.info(f"10 seconds of detection completed. Stopping recording.")
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

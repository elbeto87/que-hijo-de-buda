import cv2
import torch
from facenet_pytorch import MTCNN, InceptionResnetV1
from logger import logger

mtcnn = MTCNN(keep_all=True, device='cpu')
resnet = InceptionResnetV1(pretrained='vggface2').eval()
cap = cv2.VideoCapture('milei.mp4')


def recognize_faces():
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        boxes, _ = mtcnn.detect(rgb_frame)

        if boxes is not None:
            for box in boxes:
                x1, y1, x2, y2 = map(int, box)
                face = rgb_frame[y1:y2, x1:x2]

                if face.size == 0:
                    continue

                # Convert the face to a tensor and normalize
                face = cv2.resize(face, (160, 160))
                face = torch.tensor(face, dtype=torch.float32).permute(2, 0, 1) / 255.0
                face = face.unsqueeze(0)

                # Extract the embedding
                with torch.no_grad():
                    embedding = resnet(face)

                # Draw the bounding box
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                # Draw the text
                cv2.putText(
                    frame,
                    "Face detected",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    2
                )

        cv2.imshow("Face Recognition", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
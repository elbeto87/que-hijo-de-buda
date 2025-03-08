import os

import cv2
import torch
import numpy as np
from emotions import face_emotions
from facenet_pytorch import MTCNN, InceptionResnetV1
from deepface import DeepFace
from logger import logger


mtcnn = MTCNN(keep_all=True, device='cpu')
resnet = InceptionResnetV1(pretrained='vggface2').eval()


def load_person_dataset(dataset_path: str = "./dataset/milei"):
    embeddings = []
    for file in os.listdir(dataset_path):
        try:
            img_path = os.path.join(dataset_path, file)
            img = cv2.imread(img_path)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            if img is None:
                continue
            faces, _ = mtcnn.detect(img)
            if faces is not None:
                x1, y1, x2, y2 = map(int, faces[0])
                face = img[y1:y2, x1:x2]
                face = cv2.resize(face, (160, 160))
                face = torch.tensor(face, dtype=torch.float32).permute(2, 0, 1) / 255.0
                face = face.unsqueeze(0)
                with torch.no_grad():
                    embedding = resnet(face)
                embeddings.append(embedding.numpy())
        except Exception as e:
            logger.error(e)
            continue
    return np.array(embeddings)


def cosine_similarity(embedding1, embedding2):
    return np.dot(embedding1, embedding2.T) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))


def recognize_faces(duration: int = 30):

    cap = cv2.VideoCapture('milei.mp4')
    milei_embeddings = load_person_dataset()

    # Obtain the video properties
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Duration
    frame_limit = fps * duration
    frame_count = 0

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    output_video = cv2.VideoWriter('milei_analysis.mp4', fourcc, fps, (frame_width, frame_height))

    while True and frame_count < frame_limit:
        ret, frame = cap.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        boxes, _ = mtcnn.detect(rgb_frame)

        if boxes is not None:
            for box in boxes:
                x1, y1, x2, y2 = map(int, box)
                face_rgb = rgb_frame[y1:y2, x1:x2]

                if face_rgb.size == 0:
                    continue

                # Convert the face to a tensor and normalize
                face = torch.tensor(face_rgb, dtype=torch.float32).permute(2, 0, 1) / 255.0
                face = face.unsqueeze(0)

                # Extract the embedding
                with torch.no_grad():
                    face_embedding = resnet(face)

                similarities = [cosine_similarity(face_embedding, milei_emb) for milei_emb in milei_embeddings]
                max_similarity = max(similarities)
                percentage = max_similarity[0, 0] * 100

                if max_similarity > 0.6:
                    label = f"Milei is detected ({percentage:.2f}%)"
                    color = (0, 255, 0)
                    label += face_emotions(face_rgb)
                else:
                    label = f"Unknown ({percentage:.2f}%)"
                    color = (0, 0, 255)

                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        cv2.imshow("Face Recognition", frame)

        output_video.write(frame)

        frame_count += 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    output_video.release()

    cap.release()
    cv2.destroyAllWindows()


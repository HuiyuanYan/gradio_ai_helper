from src.analyzer.content_analyzer import ContentAnalyzer
from typing import Dict
from transformers import pipeline
from facenet_pytorch import MTCNN
import cv2
import numpy as np
from PIL import Image

class DetectionPipeline:
    def __init__(self, detector, n_frames=None, batch_size=60, resize=None):
        self.detector = detector
        self.n_frames = n_frames
        self.batch_size = batch_size
        self.resize = resize

    def __call__(self, filename):
        v_cap = cv2.VideoCapture(filename)
        v_len = int(v_cap.get(cv2.CAP_PROP_FRAME_COUNT))

        if self.n_frames is None:
            sample = np.arange(0, v_len)
        else:
            sample = np.linspace(0, v_len - 1, self.n_frames).astype(int)

 
        faces = []
        frames = []

        for j in range(v_len):
            success = v_cap.grab()
            if not success:
                print("[ERROR] first loop failed!!!")
            if j in sample:
                success, frame = v_cap.retrieve()
                if not success:
                    print("[ERROR] Second loop failed!!!")
                    continue
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                if self.resize is not None:
                    frame = frame.resize([int(d * self.resize) for d in frame.size])
                frames.append(frame) 
                if len(frames) % self.batch_size == 0 or j == sample[-1]:
                    break
              
        boxes, probs = self.detector.detect(frames) 
        for i, frame in enumerate(frames):
            face2 = np.zeros_like(frame)   
            if boxes[i] is None: 
                continue

            box = boxes[i][0].astype(int)
            face = frame[box[1]:box[3], box[0]:box[2]]

            if face.any():
                face2 = cv2.resize(face, (224, 224))

            faces.append(face2)

        frames = []   

        v_cap.release()

        return faces

class VideoAnalyzer(ContentAnalyzer):
    def __init__(self):
        self.faces_geter = DetectionPipeline(detector=MTCNN(margin=14, keep_all=True, factor=0.7, device='cpu'), n_frames=20, batch_size=60)
        self.image_analyzer = pipeline("image-classification", model="dima806/deepfake_vs_real_image_detection")

    def _analyze(self, file_path: str) -> Dict:
        """Analyze video content in the provided file."""
        faces = self.faces_geter(file_path)
        if (len(faces) == 0):
            return {
                "real": 1.0,
                "fake": 0
            }
        total = len(faces)
        # print(total)
        real = 0
        fake = 0
        for face in faces:
            ok = self.image_analyzer(Image.fromarray(face))
            for i in range(2):
                if ok[i]['label'] == 'Fake':
                    fake += ok[i]['score']
                else:
                    real += ok[i]['score']
        real_score = real / total
        fake_score = fake / total

        return {
            "real": real_score,
            "fake": fake_score
        }

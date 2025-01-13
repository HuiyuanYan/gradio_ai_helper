from transformers import pipeline
from facenet_pytorch import MTCNN
import cv2
import numpy as np
from PIL import Image
from src.pipeline.custom_pipeline import CustomPipeline

class FaceDetector:
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


class DeepFakeVideoPipeline(CustomPipeline):
    def __init__(
        self,
        task: str,
        model: str,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.face_detector = FaceDetector(
            detector=MTCNN(
                margin=14, 
                keep_all=True, 
                factor=0.7, 
                device='cpu'
            ), 
            n_frames=20, 
            batch_size=60
        )
        self.image_pipeline = pipeline(
            task=task,
            model=model,
        )
    
    def _preprocess(self, input_data):
        faces = self.face_detector(input_data)
        return faces
    
    def _predict(self, processed_data):
        total = len(processed_data)
        if total == 0:
            return [
                {'score': 1.0}
            ]
        real = 0.0
        fake = 0.0
        for face in processed_data:
            ok = self.image_pipeline(Image.fromarray(face))
            for i in range(2):
                if ok[i]['label'] == 'Fake':
                    fake += ok[i]['score']
                else:
                    real += ok[i]['score']
        return real,fake

    def _postprocess(self, prediction):
        real, fake = prediction
        assert real + fake > 0
        return [
            {'score': real / (real+ fake)},
        ]
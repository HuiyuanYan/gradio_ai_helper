import librosa
import numpy as np
import cv2
from tensorflow.python.keras.models import load_model
from src.pipeline.custom_pipeline import CustomPipeline
class Deep4snetAudioPipeline(CustomPipeline):
    def __init__(self, model_path, weights_path, **kwargs):
        super().__init__(**kwargs)
        self.model = load_model(model_path)
        self.model.load_weights(weights_path)

    def _preprocess(self, file_path):
        """Preprocess the audio file to generate the input for the model."""
        y, sr = librosa.load(file_path, sr=None)
        mel_spectogram = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
        mel_spectogram_db = librosa.power_to_db(mel_spectogram, ref=np.max)
        img = np.expand_dims(mel_spectogram_db, axis=-1)
        img = np.repeat(img, 3, axis=-1)
        img = cv2.resize(img, (150, 150))
        img = np.reshape(img, [1, 150, 150, 3])
        return img

    def _predict(self, processed_data):
        """Predict if the audio is deepfake."""
        prediction = self.model.predict(processed_data)
        return prediction[0][0]

    def _postprocess(self, prediction):
        """Postprocess the prediction to return the final result."""
        real_score = prediction
        return [
            {
                'score':real_score
            }
        ]
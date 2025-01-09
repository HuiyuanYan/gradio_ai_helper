import os
import matplotlib.pyplot as plt
from src.analyzer.content_analyzer import ContentAnalyzer
from typing import Dict
import librosa
import numpy as np
import cv2


class AudioAnalyzer(ContentAnalyzer):
    def __init__(self):
        """Initialize the audio analysis model."""
        from tensorflow.python.keras.models import load_model
        self.deep4snet_model = load_model('./models/deep4snet/model_Deep4SNet.h5')
        self.deep4snet_model.load_weights('./models/deep4snet/weights_Deep4SNet.h5')

    def _process_audio(self, file_path):
        filename = os.path.basename(file_path)

        y, sr = librosa.load(file_path, sr=None)

        short_time_fourier_transform = librosa.stft(y)
        magnitude = np.abs(short_time_fourier_transform)
        mel_spectogram = librosa.feature.melspectrogram(S=magnitude, sr=sr, n_mels=128)
        mel_spectogram_decibel_scale = librosa.power_to_db(mel_spectogram, ref=np.max)

        output_dir = 'generated-spectograms'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        plt.figure(figsize=(1.5, 1.5))
        librosa.display.specshow(mel_spectogram_decibel_scale, sr=sr, x_axis='time', y_axis='mel')
        plt.axis('off')
        plt.savefig(f'generated-spectograms/{filename}.png', bbox_inches='tight', pad_inches=0)
        plt.close()

        img = cv2.imread(f'generated-spectograms/{filename}.png')
        #print(img)
        img = cv2.resize(img, (150, 150))
        img = np.reshape(img, [1, 150, 150, 3])

        return img

    def _predict_deepfake(self, file_path):
        """Predict if the audio is deepfake."""
        processed_audio = self._process_audio(file_path)
        prediction = self.deep4snet_model.predict(processed_audio, batch_size=19)
        return prediction[0][0]

    def _analyze(self, file_path: str) -> Dict:
        """Analyze audio content in the provided file."""
        # 进行音频真伪检测：提取音频特征并传入音频真伪检测模型
        audio_features = self._predict_deepfake(file_path)
        print(audio_features)
        # 这里假设伪造音频的输出类别为1，真实音频为0
        real_score = audio_features  # 获取伪造概率
        fake_score = 1.0 - real_score  # 真实概率

        return {
            "real": real_score,
            "fake": fake_score
        }

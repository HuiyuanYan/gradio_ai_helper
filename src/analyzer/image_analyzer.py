from transformers import pipeline
from src.analyzer.content_analyzer import ContentAnalyzer
from typing import Dict

class ImageAnalyzer(ContentAnalyzer):
    def __init__(self):
        """Initialize the image analysis model (if needed)."""
        self.image_detector = pipeline(
            "image-classification",
            model="umm-maybe/AI-image-detector"
        )
        pass  # You can initialize your image model here.
    
    def _analyze(self, file_path: str) -> Dict:
        """Analyze image content in the provided file."""
        authenticity = self.image_detector(file_path)
        
        real_score = authenticity[0]['score']
        fake_score = 1.0 - real_score
        
        # real score和 fake score都保留两位小数
        return {
            "real": real_score,
            "fake": fake_score
        }

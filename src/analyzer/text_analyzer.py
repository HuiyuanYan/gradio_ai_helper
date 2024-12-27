from transformers import pipeline
from typing import Dict
from src.analyzer.content_analyzer import ContentAnalyzer

class TextAnalyzer(ContentAnalyzer):
    def __init__(self):
        """Initialize the text detector model."""
        self.text_detector = pipeline("text-classification", model="roberta-base-openai-detector")
    
    def _analyze(self, file_path: str) -> Dict:
        """Analyze text content in the provided file."""
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()
        authenticity = self.text_detector(text)
        
        real_score = authenticity[0]['score']
        fake_score = 1.0 - real_score
        
        return {
            "real": real_score,
            "fake": fake_score
        }

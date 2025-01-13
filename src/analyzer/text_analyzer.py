from typing import Dict
from src.analyzer.content_analyzer import ContentAnalyzer
from src.pipeline import get_pipeline
class TextAnalyzer(ContentAnalyzer):
    def __init__(self,pipeline_type,**args):
        """Initialize the text detector model."""
        self.pipeline = get_pipeline(
            pipeline_type=pipeline_type,
            **args
        )
    
    def _analyze(self, file_path: str) -> Dict:
        """Analyze text content in the provided file."""
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()
        authenticity = self.pipeline(text)
        
        real_score = authenticity[0]['score']
        fake_score = 1.0 - real_score
        
        # real score和 fake score都保留两位小数
        return {
            "real": real_score,
            "fake": fake_score
        }

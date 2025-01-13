from src.analyzer.content_analyzer import ContentAnalyzer
from src.pipeline import get_pipeline
from typing import Dict


class AudioAnalyzer(ContentAnalyzer):
    def __init__(self,pipeline_type,**args):
        """Initialize the text detector model."""
        self.pipeline = get_pipeline(
            pipeline_type=pipeline_type,
            **args
        )


    def _analyze(self, file_path: str) -> Dict:
        """Analyze audio content in the provided file."""
        authenticity = self.pipeline(file_path)
        real_score = authenticity[0]['score']
        fake_score = 1.0 - real_score
        
        # real score和 fake score都保留两位小数
        return {
            "real": real_score,
            "fake": fake_score
        }

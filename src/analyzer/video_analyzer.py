from src.analyzer.content_analyzer import ContentAnalyzer
from typing import Dict
from src.pipeline import get_pipeline


class VideoAnalyzer(ContentAnalyzer):
    def __init__(self,pipeline_type,**args):
        """Initialize the text detector model."""
        self.pipeline = get_pipeline(
            pipeline_type=pipeline_type,
            **args
        )

    def _analyze(self, file_path: str) -> Dict:
        """Analyze video content in the provided file."""
        authenticity = self.pipeline(file_path)
        real_score = authenticity[0]['score']
        fake_score = 1.0 - real_score
        return {
            "real": real_score,
            "fake": fake_score
        }

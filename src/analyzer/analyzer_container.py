from typing import Dict
from src.analyzer.text_analyzer import TextAnalyzer
from src.analyzer.image_analyzer import ImageAnalyzer
from src.analyzer.audio_analyzer import AudioAnalyzer
from src.analyzer.video_analyzer import VideoAnalyzer
from src.utils import validate_file_format

from src.settings import Settings
from src.utils import logger

logger.info(f"Loading AnalyzerContainer, analyzer settings: {Settings.analyzer_settings}")
class AnalyzerContainer:
    def __init__(self):
        """初始化容器并添加所有分析器"""
        self.analyzers = {
            "text": TextAnalyzer(
                Settings.analyzer_settings.text_analyzer["pipeline"],
                **Settings.analyzer_settings.text_analyzer["args"]
            ),
            "image": ImageAnalyzer(
                Settings.analyzer_settings.image_analyzer["pipeline"],
                **Settings.analyzer_settings.image_analyzer["args"]
            ),
            "audio": AudioAnalyzer(
                Settings.analyzer_settings.audio_analyzer["pipeline"],
                **Settings.analyzer_settings.audio_analyzer["args"]
            ),
            "video": VideoAnalyzer(
                Settings.analyzer_settings.video_analyzer["pipeline"],
                **Settings.analyzer_settings.video_analyzer["args"]
            )
        }

    def analyze(self, file_path: str) -> Dict:
        """根据文件路径自动判断文件类型并选择相应的分析器"""
        is_valid, media_type = validate_file_format(file_path)
        if not is_valid:
            raise ValueError(f"Unsupported file format for file: {file_path}")

        analyzer = self.analyzers.get(media_type)
        if analyzer is None:
            raise ValueError(f"No analyzer found for media type: {media_type}")
        
        return analyzer.analyze(file_path)

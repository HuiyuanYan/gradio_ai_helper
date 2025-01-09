from typing import Dict
from src.analyzer.text_analyzer import TextAnalyzer
from src.analyzer.image_analyzer import ImageAnalyzer
from src.analyzer.audio_analyzer import AudioAnalyzer
from src.analyzer.video_analyzer import VideoAnalyzer
from src.utils import validate_file_format


class AnalyzerContainer:
    def __init__(self):
        """初始化容器并添加所有分析器"""
        self.analyzers = {
            "text": TextAnalyzer(),
            "image": ImageAnalyzer(),
            "audio": AudioAnalyzer(),  # 如果你有音频分析器
            "video": VideoAnalyzer()
        }

    def analyze(self, file_path: str) -> Dict:
        """根据文件路径自动判断文件类型并选择相应的分析器"""
        is_valid, media_type = validate_file_format(file_path)
        if not is_valid:
            raise ValueError(f"Unsupported file format for file: {file_path}")

        # 获取对应的分析器并执行分析
        analyzer = self.analyzers.get(media_type)
        if analyzer is None:
            raise ValueError(f"No analyzer found for media type: {media_type}")
        
        return analyzer.analyze(file_path)

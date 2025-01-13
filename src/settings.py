# settings.py
import os,sys
sys.path.append(os.getcwd())
from pathlib import Path
GRADIO_AI_HELPER_ROOT = Path(os.environ.get("GRADIO_AI_HELPER_ROOT", ".")).resolve()
from src.pydantic_settings_file import *
from pathlib import Path

class BasicSettings(BaseFileSettings):
    
    model_config = SettingsConfigDict(yaml_file=GRADIO_AI_HELPER_ROOT / "cfg/basic_settings.yaml")
    
    version: str = "0.0.1"
    log_dir: str = "./logs"
    
    shields_start_url:str = "https://img.shields.io/github/stars/HuiyuanYan/gradio_ai_helper?style=plastic"

    env: dict = {
        "HF_ENDPOINT": "https://hf-mirror.com",
        "GRADIO_TEMP_DIR": "./tmp",
        "OPENAI_BASE_URL": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "OPENAI_API_KEY": "sk-xxxx"
    }

    def make_dirs(self):
        os.makedirs(self.log_dir, exist_ok=True)
    
    def load_env(self):
        for key, value in self.env.items():
            os.environ[key] = value
    
class AnalyzerSettings(BaseFileSettings):
    model_config = SettingsConfigDict(yaml_file=GRADIO_AI_HELPER_ROOT / "cfg/analyzer.yaml")
    max_file_num: int = 4
    supported_file_formats:dict = {
        "image": [".jpg", ".jpeg", ".png", ".webp"],
        "video": [".mp4", ".avi", ".webm"],
        "audio": [".mp3", ".wav"],
        "text": [".md", ".txt", ".doc", ".pdf"]
    }

    image_analyzer: dict = {
        "pipeline": "hf_pipeline",
        "args":{
            "task": "image-classification",
            "model": "umm-maybe/AI-image-detector"
        }
    }

    text_analyzer: dict = {
        "pipeline": "hf_pipeline",
        "args":{
            "task": "text-classification",
            "model": "MayZhou/e5-small-lora-ai-generated-detector"
        }
    }

    audio_analyzer: dict = {
        "pipeline": "deep4snet_audio_pipeline",
        "args":{
            "model_path": "./models/model_Deep4SNet.h5",
            "weights_path": "./models/weights_Deep4SNet.h5"
        }
    }

    video_analyzer: dict = {
        "pipeline": "deep_fake_video_pipeline",
        "args":{
            "task": "image-classification",
            "model": "dima806/deepfake_vs_real_image_detection"
        }
    }

    def get_supported_file_formats(self) -> dict:
        return self.supported_file_formats

class LLMSettings(BaseFileSettings):
    model_config = SettingsConfigDict(yaml_file=GRADIO_AI_HELPER_ROOT / "cfg/llm.yaml")
    
    default_history_len: int = 3
    default_temperature: float = 0.7
    default_llm:str = "qwen-long"
    default_llm_type:str = "text"

    supported_llms: dict = {
        "text": ["qwen-long"],
        "image": ["qwen-vl-max-0809"],
        "audio": ["qwen-audio-turbo"]
    }

    def get_supported_models(self)->dict:
        return self.supported_llms

class SettingsContainer:
    GRADIO_AI_HELPER_ROOT = GRADIO_AI_HELPER_ROOT
    basic_settings: BasicSettings = settings_property(BasicSettings())
    analyzer_settings: AnalyzerSettings = settings_property(AnalyzerSettings())
    llm_settings: LLMSettings = settings_property(LLMSettings())

    def __init__(self) -> None:
        self.basic_settings.load_env()
        self.basic_settings.make_dirs()
        

Settings = SettingsContainer()

if __name__ == "__main__":
    print(Path(GRADIO_AI_HELPER_ROOT / "cfg/analyzer.yaml"))
    print(Settings.analyzer_settings.audio_analyzer)
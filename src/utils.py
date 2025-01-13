import os
from typing import Tuple
import base64
import logging
from logging.handlers import RotatingFileHandler
from colorlog import ColoredFormatter
from pathlib import Path
from src.settings import Settings

SUPPORTED_FORMATS = Settings.analyzer_settings.get_supported_file_formats()
SUPPORTED_MODELS = Settings.llm_settings.get_supported_models()

MAX_FILE_NUM = Settings.analyzer_settings.max_file_num

def get_logger(name='app.log', log_file='app.log', log_level=logging.INFO, max_bytes=1024*1024*5, backup_count=5):
    """
    获取一个配置好的 logger。

    :param name: Logger 的名称。
    :param log_file: 日志文件的路径。
    :param log_level: 日志级别，默认为 INFO。
    :param max_bytes: 日志文件的最大大小，超过后会自动轮转，默认为 5MB。
    :param backup_count: 保留的旧日志文件数量，默认为 5。
    :return: 配置好的 logger。
    """
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    file_handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
    file_handler.setLevel(log_level)
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_formatter = ColoredFormatter(
        "%(log_color)s%(asctime)s - %(name)s - %(levelname)s%(reset)s - %(message)s",
        datefmt=None,
        reset=True,
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        },
        secondary_log_colors={},
        style='%'
    )
    console_handler.setFormatter(console_formatter)

    # 添加 handlers 到 logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

logger = get_logger(log_file=str(Path(Settings.basic_settings.log_dir).absolute()/'app.log'))

# 将图片转为base64
def image_to_base64(image_path:str) -> str:
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')
    return base64_image

def get_all_supported_models():
    # 获取所有支持的模型()
    models = []
    for model_list in SUPPORTED_MODELS.values():
        models.extend(model_list)
    # set去重
    models = list(set(models))
    return models




def validate_file_format(file_path: str) -> Tuple[bool, str]:
    """验证文件格式"""
    ext = os.path.splitext(file_path)[1].lower()
    for media_type, formats in SUPPORTED_FORMATS.items():
        if ext in formats:
            return True, media_type
    return False, ext


def convert_message_dict_to_user_input(message:dict,modality:str) -> list | str:
    """将消息字典转换为模型输入"""
    assert modality in SUPPORTED_MODELS.keys(), f"modality {modality} not supported"

    if modality == "audio":
        user_input = []
        if message['text']:
            user_input.append(
                {'text':message['text']}
            )
        for file in message['files']:
            _, media_type = validate_file_format(file)
            if media_type == 'audio':
                user_input.append(
                    {'audio':file}
                )
            else:
                raise ValueError(f"Unsupported file type: {media_type}")
        return user_input
    
    if modality == "image":
        user_input = []
        if message['text']:
            user_input.append(
                {
                    'type':'text',
                    'text':message['text']
                },
            )
        for file in message['files']:
            _, media_type = validate_file_format(file)
            if media_type == 'image':
                user_input.append(
                    {
                        'type':'image_url',
                        'image_url':f"data:image/png;base64,{image_to_base64(file)}"
                    }
                )
            elif media_type == 'video':
                user_input.append(
                    {
                        'type':'video_url',
                        'video_url':file
                    }
                )
            else:
                raise ValueError(f"Unsupported file type: {media_type}")
        return user_input

    if modality == "text":
        user_input = message['text']

    return user_input




def generate_html_for_file(file_path: str) -> str:
    """根据文件路径生成用于渲染文件的HTML代码，并添加边框和文件名"""
    # 首先验证文件格式
    is_supported, media_type = validate_file_format(file_path)
    if not is_supported:
        return "Unsupported file format"

    # 获取文件名称（不包含路径）
    file_name = os.path.basename(file_path)
    
    ext = os.path.splitext(file_path)[1].lower()
    file_path = file_path.replace('\\','/')

    # 保证文件路径存在
    assert os.path.exists(file_path), f"File not found: {file_path}"
    # 根据文件类型生成HTML
    if media_type == 'image':
        # 将图片转换为base64编码，以便在HTML中显示
        
        base64_image = image_to_base64(file_path)
        return (f'<div style="border: 1px solid #ddd; padding: 5px;">'
                f'<strong style="display: block; margin-bottom: 10px;">{file_name}</strong>'
                f'<img src="data:image/{ext[1:]};base64,{base64_image}" alt="{file_name}" />'
                f'</div>')

    elif media_type == 'video':
        return (f'<div style="border: 1px solid #ddd; padding: 5px;">'
                f'<strong style="display: block; margin-bottom: 10px;">{file_name}</strong>'
                f'<video controls><source src="/gradio_api/file={file_path}" type="video/{ext[1:]}">Your browser does not support the video tag.</video>'
                f'</div>')

    elif media_type == 'audio':
        return (f'<div style="border: 1px solid #ddd; padding: 5px;">'
                f'<strong style="display: block; margin-bottom: 10px;">{file_name}</strong>'
                f'<audio controls><source src="/gradio_api/file={file_path}" type="audio/{ext[1:]}">Your browser does not support the audio element.</audio>'
                f'</div>')

    elif media_type == 'text':
        # 文本文件使用<pre>标签来保持格式
        with open(file_path, 'r', encoding='utf-8') as file:
            text_content = file.read()
        return (f'<div style="border: 1px solid #ddd; padding: 5px;">'
                f'<strong style="display: block; margin-bottom: 10px;">{file_name}</strong>'
                f'<pre style="white-space: pre-wrap; word-wrap: break-word;">{text_content}</pre>'
                f'</div>')

    else:
        return "Unsupported file type"


# 辅助函数，用于将图片转为base64（已在utils中定义）
def image_to_base64(image_path: str) -> str:
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')
    return base64_image
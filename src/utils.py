import os
from typing import Tuple
import base64
SUPPORTED_FORMATS = {
    'image': ['.jpg', '.jpeg', '.png', '.webp'],
    'video': ['.mp4', '.avi'],
    'audio': ['.mp3', '.wav'],
    'text': ['.txt', '.doc', '.pdf']
}

SUPPORTED_MODELS_DICT = {
    "text" : ["qwen-long"],
    "image" : ["qwen-vl-max-0809"],
    "audio" : ["qwen-audio-turbo"],
}

# 将图片转为base64
def image_to_base64(image_path:str) -> str:
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')
    return base64_image

def get_all_supported_models():
    # 获取所有支持的模型()
    models = []
    for model_list in SUPPORTED_MODELS_DICT.values():
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
    return False, ""


def convert_message_dict_to_user_input(message:dict,model) -> list | str:
    """将消息字典转换为模型输入"""
    assert model in get_all_supported_models(), "model not supported"

    if model == "qwen-audio-turbo":
        user_input = []
        if message['text']:
            user_input.append(
                {'text':message['text']}
            )
        for file in message['files']:
            if file['mime_type'].startswith('audio'):
                user_input.append(
                    {'audio':file['url']}
                )
            else:
                raise ValueError(f"Unsupported file type: {file['mime_type']}")
        return user_input
    
    if model == "qwen-vl-max-0809":
        user_input = []
        if message['text']:
            user_input.append(
                {
                    'type':'text',
                    'text':message['text']
                },
            )
        for file in message['files']:
            if file['mime_type'].startswith('image'):
                user_input.append(
                    {
                        'type':'image_url',
                        'image_url':f"data:image/png;base64,{image_to_base64(file['path'])}"
                    }
                )
            elif file['mime_type'].startswith('video'):
                user_input.append(
                    {
                        'type':'video_url',
                        'video_url':file['url']
                    }
                )
            else:
                raise ValueError(f"Unsupported file type: {file['mime_type']}")
        return user_input

    if model == "qwen-long":
        user_input = message['text']

    return user_input
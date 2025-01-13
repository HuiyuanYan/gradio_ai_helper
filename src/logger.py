import logging
import os
from logging.handlers import RotatingFileHandler

def get_logger(name, log_file='app.log', log_level=logging.INFO, max_bytes=1024*1024*5, backup_count=5):
    """
    获取一个配置好的 logger。

    :param name: Logger 的名称。
    :param log_file: 日志文件的路径。
    :param log_level: 日志级别，默认为 INFO。
    :param max_bytes: 日志文件的最大大小，超过后会自动轮转，默认为 5MB。
    :param backup_count: 保留的旧日志文件数量，默认为 5。
    :return: 配置好的 logger。
    """
    # 创建 logger
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # 创建日志文件的目录（如果不存在）
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    # 创建文件处理器，并设置级别和格式
    file_handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
    file_handler.setLevel(log_level)

    # 创建控制台处理器，并设置级别和格式
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)

    # 创建 formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # 添加 formatter 到 handlers
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # 添加 handlers 到 logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
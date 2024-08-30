import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime

from config import LOG_LEVEL

def setup_logging(log_level=LOG_LEVEL):
    log_format = '%(asctime)s - [%(funcName)s-->line:%(lineno)d] - %(levelname)s:%(message)s'
    logging.basicConfig(level=log_level, format=log_format)

    # 如果需要将日志输出到文件，可以添加一个 RotatingFileHandler
    log_file_base = os.getenv("LOG_FILE", "DatasCollection")
    current_date = datetime.now().strftime("%Y-%m-%d")
    log_file = f"{log_file_base}_{current_date}.log"
    
    file_handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=3)  # 10MB per file, keep 3 backup files
    file_handler.setLevel(log_level)
    file_handler.setFormatter(logging.Formatter(log_format))

    # 获取根日志记录器并添加文件处理器
    root_logger = logging.getLogger()
    root_logger.addHandler(file_handler)

# 在模块加载时自动配置日志
setup_logging()

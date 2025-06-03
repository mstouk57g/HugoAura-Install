import sys
from loguru import logger


def setup_logger():
    logger.remove()

    logger.add(
        sys.stderr,
        level="DEBUG",
        format="[Aura-Inst] {time:HH:mm:ss} | <level>{level: <8}</level> | {message}",
        colorize=True,
        enqueue=True,
    )
    logger.debug("日志初始化完成。")
    return logger


log = setup_logger()

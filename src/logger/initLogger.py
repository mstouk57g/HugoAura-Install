import sys
import os
from loguru import logger
import tempfile


def setup_logger():
    """设置日志系统"""
    logger.remove()

    try:
        if sys.stdout is not None:
            sink = sys.stdout
        elif sys.stderr is not None:
            sink = sys.stderr
        else:
            log_file = os.path.join(os.path.expanduser("~"), "hugoaura_installer.log")
            sink = log_file

        logger.add(
            sink,
            level="DEBUG",
            format="[Aura-Inst] {time:HH:mm:ss} | <level>{level: <8}</level> | {message}",
            colorize=sink == sys.stdout or sink == sys.stderr,
            enqueue=True,
        )

        # 如果是 Windows GUI 应用且没有控制台, 添加文件日志
        if hasattr(sys, "frozen") and sys.platform == "win32":
            # PyInstaller 打包的应用
            log_file = os.path.join(
                os.path.dirname(sys.executable), "AuraInstaller.log"
            )
            logger.add(
                log_file,
                level="INFO",
                format="[Aura-Inst] {time:YYYY-MM-DD HH:mm:ss} | <level>{level: <8}</level> | {message}",
                rotation="10 MB",
                retention="7 days",
                enqueue=True,
            )

        logger.debug("日志初始化完成。")

    except Exception as e:
        print(f"日志初始化失败: {e}")
        # 创建一个最小的 logger 配置
        try:
            temp_log = os.path.join(tempfile.gettempdir(), "hugoaura_error.log")
            logger.add(temp_log, level="ERROR")
        except:
            pass

    return logger

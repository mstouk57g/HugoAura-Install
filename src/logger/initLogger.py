import sys
import os
from loguru import logger


def setup_logger():
    """设置日志系统，兼容PyInstaller打包环境"""
    logger.remove()
    
    # 在PyInstaller环境中，sys.stderr可能为None
    # 我们需要提供一个安全的fallback
    try:
        # 尝试使用sys.stderr
        if sys.stderr is not None:
            sink = sys.stderr
        else:
            # 如果sys.stderr为None，创建一个日志文件
            log_file = os.path.join(os.path.expanduser("~"), "hugoaura_installer.log")
            sink = log_file
        
        logger.add(
            sink,
            level="DEBUG",
            format="[Aura-Inst] {time:HH:mm:ss} | <level>{level: <8}</level> | {message}",
            colorize=sink == sys.stderr,  # 只在输出到stderr时使用颜色
            enqueue=True,
        )
        
        # 如果是Windows GUI应用且没有控制台，添加文件日志
        if hasattr(sys, 'frozen') and sys.platform == 'win32':
            # PyInstaller打包的应用
            log_file = os.path.join(os.path.dirname(sys.executable), "hugoaura_installer.log")
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
        # 如果所有日志配置都失败，至少不要让程序崩溃
        print(f"日志初始化失败: {e}")
        # 创建一个最小的logger配置
        try:
            import tempfile
            temp_log = os.path.join(tempfile.gettempdir(), "hugoaura_error.log")
            logger.add(temp_log, level="ERROR")
        except:
            pass  # 如果连这个都失败，就放弃日志
    
    return logger


log = setup_logger()

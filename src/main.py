import sys
import os
import time

from logger.initLogger import log
from utils import uac
import installer
from config import config


def main():
    log.info(f"--- 启动 {config.APP_NAME} 一键安装脚本 ---")
    log.info(f"安装脚本版本: 0.0.1-alpha")
    log.info(f"EXEC: {sys.executable}")
    log.info(f"Arg: {sys.argv}")

    if not uac.is_admin():
        log.warning("安装脚本需要管理员权限, 准备提权...")
        if uac.run_as_admin():
            log.error("提权失败, 请尝试手动使用管理员权限运行, 按回车键退出...")
            input()
            sys.exit(1)

    else:
        log.info("安装脚本正以管理员权限运行, 即将启动安装流程...")
        success = False
        try:
            success = installer.run_installation()
        except Exception as e:
            log.exception(f"执行安装流程时发生意外错误: {e}")
            success = False
        finally:
            time.sleep(1.0)
            print("\n按回车键退出...")
            input()

            sys.exit(0 if success else 1)


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)

    pkg_dir = os.path.dirname(script_dir)
    if pkg_dir not in sys.path:
        sys.path.insert(0, pkg_dir)

    main()

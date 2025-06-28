"""
安装器模型 - 封装 HugoAura 安装相关的业务逻辑
"""

import os
import threading
from typing import Callable, Optional, Dict, Any
import argparse

from installer import run_installation
from uninstaller import run_uninstallation, get_uninstall_info


class InstallerModel:
    """安装器模型类"""

    def __init__(self):
        self.installer = None
        self.install_progress = 0
        self.install_status = "就绪"
        self.current_step = ""
        self.is_installing = False
        self.is_uninstalling = False
        self.install_thread = None

        # 回调函数
        self.progress_callback: Optional[Callable[[int, str, str | None], None]] = None
        self.status_callback: Optional[Callable[[str], None]] = None
        self.completed_callback: Optional[Callable[[bool, str], None]] = None

        # 安装选项
        self.install_options = {
            "version": "latest",
            "custom_version": "",
            "custom_path": "",
            "install_directory": "",
            "non_interactive": True,
        }

        # 卸载选项
        self.uninstall_options = {
            "keep_user_data": False,
            "force": False,
            "dry_run": False,
        }

    def set_progress_callback(self, callback: Callable[[int, str, str | None], None]):
        """设置进度更新回调"""
        self.progress_callback = callback

    def set_status_callback(self, callback: Callable[[str], None]):
        """设置状态更新回调"""
        self.status_callback = callback

    def set_completed_callback(self, callback: Callable[[bool, str], None]):
        """设置安装完成回调"""
        self.completed_callback = callback

    def update_progress(self, progress: int, step: str, status: str | None = None):
        """更新安装进度"""
        self.install_progress = progress
        self.current_step = step
        if self.progress_callback:
            self.progress_callback(progress, step, status)

    def update_status(self, status: str):
        """更新安装状态"""
        self.install_status = status
        if self.status_callback:
            self.status_callback(status)

    def get_seewo_directories(self) -> list:
        """获取希沃管家安装目录列表"""
        try:
            from utils.dirSearch import find_seewo_resources_dir

            dir_path = find_seewo_resources_dir()
            return [dir_path] if dir_path else []
        except Exception as e:
            return []

    def validate_install_options(self) -> tuple[bool, str]:
        """验证安装选项"""
        if self.install_options["version"] == "custom_version":
            if not self.install_options["custom_version"]:
                return False, "请输入自定义版本号"

        if self.install_options["version"] == "custom_path":
            if not self.install_options["custom_path"]:
                return False, "请选择自定义文件路径"
            if not os.path.exists(self.install_options["custom_path"]):
                return False, "指定的文件路径不存在"

        return True, ""

    def start_install(self):
        """开始安装"""
        if self.is_installing or self.is_uninstalling:
            return False, "任务正在进行中"

        valid, message = self.validate_install_options()
        if not valid:
            return False, message

        self.is_installing = True
        self.install_progress = 0
        self.update_status("正在安装...")

        self.install_thread = threading.Thread(target=self._install_worker)
        self.install_thread.daemon = True
        self.install_thread.start()

        return True, "安装已开始"

    def start_uninstall(self):
        """开始卸载"""
        if self.is_installing or self.is_uninstalling:
            return False, "操作正在进行中"

        self.is_uninstalling = True
        self.install_progress = 0
        self.update_status("正在卸载...")

        self.install_thread = threading.Thread(target=self._uninstall_worker)
        self.install_thread.daemon = True
        self.install_thread.start()

        return True, "卸载已开始"

    def _install_worker(self):
        """安装工作线程"""
        try:
            # 构建命令行参数对象
            args = self._build_install_args()

            # 传递进度回调函数给安装器
            args.progress_callback = self.update_progress
            args.status_callback = self.update_status

            # 开始安装进度更新
            self.update_progress(0, "[0 / 10] 准备安装...", "info")

            # 执行实际安装
            result = run_installation(args, self)

            if result["success"]:
                # self.update_progress(100, "[10 / 10] 安装完成")
                self.update_status("安装完成")
                if self.completed_callback:
                    self.completed_callback(True, "HugoAura 安装成功！")
            else:
                self.update_status("安装失败")
                if self.completed_callback:
                    match str(result["errorInfo"]):
                        case _:
                            error_detail = str(result["errorInfo"])
                    self.completed_callback(
                        False, f"安装过程中发生错误:\n{error_detail}"
                    )

        except Exception as e:
            self.update_status("安装失败")
            if not self.is_installing:
                self.update_progress(0, "[FAILED] 安装取消", "error")
                self.update_status("安装已取消")
            elif self.completed_callback:
                self.completed_callback(False, f"安装失败: {str(e)}")
        finally:
            self.is_installing = False

    def _uninstall_worker(self):
        """卸载工作线程"""
        try:
            # 构建命令行参数对象
            args = self._build_uninstall_args()

            # 传递进度回调函数给卸载器
            args.progress_callback = self.update_progress
            args.status_callback = self.update_status

            # 开始卸载进度更新
            self.update_progress(0, "[0 / 8] 准备卸载...", "info")

            if not self.is_uninstalling:  # 检查是否被取消
                return

            # 执行实际卸载
            result = run_uninstallation(args, self)

            if result["success"]:
                # self.update_progress(100, "[8 / 8] 卸载完成")
                self.update_status("卸载完成")
                if self.completed_callback:
                    self.completed_callback(
                        True, "HugoAura 卸载成功! 希沃管家已恢复原始状态。"
                    )
            else:
                self.update_status("卸载失败")
                if self.completed_callback:
                    match str(result["errorInfo"]):
                        case "OLD_ASAR_ENOENT":
                            error_detail = "找不到备份的 ASAR 包\n请尝试从 e.seewo.com 重新下载希沃管家完整包进行重装"
                        case "UNINSTALLATION_CANCELLED":
                            error_detail = "用户取消了卸载"
                        case _:
                            error_detail = str(result["errorInfo"])
                    self.completed_callback(
                        False, f"卸载过程中发生错误:\n{error_detail}"
                    )

        except Exception as e:
            self.update_status("卸载失败")
            if not self.is_uninstalling:
                self.update_progress(0, "[FAILED] 卸载取消", "error")
                self.update_status("卸载已取消")
            elif self.completed_callback:
                self.completed_callback(False, f"卸载失败: {str(e)}")
        finally:
            self.is_uninstalling = False

    def cancel_install(self):
        """取消安装"""
        if self.is_installing:
            self.is_installing = False  # 设置 Flag
            self.update_status("正在取消安装...")

    def cancel_uninstall(self):
        """取消卸载"""
        if self.is_uninstalling:
            self.is_uninstalling = False  # 设置 Flag
            self.update_status("正在取消卸载...")

    def get_uninstall_info(self) -> Dict[str, Any]:
        """获取卸载信息"""
        return get_uninstall_info()  # Call func in uninstaller.py

    def _build_install_args(self) -> argparse.Namespace:
        """构建安装参数"""
        args = argparse.Namespace()

        # 设置默认值
        args.yes = self.install_options["non_interactive"]
        args.latest = False
        args.pre = False
        args.ci = False
        args.version = None
        args.path = None
        args.dir = None
        args.dry_run = False

        version_type = self.install_options["version"]
        if version_type == "latest":
            args.latest = True
        elif version_type == "pre":
            args.pre = True
        elif version_type == "ci":
            args.ci = True
        elif version_type == "custom_version":
            args.version = self.install_options["custom_version"]
        elif version_type == "custom_path":
            args.path = self.install_options["custom_path"]

        if self.install_options["install_directory"]:
            args.dir = self.install_options["install_directory"]

        return args

    def _build_uninstall_args(self) -> argparse.Namespace:
        """构建卸载参数"""
        args = argparse.Namespace()

        args.keep_user_data = self.uninstall_options["keep_user_data"]
        args.force = self.uninstall_options["force"]
        args.dry_run = self.uninstall_options["dry_run"]

        return args

    def get_install_status(self) -> Dict[str, Any]:
        """获取当前安装状态"""
        return {
            "is_installing": self.is_installing,
            "is_uninstalling": self.is_uninstalling,
            "progress": self.install_progress,
            "status": self.install_status,
            "current_step": self.current_step,
        }

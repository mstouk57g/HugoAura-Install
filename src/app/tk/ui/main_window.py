"""
主窗口 UI
"""

from logging import WARN
from version import __appVer__
import tkinter as tk
from tkinter import filedialog, messagebox
import ttkbootstrap as ttk_bs
from ttkbootstrap.constants import *
from tkinter.font import ITALIC
from typing import Callable, Optional
import ctypes
import os
from pathlib import Path


class MainWindow:
    """主窗口UI类"""

    def __init__(self, theme="flatly"):
        # 创建根窗口
        self.root = ttk_bs.Window(themename=theme)
        self.root.title("HugoAura 安装器")
        self.root.geometry("600x950")  # 增加窗口高度以适应更多选项
        self.root.resizable(False, False)
        self.root.iconbitmap(
            os.path.join(
                Path(os.path.dirname(__file__)).parents[1],
                "public",
                "installer.ico",
            )
        )

        # 居中显示窗口
        self._center_window()

        # 回调函数
        self.install_callback: Optional[Callable] = None
        self.uninstall_callback: Optional[Callable] = None
        self.cancel_callback: Optional[Callable] = None

        # 控件变量
        self.version_var = tk.StringVar(value="release")  # 版本类型：release, prerelease, ci, custom_version, custom_path
        self.specific_version_var = tk.StringVar(value="v0.1.1-beta")  # 具体版本
        self.custom_version_var = tk.StringVar()
        self.custom_path_var = tk.StringVar()
        self.install_directory_var = tk.StringVar()
        self.progress_var = tk.DoubleVar()
        self.status_var = tk.StringVar(value="就绪")
        self.step_var = tk.StringVar()

        # 创建界面
        self._create_widgets()

        # 初始状态
        self.is_installing = False
        self._update_version_inputs()

    def _center_window(self):
        """窗口居中显示"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def _create_widgets(self):
        """创建界面控件"""
        # 主容器
        main_frame = ttk_bs.Frame(self.root, padding=20)
        main_frame.pack(fill=BOTH, expand=True)

        # 标题
        title_label = ttk_bs.Label(
            main_frame,
            text="HugoAura 安装器",
            font=("Microsoft YaHei UI", 20, "bold"),
            bootstyle=PRIMARY,
        )
        title_label.pack(pady=(0, 10))

        # 权限状态显示
        self._create_permission_status(main_frame)

        # 版本选择区域
        self._create_version_section(main_frame)

        # 安装目录选择区域
        self._create_directory_section(main_frame)

        # 进度显示区域
        self._create_progress_section(main_frame)

        # 按钮区域
        self._create_button_section(main_frame)

    def _create_permission_status(self, parent):
        """创建权限状态显示区域"""
        # 检查管理员权限
        is_admin = self._check_admin_privileges()

        status_frame = ttk_bs.Frame(parent)
        status_frame.pack(fill=X, pady=(0, 15))

        # 权限图标和文本
        if is_admin:
            status_text = "✅ 已获得管理员权限"
            status_style = SUCCESS
        else:  # 理论上来说这种场景不会被触发
            status_text = "⚠ 需要管理员权限"
            status_style = WARNING

        status_label = ttk_bs.Label(
            status_frame,
            text=status_text,
            font=("Microsoft YaHei UI", 10),
            bootstyle=status_style,
        )
        status_label.pack()

    def _check_admin_privileges(self):
        """检查是否有管理员权限"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def _create_version_section(self, parent):
        """创建版本选择区域"""
        # 版本选择框架
        version_frame = ttk_bs.LabelFrame(
            parent, text="版本选择", padding=15, bootstyle=INFO
        )
        version_frame.pack(fill=X, pady=(0, 15))

        # 版本类型选择
        type_label = ttk_bs.Label(
            version_frame,
            text="版本类型：",
            font=("Microsoft YaHei UI", 10, "bold"),
            bootstyle=PRIMARY,
        )
        type_label.pack(anchor=W, pady=(0, 5))

        # 版本类型选项
        version_types = [
            ("release", "发行版"),
            ("prerelease", "预发行版"),
            ("ci", "自动构建版"),
            ("custom_version", "自定义版本"),
            ("custom_path", "本地文件"),
        ]

        for value, text in version_types:
            radio = ttk_bs.Radiobutton(
                version_frame,
                text=text,
                variable=self.version_var,
                value=value,
                command=self._update_version_inputs,
                bootstyle=PRIMARY,
            )
            radio.pack(anchor=W, pady=2, padx=(20, 0))

        # 具体版本选择框架
        self.specific_version_frame = ttk_bs.LabelFrame(
            version_frame, text="具体版本", padding=10, bootstyle=SECONDARY
        )
        
        # 发行版选项
        self.release_frame = ttk_bs.Frame(self.specific_version_frame)
        release_versions = [
            ("v0.1.1-beta", "[Rel] v0.1.1-beta"),
            ("v0.1.0-beta", "[Rel] v0.1.0 Beta"),
        ]
        for value, text in release_versions:
            radio = ttk_bs.Radiobutton(
                self.release_frame,
                text=text,
                variable=self.specific_version_var,
                value=value,
                bootstyle=SUCCESS,
            )
            radio.pack(anchor=W, pady=1)

        # 预发行版选项
        self.prerelease_frame = ttk_bs.Frame(self.specific_version_frame)
        prerelease_versions = [
            ("v0.1.1-pre-IV-patch-3", "[Pre] v0.1.1-pre-IV-patch-3"),
            ("v0.1.1-pre-IV", "[Pre] v0.1.1-pre-IV"),
            ("v0.1.1-pre-III", "[Pre] v0.1.1-pre-III"),
            ("v0.1.1-pre-II", "[Pre] v0.1.1-pre-II"),
            ("v0.1.1-pre-I", "[Pre] v0.1.1-pre-I"),
        ]
        for value, text in prerelease_versions:
            radio = ttk_bs.Radiobutton(
                self.prerelease_frame,
                text=text,
                variable=self.specific_version_var,
                value=value,
                bootstyle=WARNING,
            )
            radio.pack(anchor=W, pady=1)

        # 自动构建版选项
        self.ci_frame = ttk_bs.Frame(self.specific_version_frame)
        ci_versions = [
            ("vAutoBuild", "[CI] HugoAura Auto Build Release"),
        ]
        for value, text in ci_versions:
            radio = ttk_bs.Radiobutton(
                self.ci_frame,
                text=text,
                variable=self.specific_version_var,
                value=value,
                bootstyle=INFO,
            )
            radio.pack(anchor=W, pady=1)

        # 自定义版本输入框
        self.custom_version_frame = ttk_bs.Frame(version_frame)
        ttk_bs.Label(self.custom_version_frame, text="版本号:").pack(side=LEFT)
        self.custom_version_entry = ttk_bs.Entry(
            self.custom_version_frame, textvariable=self.custom_version_var, width=20
        )
        self.custom_version_entry.pack(side=LEFT, padx=(10, 0))

        # 自定义文件路径
        self.custom_path_frame = ttk_bs.Frame(version_frame)
        ttk_bs.Label(self.custom_path_frame, text="文件路径:").pack(side=LEFT)
        self.custom_path_entry = ttk_bs.Entry(
            self.custom_path_frame, textvariable=self.custom_path_var, width=30
        )
        self.custom_path_entry.pack(side=LEFT, padx=(10, 5))

        self.browse_file_btn = ttk_bs.Button(
            self.custom_path_frame,
            text="浏览",
            command=self._browse_file,
            bootstyle=OUTLINE,
        )
        self.browse_file_btn.pack(side=LEFT)

    def _create_directory_section(self, parent):
        """创建安装目录选择区域"""
        directory_frame = ttk_bs.LabelFrame(
            parent, text="安装目录 (可选)", padding=15, bootstyle=INFO
        )
        directory_frame.pack(fill=X, pady=(0, 15))

        dir_input_frame = ttk_bs.Frame(directory_frame)
        dir_input_frame.pack(fill=X)

        ttk_bs.Label(dir_input_frame, text="目录路径:").pack(side=LEFT)
        self.directory_entry = ttk_bs.Entry(
            dir_input_frame, textvariable=self.install_directory_var, width=40
        )
        self.directory_entry.pack(side=LEFT, padx=(10, 5))

        self.browse_dir_btn = ttk_bs.Button(
            dir_input_frame,
            text="浏览",
            command=self._browse_directory,
            bootstyle=OUTLINE,
        )
        self.browse_dir_btn.pack(side=LEFT)

        # 提示文本
        hint_label = ttk_bs.Label(
            directory_frame,
            text="留空则自动检测希沃管家安装目录",
            font=("Microsoft YaHei UI", 9),
            bootstyle=(SECONDARY, ITALIC),
        )
        hint_label.pack(anchor=W, pady=(5, 0))

    def _create_progress_section(self, parent):
        """创建进度显示区域"""
        progress_frame = ttk_bs.LabelFrame(
            parent, text="安装进度", padding=15, bootstyle=INFO
        )
        progress_frame.pack(fill=X, pady=(0, 15))

        # 状态标签
        self.status_label = ttk_bs.Label(
            progress_frame,
            textvariable=self.status_var,
            font=("Microsoft YaHei UI", 10, "bold"),
        )
        self.status_label.pack(anchor=W, pady=(0, 5))

        # 进度条
        self.progress_bar = ttk_bs.Progressbar(
            progress_frame,
            variable=self.progress_var,
            length=400,
            mode="determinate",
            bootstyle=INFO,
        )
        self.progress_bar.pack(fill=X, pady=(0, 5))

        # 当前步骤
        self.step_label = ttk_bs.Label(
            progress_frame,
            textvariable=self.step_var,
            font=("Microsoft YaHei UI", 9),
            bootstyle=SECONDARY,
        )
        self.step_label.pack(anchor=W)

    def _create_button_section(self, parent):
        """创建按钮区域"""
        button_frame = ttk_bs.Frame(parent)
        button_frame.pack(fill=X, pady=(10, 0))

        # 安装按钮
        self.install_btn = ttk_bs.Button(
            button_frame,
            text="开始安装",
            command=self._on_install_click,
            bootstyle=(INFO, "outline"),
            width=14,
        )
        self.install_btn.pack(side=LEFT, padx=(0, 10))

        # 卸载按钮
        self.uninstall_btn = ttk_bs.Button(
            button_frame,
            text="开始卸载",
            command=self._on_uninstall_click,
            bootstyle=(WARNING, "outline"),
            width=15,
        )
        self.uninstall_btn.pack(side=LEFT, padx=(0, 10))

        # 取消按钮
        self.cancel_btn = ttk_bs.Button(
            button_frame,
            text="取消",
            command=self._on_cancel_click,
            bootstyle=(DANGER, "outline"),
            width=14,
            state=DISABLED,
        )
        self.cancel_btn.pack(side=LEFT)

        about_btn_frame = ttk_bs.Frame(parent)
        about_btn_frame.pack(fill=X, pady=(10, 0))

        # 关于按钮
        about_btn = ttk_bs.Button(
            about_btn_frame,
            text="关于",
            command=self._show_about,
            bootstyle=(SECONDARY, "link"),
            width=14,
        )
        about_btn.pack(side=BOTTOM)

    def _update_version_inputs(self):
        """更新版本输入控件状态"""
        version_type = self.version_var.get()

        # 隐藏所有具体版本选择框架
        self.specific_version_frame.pack_forget()
        self.release_frame.pack_forget()
        self.prerelease_frame.pack_forget()
        self.ci_frame.pack_forget()
        self.custom_version_frame.pack_forget()
        self.custom_path_frame.pack_forget()

        if version_type == "release":
            # 显示发行版选择
            self.specific_version_frame.pack(fill=X, pady=(10, 0))
            self.release_frame.pack(fill=X)
            # 设置默认选择
            if not self.specific_version_var.get() or self.specific_version_var.get() not in ["v0.1.1-beta", "v0.1.0-beta"]:
                self.specific_version_var.set("v0.1.1-beta")

        elif version_type == "prerelease":
            # 显示预发行版选择
            self.specific_version_frame.pack(fill=X, pady=(10, 0))
            self.prerelease_frame.pack(fill=X)
            # 设置默认选择
            if not self.specific_version_var.get() or self.specific_version_var.get() not in ["v0.1.1-pre-IV-patch-3", "v0.1.1-pre-IV", "v0.1.1-pre-III", "v0.1.1-pre-II", "v0.1.1-pre-I"]:
                self.specific_version_var.set("v0.1.1-pre-IV-patch-3")

        elif version_type == "ci":
            # 显示自动构建版选择
            self.specific_version_frame.pack(fill=X, pady=(10, 0))
            self.ci_frame.pack(fill=X)
            # 设置默认选择
            self.specific_version_var.set("vAutoBuild")

        elif version_type == "custom_version":
            # 显示自定义版本输入
            self.custom_version_entry.config(state=NORMAL)
            self.custom_version_frame.pack(fill=X, pady=(10, 0))

        elif version_type == "custom_path":
            # 显示自定义文件路径选择
            self.custom_path_entry.config(state=NORMAL)
            self.browse_file_btn.config(state=NORMAL)
            self.custom_path_frame.pack(fill=X, pady=(10, 0))

        # 禁用其他输入控件
        if version_type != "custom_version":
            self.custom_version_entry.config(state=DISABLED)
        if version_type != "custom_path":
            self.custom_path_entry.config(state=DISABLED)
            self.browse_file_btn.config(state=DISABLED)

    def _browse_file(self):
        """浏览文件"""
        filename = filedialog.askopenfilename(
            title="选择 HugoAura 文件",
            filetypes=[("ASAR 文件", "*.asar"), ("所有文件", "*.*")],
        )
        if filename:
            self.custom_path_var.set(filename)

    def _browse_directory(self):
        """浏览目录"""
        directory = filedialog.askdirectory(title="选择安装目录")
        if directory:
            self.install_directory_var.set(directory)

    def _on_install_click(self):
        """安装按钮点击事件"""
        if self.install_callback:
            version_type = self.version_var.get()
            
            # 根据版本类型确定最终的版本值
            if version_type in ["release", "prerelease", "ci"]:
                # 使用具体选择的版本
                final_version = self.specific_version_var.get()
            elif version_type == "custom_version":
                # 使用自定义版本号
                final_version = self.custom_version_var.get()
            else:
                # 其他情况使用版本类型
                final_version = version_type
            
            # 收集安装选项
            options = {
                "version": final_version,
                "version_type": version_type,  # 保留版本类型信息
                "custom_version": self.custom_version_var.get(),
                "custom_path": self.custom_path_var.get(),
                "install_directory": self.install_directory_var.get(),
                "non_interactive": True,
            }
            self.install_callback(options)

    def _on_uninstall_click(self):
        """卸载按钮点击事件"""
        # 显示确认对话框
        confirm = messagebox.askyesno(
            "确认卸载",
            "确定要卸载HugoAura吗?\n\n卸载后希沃管家将恢复到原始状态\n此操作不可逆, 请确认",
            icon="warning",
        )

        if confirm and self.uninstall_callback:
            # 收集卸载选项
            uninstall_options = {
                "keep_user_data": False,  # TO DO
                "force": False,
                "dry_run": False,
            }
            self.uninstall_callback(uninstall_options)

    def _on_cancel_click(self):
        """取消按钮点击事件"""
        if self.cancel_callback:
            self.cancel_callback()

    def _show_about(self):
        """显示关于对话框"""
        about_text = f"""HugoAura-Install {__appVer__}

这是一个用于安装和管理 HugoAura 的工具。
HugoAura 是针对希沃设备的增强工具。

主要功能:
• 一键安装 HugoAura
• 智能检测希沃管家
• 自动备份原始文件  
• 一键完全卸载
• 多版本支持
• 备份机制
• 完整的卸载恢复

作者: HugoAura Devs
GUI 基于: ttkbootstrap & tkinter
GitHub 主仓库: HugoAura/Seewo-HugoAura
Install 主仓库: HugoAura/HugoAura-Install"""

        messagebox.showinfo("关于 HugoAura-Install", about_text)

    def set_install_callback(self, callback: Callable):
        """设置安装回调函数"""
        self.install_callback = callback

    def set_cancel_callback(self, callback: Callable):
        """设置取消回调函数"""
        self.cancel_callback = callback

    def set_uninstall_callback(self, callback: Callable):
        """设置卸载回调函数"""
        self.uninstall_callback = callback

    def update_progress(self, progress: int, step: str = "", status: str | None = None):
        """更新进度"""
        self.progress_var.set(progress)
        if step:
            self.step_var.set(step)
        if status:
            match status:
                case "success":
                    self.progress_bar.config(bootstyle=SUCCESS)
                case "info":
                    self.progress_bar.config(bootstyle=INFO)
                case "error":
                    self.progress_bar.config(bootstyle=DANGER)
                case "warn":
                    self.progress_bar.config(bootstyle=WARNING)
                case _:
                    pass
        self.root.update_idletasks()

    def update_status(self, status: str):
        """更新状态"""
        self.status_var.set(status)
        self.root.update_idletasks()

    def set_installing_state(self, installing: bool, operation: str = "安装"):
        """设置安装/卸载状态"""
        self.is_installing = installing
        if installing:
            if operation == "卸载":
                self.install_btn.config(state=DISABLED)
                self.uninstall_btn.config(state=DISABLED, text="卸载中...")
            else:
                self.install_btn.config(state=DISABLED, text="安装中...")
                self.uninstall_btn.config(state=DISABLED)
            self.cancel_btn.config(state=NORMAL)
            # 禁用输入控件
            for widget in [
                self.custom_version_entry,
                self.custom_path_entry,
                self.directory_entry,
                self.browse_file_btn,
                self.browse_dir_btn,
            ]:
                widget.config(state=DISABLED)
        else:
            self.install_btn.config(state=NORMAL, text="开始安装")
            self.uninstall_btn.config(state=NORMAL, text="开始卸载")
            self.cancel_btn.config(state=DISABLED)
            # 恢复输入控件状态
            self._update_version_inputs()
            self.directory_entry.config(state=NORMAL)
            self.browse_dir_btn.config(state=NORMAL)

    def set_install_button_state(self, enabled: bool, text: str = "开始安装"):
        """设置安装按钮状态"""
        if enabled:
            self.install_btn.config(state=NORMAL, text=text)
        else:
            self.install_btn.config(state=DISABLED, text=text)

    def show_message(self, title: str, message: str, msg_type: str = "info"):
        """显示消息对话框"""
        if msg_type == "error":
            messagebox.showerror(title, message)
        elif msg_type == "warning":
            messagebox.showwarning(title, message)
        else:
            messagebox.showinfo(title, message)

    def run(self):
        """运行主窗口"""
        self.root.mainloop()

    def destroy(self):
        """销毁窗口"""
        self.root.destroy()

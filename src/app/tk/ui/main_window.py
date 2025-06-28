#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主窗口UI - 使用ttkbootstrap实现现代化界面
author: vistamin
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import ttkbootstrap as ttk_bs
from ttkbootstrap.constants import *
from tkinter.font import ITALIC
from typing import Callable, Optional, Dict, Any
import ctypes


class MainWindow:
    """主窗口UI类"""
    
    def __init__(self, theme="flatly"):
        # 创建根窗口
        self.root = ttk_bs.Window(themename=theme)
        self.root.title("HugoAura 安装器")
        self.root.geometry("600x750")
        self.root.resizable(False, False)
        
        # 居中显示窗口
        self._center_window()
        
        # 回调函数
        self.install_callback: Optional[Callable] = None
        self.cancel_callback: Optional[Callable] = None
        self.uninstall_callback: Optional[Callable] = None
        
        # 控件变量
        self.version_var = tk.StringVar(value="latest")
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
            cursor="hand2"  # 设置鼠标悬停时的手型光标
        )
        title_label.pack(pady=(0, 10))
        
        # 绑定标题点击事件
        title_label.bind("<Button-1>", lambda e: self._show_about())
        
        # 添加悬停提示
        self._create_tooltip(title_label, "点击查看关于信息")
        
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
            status_text = "✓ 已获得管理员权限"
            status_style = SUCCESS
        else:
            status_text = "⚠ 需要管理员权限"
            status_style = WARNING
        
        status_label = ttk_bs.Label(
            status_frame,
            text=status_text,
            font=("Microsoft YaHei UI", 10),
            bootstyle=status_style
        )
        status_label.pack()
    
    def _check_admin_privileges(self):
        """检查是否有管理员权限"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    
    def _create_tooltip(self, widget, text):
        """为控件创建工具提示"""
        def on_enter(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.configure(bg='#ffffe0')
            
            # 获取鼠标位置
            x = widget.winfo_rootx() + 25
            y = widget.winfo_rooty() + 25
            tooltip.geometry(f"+{x}+{y}")
            
            label = tk.Label(
                tooltip, 
                text=text, 
                background='#ffffe0',
                relief='solid',
                borderwidth=1,
                font=("Microsoft YaHei UI", 9)
            )
            label.pack()
            
            # 保存tooltip引用
            widget.tooltip = tooltip
            
            # 2秒后自动消失
            tooltip.after(2000, tooltip.destroy)
        
        def on_leave(event):
            if hasattr(widget, 'tooltip'):
                try:
                    widget.tooltip.destroy()
                except:
                    pass
        
        widget.bind('<Enter>', on_enter)
        widget.bind('<Leave>', on_leave)
    
    def _create_version_section(self, parent):
        """创建版本选择区域"""
        # 版本选择框架
        version_frame = ttk_bs.LabelFrame(
            parent, 
            text="版本选择", 
            padding=15,
            bootstyle=INFO
        )
        version_frame.pack(fill=X, pady=(0, 15))
        
        # 版本选项
        versions = [
            ("latest", "最新稳定版"),
            ("pre", "最新预发行版"),
            ("ci", "CI 构建版"),
            ("custom_version", "自定义版本"),
            ("custom_path", "本地文件")
        ]
        
        for value, text in versions:
            radio = ttk_bs.Radiobutton(
                version_frame,
                text=text,
                variable=self.version_var,
                value=value,
                command=self._update_version_inputs,
                bootstyle=PRIMARY
            )
            radio.pack(anchor=W, pady=2)
        
        # 自定义版本输入框
        self.custom_version_frame = ttk_bs.Frame(version_frame)
        # 初始状态下不显示
        
        ttk_bs.Label(self.custom_version_frame, text="版本号:").pack(side=LEFT)
        self.custom_version_entry = ttk_bs.Entry(
            self.custom_version_frame,
            textvariable=self.custom_version_var,
            width=20
        )
        self.custom_version_entry.pack(side=LEFT, padx=(10, 0))
        
        # 自定义文件路径
        self.custom_path_frame = ttk_bs.Frame(version_frame)
        # 初始状态下不显示
        
        ttk_bs.Label(self.custom_path_frame, text="文件路径:").pack(side=LEFT)
        self.custom_path_entry = ttk_bs.Entry(
            self.custom_path_frame,
            textvariable=self.custom_path_var,
            width=30
        )
        self.custom_path_entry.pack(side=LEFT, padx=(10, 5))
        
        self.browse_file_btn = ttk_bs.Button(
            self.custom_path_frame,
            text="浏览",
            command=self._browse_file,
            bootstyle=OUTLINE
        )
        self.browse_file_btn.pack(side=LEFT)
    
    def _create_directory_section(self, parent):
        """创建安装目录选择区域"""
        directory_frame = ttk_bs.LabelFrame(
            parent,
            text="安装目录 (可选)",
            padding=15,
            bootstyle=SUCCESS
        )
        directory_frame.pack(fill=X, pady=(0, 15))
        
        dir_input_frame = ttk_bs.Frame(directory_frame)
        dir_input_frame.pack(fill=X)
        
        ttk_bs.Label(dir_input_frame, text="目录路径:").pack(side=LEFT)
        self.directory_entry = ttk_bs.Entry(
            dir_input_frame,
            textvariable=self.install_directory_var,
            width=40
        )
        self.directory_entry.pack(side=LEFT, padx=(10, 5))
        
        self.browse_dir_btn = ttk_bs.Button(
            dir_input_frame,
            text="浏览",
            command=self._browse_directory,
            bootstyle=OUTLINE
        )
        self.browse_dir_btn.pack(side=LEFT)
        
        # 提示文本
        hint_label = ttk_bs.Label(
            directory_frame,
            text="留空则自动检测希沃管家安装目录",
            font=("Microsoft YaHei UI", 9),
            bootstyle=(SECONDARY, ITALIC)
        )
        hint_label.pack(anchor=W, pady=(5, 0))
    
    def _create_progress_section(self, parent):
        """创建进度显示区域"""
        progress_frame = ttk_bs.LabelFrame(
            parent,
            text="安装进度",
            padding=15,
            bootstyle=WARNING
        )
        progress_frame.pack(fill=X, pady=(0, 15))
        
        # 状态标签
        self.status_label = ttk_bs.Label(
            progress_frame,
            textvariable=self.status_var,
            font=("Microsoft YaHei UI", 10, "bold")
        )
        self.status_label.pack(anchor=W, pady=(0, 5))
        
        # 进度条
        self.progress_bar = ttk_bs.Progressbar(
            progress_frame,
            variable=self.progress_var,
            length=400,
            mode='determinate',
            bootstyle=SUCCESS
        )
        self.progress_bar.pack(fill=X, pady=(0, 5))
        
        # 当前步骤
        self.step_label = ttk_bs.Label(
            progress_frame,
            textvariable=self.step_var,
            font=("Microsoft YaHei UI", 9),
            bootstyle=SECONDARY
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
            bootstyle=(SUCCESS, "outline"),
            width=15
        )
        self.install_btn.pack(side=LEFT, padx=(0, 10))
        
        # 卸载按钮
        self.uninstall_btn = ttk_bs.Button(
            button_frame,
            text="卸载HugoAura",
            command=self._on_uninstall_click,
            bootstyle=(WARNING, "outline"),
            width=15
        )
        self.uninstall_btn.pack(side=LEFT, padx=(0, 10))
        
        # 取消按钮
        self.cancel_btn = ttk_bs.Button(
            button_frame,
            text="取消",
            command=self._on_cancel_click,
            bootstyle=(DANGER, "outline"),
            width=15,
            state=DISABLED
        )
        self.cancel_btn.pack(side=LEFT)
    
    def _update_version_inputs(self):
        """更新版本输入控件状态"""
        version = self.version_var.get()
        
        # 自定义版本输入框
        if version == "custom_version":
            self.custom_version_entry.config(state=NORMAL)
            self.custom_version_frame.pack(fill=X, pady=(10, 0))
        else:
            self.custom_version_entry.config(state=DISABLED)
            if version != "custom_path":
                self.custom_version_frame.pack_forget()
        
        # 自定义文件路径
        if version == "custom_path":
            self.custom_path_entry.config(state=NORMAL)
            self.browse_file_btn.config(state=NORMAL)
            self.custom_path_frame.pack(fill=X, pady=(5, 0))
            if version != "custom_version":
                self.custom_version_frame.pack_forget()
        else:
            self.custom_path_entry.config(state=DISABLED)
            self.browse_file_btn.config(state=DISABLED)
            self.custom_path_frame.pack_forget()
    
    def _browse_file(self):
        """浏览文件"""
        filename = filedialog.askopenfilename(
            title="选择 HugoAura 文件",
            filetypes=[
                ("ASAR 文件", "*.asar"),
                ("所有文件", "*.*")
            ]
        )
        if filename:
            self.custom_path_var.set(filename)
    
    def _browse_directory(self):
        """浏览目录"""
        directory = filedialog.askdirectory(
            title="选择安装目录"
        )
        if directory:
            self.install_directory_var.set(directory)
    
    def _on_install_click(self):
        """安装按钮点击事件"""
        if self.install_callback:
            # 收集安装选项
            options = {
                'version': self.version_var.get(),
                'custom_version': self.custom_version_var.get(),
                'custom_path': self.custom_path_var.get(),
                'install_directory': self.install_directory_var.get(),
                'non_interactive': True
            }
            self.install_callback(options)
    
    def _on_cancel_click(self):
        """取消按钮点击事件"""
        if self.cancel_callback:
            self.cancel_callback()
    
    def _on_uninstall_click(self):
        """卸载按钮点击事件"""
        # 显示确认对话框
        confirm = messagebox.askyesno(
            "确认卸载", 
            "确定要卸载HugoAura吗？\n\n卸载后希沃管家将恢复到原始状态。\n此操作不可逆，请确认。",
            icon='warning'
        )
        
        if confirm and self.uninstall_callback:
            # 收集卸载选项
            uninstall_options = {
                'keep_user_data': False,  # 可以后续添加选项让用户选择
                'force': False,
                'dry_run': False
            }
            self.uninstall_callback(uninstall_options)
    
    def _show_about(self):
        """显示关于对话框"""
        about_text = """HugoAura 安装器 v1.0

这是一个用于安装和管理 HugoAura 的现代化工具
HugoAura 是针对希沃设备的增强工具

主要功能:
• 一键安装 HugoAura
• 智能检测希沃管家
• 自动备份原始文件  
• 一键完全卸载
• 多版本支持

安全特性:
• 自动请求管理员权限
• 备份保护机制
• 完整的卸载恢复

提示: 点击标题可再次打开此界面

作者: vistamin
基于: ttkbootstrap & tkinter
GitHub: HugoAura/Seewo-HugoAura"""
        
        messagebox.showinfo("关于 HugoAura 安装器", about_text)
    
    def set_install_callback(self, callback: Callable):
        """设置安装回调函数"""
        self.install_callback = callback
    
    def set_cancel_callback(self, callback: Callable):
        """设置取消回调函数"""
        self.cancel_callback = callback
    
    def set_uninstall_callback(self, callback: Callable):
        """设置卸载回调函数"""
        self.uninstall_callback = callback
    
    def update_progress(self, progress: int, step: str = ""):
        """更新进度"""
        self.progress_var.set(progress)
        if step:
            self.step_var.set(step)
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
            for widget in [self.custom_version_entry, self.custom_path_entry, 
                          self.directory_entry, self.browse_file_btn, self.browse_dir_btn]:
                widget.config(state=DISABLED)
        else:
            self.install_btn.config(state=NORMAL, text="开始安装")
            self.uninstall_btn.config(state=NORMAL, text="卸载HugoAura")
            self.cancel_btn.config(state=DISABLED)
            # 恢复输入控件状态
            self._update_version_inputs()
            self.directory_entry.config(state=NORMAL)
            self.browse_dir_btn.config(state=NORMAL)
    
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
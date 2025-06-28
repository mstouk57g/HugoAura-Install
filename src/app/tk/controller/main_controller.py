#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主控制器 - 实现MVC架构中的控制层
author: vistamin
"""

import sys
import threading
from typing import Dict, Any
from loguru import logger

from app.tk.ui.main_window import MainWindow
from app.tk.models.installer_model import InstallerModel


class MainController:
    """主控制器类"""
    
    def __init__(self, theme="flatly"):
        # 创建模型和视图
        self.model = InstallerModel()
        self.view = MainWindow(theme=theme)
        
        # 绑定事件
        self._bind_events()
        
        # 设置模型回调
        self._setup_model_callbacks()
        
        logger.info("主控制器初始化完成")
    
    def _bind_events(self):
        """绑定界面事件"""
        # 设置按钮回调
        self.view.set_install_callback(self._on_install)
        self.view.set_cancel_callback(self._on_cancel)
        
        # 设置窗口关闭事件
        self.view.root.protocol("WM_DELETE_WINDOW", self._on_window_close)
        
        logger.debug("界面事件绑定完成")
    
    def _setup_model_callbacks(self):
        """设置模型回调函数"""
        self.model.set_progress_callback(self._on_progress_update)
        self.model.set_status_callback(self._on_status_update)
        self.model.set_completed_callback(self._on_install_completed)
        
        logger.debug("模型回调设置完成")
    
    def _on_install(self, options: Dict[str, Any]):
        """处理安装事件"""
        logger.info(f"开始安装，选项: {options}")
        
        try:
            # 更新模型的安装选项
            self.model.install_options.update(options)
            
            # 验证安装选项
            valid, message = self.model.validate_install_options()
            if not valid:
                self.view.show_message("错误", message, "error")
                return
            
            # 设置UI为安装状态
            self.view.set_installing_state(True)
            
            # 开始安装
            success, message = self.model.start_install()
            if not success:
                self.view.show_message("错误", message, "error")
                self.view.set_installing_state(False)
                return
            
            logger.info("安装已开始")
            
        except Exception as e:
            logger.error(f"安装启动失败: {e}")
            self.view.show_message("错误", f"安装启动失败: {str(e)}", "error")
            self.view.set_installing_state(False)
    
    def _on_cancel(self):
        """处理取消事件"""
        logger.info("用户请求取消安装")
        
        # 显示确认对话框
        import tkinter.messagebox as messagebox
        if messagebox.askyesno("确认", "确定要取消安装吗？"):
            # 取消安装
            self.model.cancel_install()
            self.view.set_installing_state(False)
            logger.info("安装已取消")
    
    def _on_progress_update(self, progress: int, step: str):
        """处理进度更新"""
        # 使用线程安全的方式更新UI
        self.view.root.after(0, lambda: self.view.update_progress(progress, step))
        logger.debug(f"进度更新: {progress}% - {step}")
    
    def _on_status_update(self, status: str):
        """处理状态更新"""
        # 使用线程安全的方式更新UI
        self.view.root.after(0, lambda: self.view.update_status(status))
        logger.debug(f"状态更新: {status}")
    
    def _on_install_completed(self, success: bool, message: str):
        """处理安装完成事件"""
        logger.info(f"安装完成: {'成功' if success else '失败'} - {message}")
        
        # 使用线程安全的方式更新UI
        def update_ui():
            self.view.set_installing_state(False)
            
            if success:
                self.view.show_message("成功", message, "info")
            else:
                self.view.show_message("失败", message, "error")
        
        self.view.root.after(0, update_ui)
    
    def _on_window_close(self):
        """处理窗口关闭事件"""
        logger.info("用户请求关闭窗口")
        
        # 如果正在安装，询问是否确认关闭
        if self.model.is_installing:
            import tkinter.messagebox as messagebox
            if not messagebox.askyesno("确认", "安装正在进行中，确定要退出吗？"):
                return
            
            # 取消安装
            self.model.cancel_install()
        
        # 清理资源
        self._cleanup()
        
        # 关闭窗口
        self.view.destroy()
        
        logger.info("应用程序已退出")
    
    def _cleanup(self):
        """清理资源"""
        try:
            # 等待安装线程结束（最多等待2秒）
            if self.model.install_thread and self.model.install_thread.is_alive():
                self.model.install_thread.join(timeout=2.0)
            
            logger.debug("资源清理完成")
        except Exception as e:
            logger.error(f"资源清理失败: {e}")
    
    def run(self):
        """运行应用程序"""
        logger.info("启动GUI应用程序")
        try:
            self.view.run()
        except KeyboardInterrupt:
            logger.info("用户中断应用程序")
        except Exception as e:
            logger.error(f"应用程序运行出错: {e}")
            raise
        finally:
            self._cleanup()
    
    def get_install_status(self) -> Dict[str, Any]:
        """获取当前安装状态"""
        return self.model.get_install_status()
    
    def set_theme(self, theme: str):
        """设置主题"""
        try:
            # 重新创建视图（ttkbootstrap在运行时切换主题较复杂）
            logger.info(f"切换主题到: {theme}")
            # 这里可以扩展主题切换功能
        except Exception as e:
            logger.error(f"主题切换失败: {e}")


# 便捷函数
def create_app(theme="flatly") -> MainController:
    """创建应用程序实例"""
    return MainController(theme=theme)


def run_app(theme="flatly"):
    """运行应用程序"""
    app = create_app(theme)
    app.run() 
# -*- coding: utf-8 -*-
"""
版本信息文件，用于PyInstaller生成带有版本信息的exe文件
"""

VSVersionInfo(
    ffi=FixedFileInfo(
        # 文件版本信息
        filevers=(1, 0, 0, 0),
        prodvers=(1, 0, 0, 0),
        
        # 文件标志掩码
        mask=0x3f,
        flags=0x0,
        
        # 操作系统类型
        OS=0x40004,  # VOS_NT_WINDOWS32
        
        # 文件类型
        fileType=0x1,  # VFT_APP
        subtype=0x0,   # VFT2_UNKNOWN
        
        # 文件日期（高位和低位）
        date=(0, 0)
    ),
    kids=[
        StringFileInfo(
            [
                StringTable(
                    u'080404B0',  # 简体中文，Unicode
                    [
                        StringStruct(u'CompanyName', u'HugoAura Team'),
                        StringStruct(u'FileDescription', u'HugoAura - 希沃设备增强工具安装程序'),
                        StringStruct(u'FileVersion', u'1.0.0.0'),
                        StringStruct(u'InternalName', u'HugoAura Installer'),
                        StringStruct(u'LegalCopyright', u'Copyright © 2024 HugoAura Team. All rights reserved.'),
                        StringStruct(u'OriginalFilename', u'HugoAuraInstaller.exe'),
                        StringStruct(u'ProductName', u'HugoAura'),
                        StringStruct(u'ProductVersion', u'1.0.0'),
                        StringStruct(u'Comments', u'用于安装和管理 HugoAura 的图形界面工具'),
                    ]
                )
            ]
        ),
        VarFileInfo([VarStruct(u'Translation', [2052, 1200])])  # 简体中文
    ]
) 
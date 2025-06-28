# PyInstaller hook for PIL/Pillow
# 确保所有PIL模块被正确包含

from PyInstaller.utils.hooks import collect_submodules, collect_data_files

# 收集所有PIL子模块
hiddenimports = collect_submodules('PIL')

# 收集PIL的数据文件
datas = collect_data_files('PIL')

# 明确添加关键模块
hiddenimports += [
    'PIL._tkinter_finder',
    'PIL._imaging',
    'PIL.Image',
    'PIL.ImageTk',
    'PIL.ImageDraw',
    'PIL.ImageFont',
    'PIL.ImageFilter',
    'PIL.ImageEnhance',
    'PIL.ImageOps',
    'PIL.ImageFile',
    'PIL.PngImagePlugin',
    'PIL.JpegImagePlugin',
    'PIL.BmpImagePlugin',
    'PIL.GifImagePlugin',
] 
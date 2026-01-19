import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon

# 模拟打包后的环境
print("=== 图标加载测试 ===")

# 测试多个可能的路径
test_paths = [
    "professional_icon.png",
    "icon.ico",
    os.path.join(os.path.dirname(__file__), "professional_icon.png"),
    os.path.join(os.path.dirname(__file__), "icon.ico"),
]

for path in test_paths:
    exists = os.path.exists(path)
    print(f"路径: {path}")
    print(f"文件存在: {exists}")
    if exists:
        icon = QIcon(path)
        print(f"图标有效: {not icon.isNull()}")
        print(f"文件大小: {os.path.getsize(path)} 字节")
    print("-" * 40)

# 检查当前目录文件
print("当前目录文件:")
for f in os.listdir('.'):
    if f.endswith(('.png', '.ico')):
        print(f"  {f}")
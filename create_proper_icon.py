# 创建一个真正的有效ICO文件
import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon, QPixmap, QPainter
from PyQt6.QtCore import Qt
import os

# 需要先创建QApplication才能使用Qt图形功能
app = QApplication(sys.argv)

# 创建一个32x32的图标
pixmap = QPixmap(32, 32)
pixmap.fill(Qt.GlobalColor.transparent)

# 使用QPainter绘制一个简单的文件重命名图标
painter = QPainter(pixmap)
painter.setRenderHint(QPainter.RenderHint.Antialiasing)

# 绘制文档背景
painter.setBrush(Qt.GlobalColor.white)
painter.setPen(Qt.GlobalColor.darkGray)
painter.drawRoundedRect(2, 2, 28, 28, 4, 4)

# 绘制笔图标（表示重命名）
painter.setPen(Qt.GlobalColor.blue)
painter.drawLine(8, 20, 24, 8)  # 斜线
painter.drawLine(24, 8, 28, 12)  # 笔尖

painter.end()

# 保存为ICO文件
pixmap.save("proper_icon.ico", "ICO")
print("✅ 创建了有效的ICO图标文件")

# 测试新图标
icon = QIcon("proper_icon.ico")
print(f"新图标有效: {not icon.isNull()}")
print(f"新图标尺寸: {icon.availableSizes()}")
print(f"文件大小: {os.path.getsize('proper_icon.ico')} 字节")
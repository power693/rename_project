from PyQt6.QtWidgets import QApplication
import sys
import os
from gui import FileRenamerApp
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QStyle

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # 尝试使用高质量的专业图标
    try:
        # 获取程序所在目录的绝对路径
        if getattr(sys, 'frozen', False):
            # 打包后的情况
            base_path = sys._MEIPASS
        else:
            # 开发时的情况
            base_path = os.path.dirname(os.path.abspath(__file__))
        
        # 尝试多个可能的图标路径
        icon_paths = [
            os.path.join(base_path, "professional_icon.png"),
            os.path.join(base_path, "icon.ico"),
            "professional_icon.png",
            "icon.ico"
        ]
        
        app_icon = None
        for icon_path in icon_paths:
            if os.path.exists(icon_path):
                app_icon = QIcon(icon_path)
                if not app_icon.isNull():
                    print(f"使用图标: {icon_path}")
                    break
        
        if app_icon is None or app_icon.isNull():
            # 回退到系统标准图标
            app_icon = app.style().standardIcon(QStyle.StandardPixmap.SP_FileIcon)
            print("使用系统标准图标")
            
    except Exception as e:
        print(f"图标加载错误: {e}")
        app_icon = app.style().standardIcon(QStyle.StandardPixmap.SP_FileIcon)
        print("使用备用系统图标")
    
    app.setWindowIcon(app_icon)
    window = FileRenamerApp()
    window.setWindowIcon(app_icon)
    window.show()
    sys.exit(app.exec())
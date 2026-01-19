# 批量文件重命名工具

这是一个用于Windows 10及以上系统的Python GUI应用程序，用于批量重命名文件。

## 项目结构

- `main.py`：程序入口
- `gui.py`：GUI界面代码
- `renamer.py`：重命名逻辑
- `README.md`：说明文档
- `requirements.txt`：依赖列表

## 功能

- 打开文件夹选择文件
- 单选、多选、全选文件
- 取消选择文件
- 根据文件类型选择（下拉选择常见类型或手动输入）
- 拖拽文件到窗口中添加
- 按规则批量修改文件名，支持预设规则并显示解析和例子
- 实时预览重命名结果

## 重命名规则

- prefix_{num}：前缀加数字，如prefix_1.ext
- name_#：名称加数字，如name_1.ext
- {num}_file：数字加后缀，如1_file.ext
- new_{num}：new加数字，如new_1.ext
- 自定义：输入任意规则，支持{num}或#作为占位符

## 安装

1. 确保安装了Python 3.x
2. 运行 `pip install -r requirements.txt` （如果有依赖）

## 使用

运行 `python main.py` 启动应用程序。
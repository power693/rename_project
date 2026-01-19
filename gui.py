from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QListWidget, 
                            QPushButton, QHBoxLayout, QComboBox, QLabel, 
                            QFileDialog, QMessageBox, QAbstractItemView, 
                            QGridLayout, QStyledItemDelegate)
from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtGui import QDropEvent, QDragEnterEvent

class CombinedDropList(QListWidget):
    """支持拖拽的文件列表控件"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        self.setMinimumHeight(400)
        self.setAcceptDrops(True)
        self.setDragEnabled(False)  # 禁用内部拖拽，只接受外部拖入
        
        # 样式设置
        self.setStyleSheet("""
            QListWidget {
                border: 2px dashed #555;
                background-color: #2d2d2d;
                color: #ffffff;
                padding: 10px;
            }
            QListWidget::item { 
                padding: 8px; 
                border-bottom: 1px solid #444; 
            }
            QListWidget::item:selected { 
                background-color: #4a7c59; 
            }
            QListWidget::item:hover {
                background-color: #3d3d3d;
            }
        """)
        
        # 空列表提示
        self.empty_label = QLabel("拖拽文件到此处添加\n或点击此处选择文件")
        self.empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.empty_label.setStyleSheet("""
            color: #888; 
            font-size: 14px; 
            background: transparent;
            border: none;
        """)
        self.empty_label.setParent(self.viewport())
        
        # 重写paintEvent来显示提示文本
        def paintEvent(event):
            super(CombinedDropList, self).paintEvent(event)
            if self.count() == 0:
                center_x = (self.width() - self.empty_label.width()) // 2
                center_y = (self.height() - self.empty_label.height()) // 2
                self.empty_label.move(center_x, center_y)
                self.empty_label.show()
            else:
                self.empty_label.hide()
        
        self.paintEvent = paintEvent
    
    def dragEnterEvent(self, event):
        """拖拽进入事件"""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.setStyleSheet("""
                QListWidget {
                    border: 2px dashed #00f;
                    background-color: #3d3d3d;
                    color: #ffffff;
                    padding: 10px;
                }
            """)
        else:
            event.ignore()
    
    def dragMoveEvent(self, event):
        """拖拽移动事件 - 必须在dropEvent之前正确处理"""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()
    
    def dropEvent(self, event):
        """拖放事件"""
        print(f"CombinedDropList dropEvent called")
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            urls = event.mimeData().urls()
            print(f"Received {len(urls)} URLs")
            
            # 查找主应用程序实例
            parent_app = self.window()
            print(f"Window: {parent_app}")
            if parent_app and hasattr(parent_app, 'files_to_rename'):
                print("Found files_to_rename")
                for url in urls:
                    file_path = url.toLocalFile()
                    print(f"Processing: {file_path}")
                    if os.path.isfile(file_path):
                        parent_app.files_to_rename.append(file_path)
                        print(f"Added: {file_path}")
                
                parent_app.update_list()
                parent_app.update_preview()
            else:
                print("Parent app not found or no files_to_rename")
        
        # 恢复正常样式
        self.setStyleSheet("""
            QListWidget {
                border: 2px dashed #555;
                background-color: #2d2d2d;
                color: #ffffff;
                padding: 10px;
            }
            QListWidget::item { 
                padding: 8px; 
                border-bottom: 1px solid #444; 
            }
            QListWidget::item:selected { 
                background-color: #4a7c59; 
            }
            QListWidget::item:hover {
                background-color: #3d3d3d;
            }
        """)
    
    def dragLeaveEvent(self, event):
        """拖拽离开事件"""
        self.setStyleSheet("""
            QListWidget {
                border: 2px dashed #555;
                background-color: #2d2d2d;
                color: #ffffff;
                padding: 10px;
            }
        """)
    
    def mousePressEvent(self, event):
        """鼠标点击事件 - 列表为空时触发添加文件"""
        if self.count() == 0:
            parent = self.parent()
            while parent and not hasattr(parent, 'add_files'):
                parent = parent.parent()
            if parent:
                parent.add_files()
        else:
            super().mousePressEvent(event)


class EmptyListDelegate(QStyledItemDelegate):
    """用于在空列表时显示提示文本的委托类"""
    def __init__(self, empty_label, parent=None):
        super().__init__(parent)
        self.empty_label = empty_label
        
    def paint(self, painter, option, index):
        if index.model().rowCount() == 0:
            self.empty_label.setGeometry(option.rect)
            self.empty_label.render(painter, option.rect.topLeft())
        else:
            super().paint(painter, option, index)
import os
from renamer import Renamer

class DragDropArea(QLabel):
    def __init__(self, parent=None):
        super().__init__("拖拽文件到此处添加\n或点击此处选择文件", parent)
        self.setAcceptDrops(True)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("border: 2px dashed #aaa; padding: 20px;")
        self.setFixedHeight(80)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def mousePressEvent(self, event):
        # 点击时触发添加文件对话框
        parent_app = self.parent()
        if hasattr(parent_app, 'add_files'):
            parent_app.add_files()
        elif hasattr(parent_app, 'parent') and hasattr(parent_app.parent(), 'add_files'):
            parent_app.parent().add_files()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.setStyleSheet("border: 2px dashed #00f; padding: 20px;")

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        main_app = self.parent()
        # 确保能够正确访问主应用的属性
        while main_app and not hasattr(main_app, 'files_to_rename'):
            main_app = main_app.parent()
        
        if main_app and hasattr(main_app, 'files_to_rename'):
            for url in urls:
                file_path = url.toLocalFile()
                if os.path.isfile(file_path):
                    main_app.files_to_rename.append(file_path)
            main_app.update_list()
            main_app.update_preview()
        
        self.setStyleSheet("border: 2px dashed #aaa; padding: 20px;")
        event.acceptProposedAction()

    def dragLeaveEvent(self, event):
        self.setStyleSheet("border: 2px dashed #aaa; padding: 20px;")

class FileRenamerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.files_to_rename = []
        self.initUI()

    def initUI(self):
        self.setWindowTitle("批量文件重命名工具 V-1.0")
        self.setGeometry(300, 300, 800, 500)

        main_layout = QHBoxLayout()

        # 左边布局
        left_layout = QVBoxLayout()

        # 创建一个大框容器来包含文件选择和功能按钮区域
        file_operation_box = QWidget()
        file_operation_box.setStyleSheet("border: 1px solid #ccc; padding: 10px; border-radius: 5px;")
        file_operation_layout = QVBoxLayout(file_operation_box)
        
        # 使用合并的拖放文件列表控件
        self.file_list = CombinedDropList(self)
        file_operation_layout.addWidget(self.file_list)
        
        # 将功能按钮整合到一个水平工具栏中
        toolbar_layout = QHBoxLayout()
        toolbar_layout.setSpacing(5)
        
        # 文件操作按钮
        self.select_folder_btn = QPushButton("📂 文件夹")
        self.select_folder_btn.clicked.connect(self.select_folder)
        self.select_folder_btn.setToolTip("选择文件夹")
        toolbar_layout.addWidget(self.select_folder_btn)
        
        self.add_files_btn = QPushButton("➕ 文件")
        self.add_files_btn.clicked.connect(self.add_files)
        self.add_files_btn.setToolTip("添加文件")
        toolbar_layout.addWidget(self.add_files_btn)
        
        # 选择操作按钮
        self.select_all_btn = QPushButton("✅ 全选")
        self.select_all_btn.clicked.connect(self.select_all)
        self.select_all_btn.setToolTip("全选文件")
        toolbar_layout.addWidget(self.select_all_btn)
        
        self.deselect_btn = QPushButton("❌ 取消")
        self.deselect_btn.clicked.connect(self.deselect)
        self.deselect_btn.setToolTip("取消选择")
        toolbar_layout.addWidget(self.deselect_btn)
        
        # 列表操作按钮
        self.clear_list_btn = QPushButton("🗑️ 清空")
        self.clear_list_btn.clicked.connect(self.clear_list)
        self.clear_list_btn.setToolTip("清空文件列表")
        toolbar_layout.addWidget(self.clear_list_btn)
        
        # 重命名按钮（突出显示）
        self.rename_btn = QPushButton("🚀 重命名")
        self.rename_btn.clicked.connect(self.rename_files)
        self.rename_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        self.rename_btn.setToolTip("执行重命名操作")
        toolbar_layout.addWidget(self.rename_btn)
        
        # 类型选择组合
        type_container = QWidget()
        type_container_layout = QHBoxLayout(type_container)
        type_container_layout.setContentsMargins(0, 0, 0, 0)
        type_container_layout.setSpacing(5)
        
        type_container_layout.addWidget(QLabel("类型:"))
        self.type_combo = QComboBox()
        self.type_combo.addItems([".txt", ".jpg", ".png", ".pdf", ".docx", ".mp4", ".zip", ".stl", ".stp", ".obj", ".fbx", ".dae", ".3ds"])
        self.type_combo.setMinimumWidth(120)  # 进一步增加最小宽度
        self.type_combo.setMaximumWidth(150)  # 进一步增加最大宽度
        self.type_combo.setToolTip("选择文件类型")
        type_container_layout.addWidget(self.type_combo)
        
        self.select_by_type_btn = QPushButton("筛选")
        self.select_by_type_btn.clicked.connect(self.select_by_type)
        self.select_by_type_btn.setToolTip("按类型筛选文件")
        type_container_layout.addWidget(self.select_by_type_btn)
        
        toolbar_layout.addWidget(type_container)
        toolbar_layout.addStretch()  # 添加弹性空间
        
        file_operation_layout.addLayout(toolbar_layout)
        
        # 将重命名模式设置也整合到文件操作大框中
        mode_layout = QVBoxLayout()
        mode_layout.addWidget(QLabel("🎯 重命名设置"))
        file_operation_layout.addLayout(mode_layout)
        
        # 模式选择单选框
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["自定义名称+递增数字", "添加前缀/后缀"])
        self.mode_combo.currentTextChanged.connect(self.switch_rename_mode)
        mode_layout.addWidget(self.mode_combo)
        
        # 自定义名称+数字布局
        self.custom_name_layout = QHBoxLayout()
        self.custom_name_layout.addWidget(QLabel("自定义名称:"))
        self.name_edit = QComboBox()
        self.name_edit.setEditable(True)
        self.name_edit.addItems(["名称", "文件", "图片", "文档", "项目"])
        self.custom_name_layout.addWidget(self.name_edit)
        
        self.custom_name_layout.addWidget(QLabel("位置:"))
        self.position_combo = QComboBox()
        self.position_combo.addItems(["名称在前", "数字在前"])
        self.custom_name_layout.addWidget(self.position_combo)
        
        mode_layout.addLayout(self.custom_name_layout)
        
        # 前缀/后缀布局
        self.prefix_suffix_layout = QHBoxLayout()
        self.prefix_suffix_layout.addWidget(QLabel("前缀:"))
        self.prefix_edit = QComboBox()
        self.prefix_edit.setEditable(True)
        self.prefix_edit.addItems(["new_", "pre_", "backup_", "v"])
        self.prefix_suffix_layout.addWidget(self.prefix_edit)
        
        self.prefix_suffix_layout.addWidget(QLabel("后缀:"))
        self.suffix_edit = QComboBox()
        self.suffix_edit.setEditable(True)
        self.suffix_edit.addItems(["_new", "_copy", "_v2", "_bak"])
        self.prefix_suffix_layout.addWidget(self.suffix_edit)
        
        mode_layout.addLayout(self.prefix_suffix_layout)
        
        # 初始隐藏前缀后缀布局
        self.prefix_suffix_layout.setEnabled(False)
        for i in range(self.prefix_suffix_layout.count()):
            widget = self.prefix_suffix_layout.itemAt(i).widget()
            if widget:
                widget.hide()
        
        # 规则描述
        self.rule_desc = QLabel("选择重命名模式后开始预览")
        self.rule_desc.setWordWrap(True)
        mode_layout.addWidget(self.rule_desc)
        
        # 连接信号
        self.name_edit.currentTextChanged.connect(self.update_preview)
        self.position_combo.currentTextChanged.connect(self.update_preview)
        self.prefix_edit.currentTextChanged.connect(self.update_preview)
        self.suffix_edit.currentTextChanged.connect(self.update_preview)
        
        # 将文件操作大框添加到左侧布局
        left_layout.addWidget(file_operation_box)
        
        main_layout.addLayout(left_layout, 2)

        # 右边布局
        right_layout = QVBoxLayout()
        right_layout.addWidget(QLabel("重命名预览"))
        self.result_list = QListWidget()
        self.result_list.setMinimumWidth(300)  # 设置为原始宽度的2/3左右
        self.result_list.setMaximumWidth(500)  # 设置最大宽度
        right_layout.addWidget(self.result_list)

        main_layout.addLayout(right_layout, 6)  # 调整右侧布局权重

        self.setLayout(main_layout)
        self.update_rule_desc()

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "选择文件夹")
        if folder:
            files = [os.path.join(folder, f) for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
            self.files_to_rename.extend(files)
            self.update_list()
            self.update_preview()

    def add_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "选择文件")
        self.files_to_rename.extend(files)
        self.update_list()
        self.update_preview()

    def select_all(self):
        self.file_list.selectAll()
        self.update_preview()

    def deselect(self):
        self.file_list.clearSelection()
        self.update_preview()

    def clear_list(self):
        self.files_to_rename = []
        self.update_list()
        self.update_preview()

    def select_by_type(self):
        ext = self.type_combo.currentText().strip()
        if not ext.startswith('.'):
            ext = '.' + ext
        self.file_list.clearSelection()
        for i, file_path in enumerate(self.files_to_rename):
            if os.path.splitext(file_path)[1].lower() == ext.lower():
                self.file_list.item(i).setSelected(True)
        self.update_preview()

    # 拖放功能现在由 CombinedDropList 类内部处理
    # 删除旧的拖放事件处理方法

    def update_list(self):
        self.file_list.clear()
        for file in self.files_to_rename:
            self.file_list.addItem(os.path.basename(file))

    def switch_rename_mode(self, mode):
        if mode == "自定义名称+递增数字":
            # 显示自定义名称布局，隐藏前缀后缀布局
            self.custom_name_layout.setEnabled(True)
            for i in range(self.custom_name_layout.count()):
                self.custom_name_layout.itemAt(i).widget().show()
            
            self.prefix_suffix_layout.setEnabled(False)
            for i in range(self.prefix_suffix_layout.count()):
                self.prefix_suffix_layout.itemAt(i).widget().hide()
            
            self.rule_desc.setText("自定义名称 + 递增数字，可以分别编辑名称和选择位置")
            
        else:  # 添加前缀/后缀
            # 显示前缀后缀布局，隐藏自定义名称布局
            self.prefix_suffix_layout.setEnabled(True)
            for i in range(self.prefix_suffix_layout.count()):
                self.prefix_suffix_layout.itemAt(i).widget().show()
            
            self.custom_name_layout.setEnabled(False)
            for i in range(self.custom_name_layout.count()):
                self.custom_name_layout.itemAt(i).widget().hide()
            
            self.rule_desc.setText("在原文件名基础上添加前缀和/或后缀")
        
        self.update_preview()

    def update_rule_desc(self):
        mode = self.mode_combo.currentText()
        if mode == "自定义名称+递增数字":
            self.rule_desc.setText("自定义名称 + 递增数字，可以分别编辑名称和选择位置")
        else:
            self.rule_desc.setText("在原文件名基础上添加前缀和/或后缀")
        self.update_preview()
    def update_preview(self):
        self.result_list.clear()
        if not self.files_to_rename:
            return
        selected_items = self.file_list.selectedItems()
        if not selected_items:
            return
        
        selected_indices = [self.file_list.row(item) for item in selected_items]
        mode = self.mode_combo.currentText()
        
        for idx, list_idx in enumerate(selected_indices):
            file_path = self.files_to_rename[list_idx]
            
            if mode == "自定义名称+递增数字":
                # 使用Renamer类生成名称
                custom_name = self.name_edit.currentText().strip()
                position = self.position_combo.currentText()
                new_name = Renamer.generate_custom_name_with_number(
                    file_path, custom_name, position, idx+1
                )
            else:
                # 前缀/后缀模式
                prefix = self.prefix_edit.currentText().strip()
                suffix = self.suffix_edit.currentText().strip()
                new_name = Renamer.generate_with_prefix_suffix(
                    file_path, prefix, suffix
                )
            
            self.result_list.addItem(f"{os.path.basename(file_path)} -> {new_name}")

    def rename_files(self):
        if not self.files_to_rename:
            QMessageBox.warning(self, "错误", "请先添加文件")
            return

        selected_items = self.file_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "错误", "请选择要重命名的文件")
            return

        try:
            selected_indices = [self.file_list.row(item) for item in selected_items]
            mode = self.mode_combo.currentText()
            renamed_files = []  # 存储重命名后的文件信息
            unchanged_files = []  # 存储文件名未变化的文件
            has_changes = False  # 标记是否有文件需要重命名
            
            for idx, list_idx in enumerate(selected_indices):
                file_path = self.files_to_rename[list_idx]
                dir_name = os.path.dirname(file_path)
                old_name = os.path.basename(file_path)
                
                if mode == "自定义名称+递增数字":
                    custom_name = self.name_edit.currentText().strip()
                    position = self.position_combo.currentText()
                    new_name = Renamer.generate_custom_name_with_number(
                        file_path, custom_name, position, idx+1
                    )
                else:
                    prefix = self.prefix_edit.currentText().strip()
                    suffix = self.suffix_edit.currentText().strip()
                    new_name = Renamer.generate_with_prefix_suffix(
                        file_path, prefix, suffix
                    )
                
                # 检查文件名是否真的发生了变化
                if new_name == old_name:
                    unchanged_files.append(old_name)
                    continue
                
                # 检查目标文件是否已存在
                new_path = os.path.join(dir_name, new_name)
                if os.path.exists(new_path):
                    # 生成冲突提示信息
                    conflict_info = {
                        'old_name': old_name,
                        'new_name': new_name, 
                        'conflict_path': new_path,
                        'error': '文件已存在'
                    }
                    renamed_files.append(conflict_info)
                    continue
                
                # 执行重命名
                try:
                    os.rename(file_path, new_path)
                    has_changes = True
                    
                    # 记录重命名后的文件信息
                    renamed_files.append({
                        'old_name': old_name,
                        'new_name': new_name,
                        'new_path': new_path
                    })
                except OSError as e:
                    # 记录重命名失败的信息
                    conflict_info = {
                        'old_name': old_name,
                        'new_name': new_name,
                        'error': f"重命名失败: {str(e)}"
                    }
                    renamed_files.append(conflict_info)
            
            # 统计成功、冲突和失败的数量
            success_count = sum(1 for f in renamed_files if 'error' not in f)
            conflict_count = sum(1 for f in renamed_files if f.get('error') == '文件已存在')
            error_count = sum(1 for f in renamed_files if 'error' in f and f.get('error') != '文件已存在')
            
            # 处理没有任何变化（包括重命名和冲突）的情况
            if not has_changes and not renamed_files:
                if unchanged_files:
                    if len(unchanged_files) == 1:
                        QMessageBox.information(self, "提示", f"文件名未发生变化: {unchanged_files[0]}")
                    else:
                        file_list = "\n".join([f"• {f}" for f in unchanged_files[:5]])
                        if len(unchanged_files) > 5:
                            file_list += f"\n• ... 还有 {len(unchanged_files) - 5} 个文件"
                        QMessageBox.information(self, "提示", f"所有选中的文件名均未发生变化:\n{file_list}")
                else:
                    QMessageBox.information(self, "提示", "文件名未发生变化")
                return
            elif not has_changes and conflict_count > 0:
                # 只有冲突没有成功重命名
                if conflict_count == 1:
                    conflict_file = next(f for f in renamed_files if f.get('error') == '文件已存在')
                    QMessageBox.warning(self, "冲突", f"目标文件已存在: {conflict_file['new_name']}")
                else:
                    QMessageBox.warning(self, "冲突", f"{conflict_count} 个文件因目标文件已存在而无法重命名")
                return
            
            # 存储最后重命名的文件夹路径（如果至少有一个成功）
            if success_count > 0:
                success_file = next(f for f in renamed_files if 'error' not in f)
                self.last_rename_dir = os.path.dirname(success_file['new_path'])
            
            # 清空左侧文件列表
            self.files_to_rename = []
            self.update_list()
            
            # 更新右侧预览窗口显示重命名结果
            self.show_rename_results(renamed_files)
            
            # 构建结果消息
            messages = []
            if success_count > 0:
                messages.append(f"成功重命名 {success_count} 个文件")
            if conflict_count > 0:
                messages.append(f"{conflict_count} 个文件因目标文件已存在而跳过")
            if error_count > 0:
                messages.append(f"{error_count} 个文件重命名失败")
            if unchanged_files:
                messages.append(f"{len(unchanged_files)} 个文件名未变化")
            
            result_msg = "，".join(messages)
            
            if conflict_count > 0 or error_count > 0:
                QMessageBox.warning(self, "完成但有部分问题", result_msg)
            else:
                QMessageBox.information(self, "成功", result_msg)
            
        except Exception as e:
            QMessageBox.critical(self, "错误", str(e))

    def show_rename_results(self, renamed_files):
        """在右侧预览窗口显示重命名结果，包括成功和失败的"""
        self.result_list.clear()
        
        success_files = [f for f in renamed_files if 'error' not in f]
        conflict_files = [f for f in renamed_files if f.get('error') == '文件已存在']
        error_files = [f for f in renamed_files if 'error' in f and f.get('error') != '文件已存在']
        
        # 添加快捷打开文件夹提示（如果有成功的）
        if success_files:
            first_file_dir = os.path.dirname(success_files[0]['new_path'])
            self.result_list.addItem("🖱️ 🚀 双击此处快速打开文件夹")
            self.result_list.addItem(f"📂 位置: {first_file_dir}")
            self.result_list.addItem("────────────────────")
        
        # 显示成功重命名的文件
        if success_files:
            self.result_list.addItem("=== 成功重命名 ===")
            for file_info in success_files:
                self.result_list.addItem(f"✅ {file_info['old_name']} → {file_info['new_name']}")
            self.result_list.addItem("")
        
        # 显示冲突的文件
        if conflict_files:
            self.result_list.addItem("=== 冲突跳过 ===")
            for file_info in conflict_files[:5]:  # 最多显示5个冲突
                self.result_list.addItem(f"⚠️ {file_info['old_name']} → {file_info['new_name']} (文件已存在)")
            if len(conflict_files) > 5:
                self.result_list.addItem(f"⚠️ ... 还有 {len(conflict_files) - 5} 个冲突文件")
            self.result_list.addItem("")
        
        # 显示错误文件
        if error_files:
            self.result_list.addItem("=== 重命名失败 ===")
            for file_info in error_files[:3]:  # 最多显示3个错误
                self.result_list.addItem(f"❌ {file_info['old_name']} → {file_info['error']}")
            if len(error_files) > 3:
                self.result_list.addItem(f"❌ ... 还有 {len(error_files) - 3} 个失败文件")
            self.result_list.addItem("")
        
        # 连接双击事件（只在有成功重命名时才启用）
        if success_files:
            self.result_list.itemDoubleClicked.connect(self.open_result_folder)

    def open_result_folder(self, item):
        """打开重命名结果所在的文件夹"""
        text = item.text()
        # 双击第一行快捷提示或路径行都可以打开文件夹
        if hasattr(self, 'last_rename_dir') and os.path.isdir(self.last_rename_dir):
            os.startfile(self.last_rename_dir)
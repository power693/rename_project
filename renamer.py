import os
import re

class Renamer:
    """文件名重命名器 - 处理所有命名逻辑"""
    
    @staticmethod
    def generate_custom_name_with_number(original_path, custom_name, position, num):
        """生成自定义名称+数字的文件名"""
        base, ext = os.path.splitext(os.path.basename(original_path))
        
        if position == "名称在前":
            return f"{custom_name}_{num}{ext}"
        else:
            return f"{num}_{custom_name}{ext}"
    
    @staticmethod
    def generate_with_prefix_suffix(original_path, prefix, suffix):
        """生成带前缀/后缀的文件名"""
        base, ext = os.path.splitext(os.path.basename(original_path))
        new_base = base
        
        if prefix:
            new_base = f"{prefix}{new_base}"
        if suffix:
            new_base = f"{new_base}{suffix}"
            
        return new_base + ext
    
    @staticmethod
    def generate_new_name(original_path, rule, num=1):
        """
        兼容旧版本的函数 - 保持向后兼容
        """
        base, ext = os.path.splitext(os.path.basename(original_path))
        
        if rule == "名称+数字":
            return f"{base}_{num}{ext}"
        elif rule == "数字+名称":
            return f"{num}_{base}{ext}"
        
        # 处理带前缀后缀的规则
        new_base = base
        prefix_match = re.search(r'\{prefix:([^}]+)\}', rule)
        suffix_match = re.search(r'\{suffix:([^}]+)\}', rule)
        
        if prefix_match:
            prefix = prefix_match.group(1)
            new_base = f"{prefix}{new_base}"
        
        if suffix_match:
            suffix = suffix_match.group(1)
            new_base = f"{new_base}{suffix}"
        
        return new_base + ext
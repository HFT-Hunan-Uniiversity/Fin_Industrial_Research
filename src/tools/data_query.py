"""
数据查询工具模块
"""

import os
import pandas as pd
from typing import Dict, Any, Optional, Union
import logging

logger = logging.getLogger(__name__)


class DataQuery:
    """数据查询工具类"""
    
    def __init__(self, data_dir: Union[str, Any] = "data"):
        """
        初始化数据查询工具
        
        Args:
            data_dir: 数据目录路径或数据加载器实例
        """
        # 检查是否是数据加载器实例
        if hasattr(data_dir, 'data_root_path') and hasattr(data_dir, 'load_data'):
            # 这是一个MappedDataLoader实例
            self.data_loader = data_dir
            self.data_dir = data_dir.data_root_path
        else:
            # 这是一个路径字符串，创建MappedDataLoader实例
            from .mapped_data_loader import MappedDataLoader
            self.data_loader = MappedDataLoader(data_root_path=data_dir)
            self.data_dir = self.data_loader.data_root_path
    
    def get_data_summary(self, file_name: str) -> Dict[str, Any]:
        """
        获取数据文件摘要
        
        Args:
            file_name: 数据文件名
            
        Returns:
            数据摘要字典
        """
        try:
            # 使用MappedDataLoader加载数据
            df = self.data_loader.load_data(file_name)
            
            # 生成摘要
            summary = f"""
            文件名: {file_name}
            数据行数: {len(df)}
            数据列数: {len(df.columns)}
            列名: {', '.join(df.columns.tolist())}
            
            数据预览:
            {df.head().to_string()}
            
            数据统计信息:
            {df.describe().to_string()}
            """
            
            return {
                "status": "success",
                "file_name": file_name,
                "data_shape": df.shape,
                "columns": df.columns.tolist(),
                "summary": summary,
                "data": df
            }
            
        except Exception as e:
            logger.error(f"读取数据文件 {file_name} 失败: {str(e)}")
            return {
                "status": "error",
                "error": f"读取数据文件失败: {str(e)}",
                "summary": ""
            }
    
    def list_available_files(self) -> list:
        """
        列出可用的数据文件
        
        Returns:
            可用数据文件列表
        """
        try:
            # 使用MappedDataLoader的list_available_files方法
            available_files = self.data_loader.list_available_files()
            return available_files.get("actual_files", [])
        except Exception as e:
            logger.error(f"列出数据文件失败: {str(e)}")
            return []
    
    def get_file_path(self, file_name: str) -> str:
        """
        获取数据文件的完整路径
        
        Args:
            file_name: 数据文件名
            
        Returns:
            数据文件的完整路径
        """
        # 使用MappedDataLoader的get_file_path方法
        return self.data_loader.get_file_path(file_name)
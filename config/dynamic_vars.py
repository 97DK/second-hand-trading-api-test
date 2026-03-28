# config/dynamic_vars.py
"""动态变量管理模块"""

class DynamicVars:
    """动态变量存储类"""
    _vars = {}
    
    @classmethod
    def set_var(cls, key: str, value):
        """设置变量值"""
        cls._vars[key] = value
        
    @classmethod
    def get_var(cls, key: str, default=None):
        """获取变量值"""
        return cls._vars.get(key, default)
        
    @classmethod
    def clear_vars(cls):
        """清空所有变量"""
        cls._vars.clear()
        
    @classmethod
    def get_next_from_list(cls, list_key: str, item_key: str):
        """从列表中获取下一个元素并移除已使用的元素
        Args:
            list_key: 列表变量名 (如 'bought_product_ids')
            item_key: 单个元素变量名 (如 'first_bought_product_id')
        Returns:
            下一个可用的元素值，如果没有则返回None
        """
        # 获取列表
        item_list = cls._vars.get(list_key, [])
        if not item_list:
            return None
            
        # 获取当前使用的元素
        current_item = cls._vars.get(item_key)
        
        # 如果当前元素在列表中，移除它
        if current_item in item_list:
            item_list.remove(current_item)
            cls._vars[list_key] = item_list
            
        # 返回列表中的下一个元素
        if item_list:
            next_item = item_list[0]
            cls._vars[item_key] = next_item
            return next_item
        else:
            # 列表为空，清空单个元素变量
            cls._vars.pop(item_key, None)
            return None
            
    @classmethod
    def mark_as_used(cls, list_key: str, item_value):
        """标记某个元素为已使用
        Args:
            list_key: 列表变量名
            item_value: 要标记为已使用的值
        """
        item_list = cls._vars.get(list_key, [])
        if item_value in item_list:
            item_list.remove(item_value)
            cls._vars[list_key] = item_list
            
    @classmethod
    def get_unused_items(cls, list_key: str):
        """获取未使用的项目列表
        Args:
            list_key: 列表变量名
        Returns:
            未使用的项目列表
        """
        return cls._vars.get(list_key, []).copy()
            
    @classmethod
    def rotate_list_elements(cls, list_key: str, item_key: str):
        """循环轮换列表元素（将已使用的元素移到列表末尾）
        Args:
            list_key: 列表变量名
            item_key: 单个元素变量名
        """
        item_list = cls._vars.get(list_key, [])
        if len(item_list) <= 1:
            return
            
        current_item = cls._vars.get(item_key)
        if current_item in item_list:
            # 移除当前元素并添加到列表末尾
            item_list.remove(current_item)
            item_list.append(current_item)
            cls._vars[list_key] = item_list
            # 更新当前元素为新的第一个元素
            cls._vars[item_key] = item_list[0]

# 全局变量实例
dynamic_vars = DynamicVars()
# common/user_helper.py
"""用户操作辅助工具"""

from config.dynamic_vars import dynamic_vars
from core.send_request import SendRequest
from common.logger import Logger

class UserHelper:
    """用户操作辅助类"""
    
    def __init__(self):
        self.request = SendRequest()
        self.logger = Logger().get_logger()
    
    def get_pending_users(self) -> list:
        """
        获取待审核用户列表
        :return: 待审核用户列表
        """
        try:
            response = self.request.send({
                'method': 'GET',
                'path': '/users/admin/users/',
                'params': {'type': 'pending'},
                'auth_required': True,
                'auth_type': 'admin'
            })
            
            if response.status_code == 200:
                users = response.json()
                self.logger.info(f"获取到 {len(users)} 个待审核用户")
                
                # 将第一个用户ID存储到动态变量中
                if users:
                    first_user_id = users[0]['id']
                    dynamic_vars.set_var('pending_user_id', first_user_id)
                    self.logger.info(f"设置待审核用户ID变量: {first_user_id}")
                
                return users
            else:
                self.logger.error(f"获取待审核用户失败: {response.status_code}")
                return []
                
        except Exception as e:
            self.logger.error(f"获取待审核用户异常: {str(e)}")
            return []
    
    def get_first_pending_user_id(self) -> int:
        """
        获取第一个待审核用户的ID
        :return: 用户ID
        """
        # 先尝试从动态变量获取
        user_id = dynamic_vars.get_var('pending_user_id')
        if user_id:
            return user_id
            
        # 如果没有，则重新获取
        users = self.get_pending_users()
        if users:
            return users[0]['id']
        return None

# 全局实例
user_helper = UserHelper()
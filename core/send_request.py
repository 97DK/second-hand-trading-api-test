# core/send_request.py
import requests
import time
from typing import Dict, Any, Optional
from urllib.parse import urljoin
from pathlib import Path
from common.logger import Logger
from config.settings import Config


class SendRequest:
    """
    发送HTTP请求核心类
    负责：管理会话、处理Headers、维护Cookie、处理CSRF Token
    """

    _instance = None
    _session = None
    _logger = Logger().get_logger()
    _csrf_token = None
    _current_user = None
    _default_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive'
    }

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_session()
        return cls._instance

    def _process_file_references(self, files_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理文件引用，将 @filename 格式转换为实际文件对象
        :param files_dict: 包含文件引用的字典
        :return: 处理后的文件字典
        """
        if not files_dict:
            return {}
            
        processed_files = {}
        base_dir = Path(__file__).parent.parent  # apiautotest目录
        
        for field_name, file_ref in files_dict.items():
            if isinstance(file_ref, str) and file_ref.startswith('@'):
                # 处理 @filename 格式
                filename = file_ref[1:]  # 去掉@符号
                file_path = base_dir / filename
                
                if file_path.exists():
                    # 打开文件用于上传
                    processed_files[field_name] = open(file_path, 'rb')
                    self._logger.info(f"处理文件引用: {field_name} -> {file_path}")
                else:
                    self._logger.error(f"文件不存在: {file_path}")
                    # 如果文件不存在，仍然保留原始引用（可能会导致错误）
                    processed_files[field_name] = file_ref
            else:
                # 直接使用原始值
                processed_files[field_name] = file_ref
                
        return processed_files

    def _process_file_references(self, files_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理文件引用，将 @filename 格式转换为实际文件对象
        :param files_dict: 包含文件引用的字典
        :return: 处理后的文件字典
        """
        if not files_dict:
            return {}
            
        processed_files = {}
        base_dir = Path(__file__).parent.parent  # apiautotest目录
        
        for field_name, file_ref in files_dict.items():
            if isinstance(file_ref, str) and file_ref.startswith('@'):
                # 处理 @filename 格式
                filename = file_ref[1:]  # 去掉@符号
                file_path = base_dir / filename
                
                if file_path.exists():
                    # 打开文件用于上传
                    processed_files[field_name] = open(file_path, 'rb')
                    self._logger.info(f"处理文件引用: {field_name} -> {file_path}")
                else:
                    self._logger.error(f"文件不存在: {file_path}")
                    # 如果文件不存在，仍然保留原始引用（可能会导致错误）
                    processed_files[field_name] = file_ref
            else:
                # 直接使用原始值
                processed_files[field_name] = file_ref
                
        return processed_files
    
    def _build_request(self, case_data: Dict[str, Any]) -> tuple:
        """
        构建请求参数
        :param case_data: 用例数据
        :return: method, url, kwargs
        """
        config = Config()
        
        # 构建完整URL
        path = case_data.get('path', '')
        url = urljoin(config.base_url, path.lstrip('/'))
        
        # 构建请求参数
        request_kwargs = {}
        
        # 文件上传 - 优先处理
        files = case_data.get('files', {})
        if files:
            # 处理文件引用
            processed_files = self._process_file_references(files)
            if processed_files:
                # multipart/form-data 请求
                request_kwargs['files'] = processed_files
                # 数据部分
                data = case_data.get('data', {})
                if data:
                    request_kwargs['data'] = data
        else:
            # 普通请求
            data = case_data.get('data', {})
            if data:
                content_type = case_data.get('content_type', 'application/json')
                if 'json' in content_type.lower():
                    request_kwargs['json'] = data
                else:
                    request_kwargs['data'] = data
        
        # 查询参数
        params = case_data.get('query_params', {})
        if params:
            request_kwargs['params'] = params
        
        # 超时设置
        request_kwargs['timeout'] = config.timeout
        
        method = case_data.get('method', 'GET').upper()
        
        return method, url, request_kwargs

    def _log_request(self, method: str, url: str, headers: Dict, kwargs: Dict):
        """记录请求信息"""
        self._logger.info(f"发送请求: {method} {url}")
        self._logger.info(f"请求Headers: {headers}")
        if 'X-CSRFToken' in headers:
            self._logger.info(f"CSRF Token in Headers: {headers['X-CSRFToken'][:20]}...")
        
        # 记录认证状态
        self._logger.info(f"当前用户状态: {'已登录' if self._current_user else '未登录'}")
        self._logger.info(f"Session Cookies: {dict(self._session.cookies)}")
        if 'json' in kwargs:
            self._logger.debug(f"Body: {kwargs['json']}")
        if 'data' in kwargs:
            self._logger.debug(f"Data: {kwargs['data']}")
        if 'params' in kwargs:
            self._logger.debug(f"Params: {kwargs['params']}")

    def _log_response(self, response: requests.Response):
        """记录响应信息"""
        self._logger.info(f"响应状态码: {response.status_code}")
        self._logger.info(f"响应Headers: {dict(response.headers)}")
        if response.text:
            # 限制日志长度
            preview = response.text[:1000] + ('...' if len(response.text) > 1000 else '')
            self._logger.info(f"响应体: {preview}")

    def _init_session(self):
        """初始化会话 - 自动管理Cookie"""
        self._session = requests.Session()
        # 设置默认Headers
        self._session.headers.update(self._default_headers)
        self._logger.info("HTTP会话初始化完成，默认Headers已设置")

    def send(self, case_data: Dict[str, Any]) -> requests.Response:
        """
        Send HTTP request - Core method
        Processing flow:
        1. Build basic request
        2. Add Headers
        3. Add authentication info
        4. Add CSRF Token
        5. Send request (automatically carry Cookie)
        6. Handle variable extraction
        """
        # 1. 构建请求
        method, url, request_kwargs = self._build_request(case_data)

        # 2. 添加Headers
        headers = self._build_headers(case_data)
        request_kwargs['headers'] = headers

        # 3. 处理认证
        self._handle_auth(case_data)

        # 4. 记录请求信息
        self._log_request(method, url, headers, request_kwargs)

        # 5. 发送请求（_session自动管理Cookie）
        try:
            response = self._session.request(method, url, **request_kwargs)
            self._log_response(response)
            
            # 6. 处理变量提取
            self._handle_variable_extraction(case_data, response)
            
            return response
        except Exception as e:
            self._logger.error(f"请求异常: {str(e)}")
            raise
    
    def _handle_variable_extraction(self, case_data: Dict[str, Any], response: requests.Response):
        """处理变量提取"""
        extract_config = case_data.get('extract', {})
        if not extract_config:
            return
            
        try:
            resp_json = response.json()
            local_vars = {'resp_json': resp_json, 'response': response}
            
            for var_name, expression in extract_config.items():
                try:
                    # 执行提取表达式
                    extracted_value = eval(expression, {"__builtins__": {}}, local_vars)
                    # 存储到动态变量
                    from config.dynamic_vars import dynamic_vars
                    dynamic_vars.set_var(var_name, extracted_value)
                    self._logger.info(f"提取变量 {var_name} = {extracted_value}")
                except Exception as e:
                    self._logger.error(f"变量提取失败 {var_name}: {str(e)}")
                    
        except Exception as e:
            self._logger.error(f"变量提取处理异常: {str(e)}")

    def _build_headers(self, case_data: Dict[str, Any]) -> Dict[str, str]:
        """
        Build request Headers
        Priority: Default Headers < Case Headers < Session Headers(CSRF Token)
        """
        headers = {}

        # 1. Basic default Headers
        headers.update(self._default_headers)

        # 2. Case-level Headers (allow overriding default values)
        case_headers = case_data.get('headers', {})
        headers.update(case_headers)

        # 3. Session-level Headers (such as CSRF Token, highest priority)
        # Special handling of CSRF Token to ensure it won't be overwritten by case headers
        self._logger.debug(f"检查Session Headers中的CSRF Token: {'X-CSRFToken' in self._session.headers}")
        self._logger.debug(f"检查实例中的CSRF Token: {bool(self._csrf_token)}")
        
        if 'X-CSRFToken' in self._session.headers:
            headers['X-CSRFToken'] = self._session.headers['X-CSRFToken']
            self._logger.debug(f"使用Session中的CSRF Token: {self._session.headers['X-CSRFToken'][:10]}...")
        elif self._csrf_token:
            headers['X-CSRFToken'] = self._csrf_token
            self._logger.debug(f"使用实例中的CSRF Token: {self._csrf_token[:10]}...")
        else:
            self._logger.warning("未找到有效的CSRF Token")

        # 4. Set according to Content-Type
        # 注意：对于 multipart/form-data 请求，不手动设置 Content-Type，
        # 让 requests 库自动生成包含 boundary 的完整 Content-Type
        content_type = case_data.get('content_type', 'application/json')
        files = case_data.get('files', {})
        
        # 只有在不是文件上传且没有设置 Content-Type 时才设置
        if not files and content_type and 'Content-Type' not in headers:
            headers['Content-Type'] = content_type

        self._logger.debug(f"最终构建的Headers: {headers}")
        return headers

    def _handle_auth(self, case_data: Dict[str, Any]):
        """
        Handle authentication requirements
        Decide whether login is needed based on auth_required and auth_type
        """        
        auth_required = case_data.get('auth_required', True)
        auth_type = case_data.get('auth_type')
        
        # If the test case explicitly does not require authentication, skip completely
        if not auth_required:
            self._logger.debug("Test case does not require authentication, completely skipping auth process")
            # 清除所有认证相关信息
            self.clear_auth()
            # 不获取 CSRF Token
            return
        
        # Check if already logged in AND user type matches auth_type
        if self._current_user:
            current_user_type = self._current_user.get('user_type')
            # Determine expected user type based on auth_type
            if auth_type == 'admin':
                expected_user_type = 'admin'
            elif auth_type == 'evaluation_student':
                expected_user_type = 'student'  # evaluation_student uses student account (num3)
            else:
                expected_user_type = 'student'  # default to student
                
            # Check if current user matches expected type
            if current_user_type == expected_user_type:
                self._logger.debug(f"Already logged in as {current_user_type}, matches required auth_type")
                return
            else:
                self._logger.info(f"Current user type ({current_user_type}) doesn't match required auth_type ({expected_user_type}), need to re-login")
                # Clear current auth and proceed to login with correct user
                self.clear_auth()
        
        # For login interface: always get fresh CSRF token
        # For other interfaces: use existing token if available
        is_login_interface = case_data.get('path') == '/api/users/login/'
                    
        if is_login_interface:
            # 登录接口专用：获取新鲜的 CSRF Token
            # 强制清除之前的认证状态
            self._logger.info("=== 登录测试用例：强制清除认证状态 ===")
            self.clear_auth()
            self.get_fresh_csrf_token_for_login()
        elif not self._csrf_token:
            # 其他接口：如果没 Token 则获取
            self._logger.info("Getting CSRF Token for non-login interface")
            self.get_csrf_token()
        
        # Auto-login based on auth_type
        config = Config()
        if auth_type == 'admin':
            # Requires administrator privileges
            user = config.test_users.get('admin', {})
            self.login(user.get('user_type', 'admin'), user.get('username'), user.get('password'))
        elif auth_type == 'evaluation_student':
            # Use dedicated evaluation student account (num3)
            user = config.test_users.get('evaluation_student', {})
            self.login(user.get('user_type', 'student'), user.get('username'), user.get('password'))
        else:
            # Default to student user
            user = config.test_users.get('student', {})
            self.login(user.get('user_type', 'student'), user.get('username'), user.get('password'))

    def login(self, user_type: str, username: str, password: str) -> bool:
        """
        Login and save session state
        After successful login, Cookie will be automatically saved in _session
        """
        login_data = {
            'method': 'POST',
            'path': '/api/users/login/',
            'data': {
                'user_type': user_type,
                'username': username,
                'password': password
            },
            'auth_required': False  # Login interface does not require authentication
        }

        # Send login request
        response = self.send(login_data)

        if response.status_code == 200:
            self._current_user = response.json().get('user')
            # Cookie has been automatically saved in _session
            self._logger.info(f"Login successful: {username} ({user_type})")
            self._logger.debug(f"Session Cookie: {self._session.cookies.get_dict()}")
            
            # 登录成功后重新获取CSRF Token并更新session headers
            self._logger.info("重新获取登录后的CSRF Token并更新session headers")
            self.get_csrf_token()
            
            return True
        else:
            self._logger.error(f"Login failed: {response.text}")
            return False

    def logout(self):
        """Logout - Clear session"""
        if self._current_user:
            self.send({
                'method': 'POST',
                'path': '/api/users/logout/',
                'auth_required': False
            })
            # Clear current user information
            self._current_user = None
            # Note: Do not clear _session, because sessionid will expire after logout
            self._logger.info("Logged out")

    def clear_auth(self):
        """Clear authentication information - Used for testing scenarios without login state"""
        self._current_user = None
        # Clear authentication-related Cookies in session
        if 'sessionid' in self._session.cookies:
            self._session.cookies.pop('sessionid')
        if 'csrftoken' in self._session.cookies:
            self._session.cookies.pop('csrftoken')
        self._logger.info("Authentication information cleared")

    def get_fresh_csrf_token_for_login(self) -> str:
        """
        专门为登录测试用例获取新鲜的CSRF Token
        清除现有状态并获取新的Token
        """
        self._logger.info("=== 为登录测试用例获取新鲜CSRF Token ===")        
        # 清除现有认证状态
        self.clear_auth()
        
        # 清除现有的CSRF Token
        self._csrf_token = None
        if 'X-CSRFToken' in self._session.headers:
            del self._session.headers['X-CSRFToken']
        
        # 直接获取新的CSRF Token，不经过认证处理
        response = self._session.get(
            urljoin(Config().base_url, '/api/users/csrf-token/'),
            headers=self._default_headers,
            timeout=30
        )
        
        if response.status_code == 200:
            self._csrf_token = response.json().get('csrfToken')
            # Update session Headers
            self._session.headers.update({'X-CSRFToken': self._csrf_token})
            # Store in dynamic variable system for YAML configuration
            from config.dynamic_vars import dynamic_vars
            dynamic_vars.set_var('csrf_token', self._csrf_token)
            self._logger.info(f"Fresh CSRF Token obtained successfully: {self._csrf_token[:10]}...")
        
        return self._csrf_token
    
    def get_csrf_token(self) -> str:
        """Get CSRF Token"""
        # 直接发送请求，不经过认证处理
        response = self._session.get(
            urljoin(Config().base_url, '/api/users/csrf-token/'),
            headers=self._default_headers,
            timeout=30
        )

        if response.status_code == 200:
            self._csrf_token = response.json().get('csrfToken')
            # Update session Headers
            self._session.headers.update({'X-CSRFToken': self._csrf_token})
            # Store in dynamic variable system for YAML configuration
            from config.dynamic_vars import dynamic_vars
            dynamic_vars.set_var('csrf_token', self._csrf_token)
            self._logger.info(f"CSRF Token obtained successfully: {self._csrf_token[:10]}...")

        return self._csrf_token

    def get_session_cookies(self) -> Dict:
        """Get current session Cookies"""
        return self._session.cookies.get_dict()

    def set_cookie(self, name: str, value: str):
        """Manually set Cookie"""
        self._session.cookies.set(name, value)
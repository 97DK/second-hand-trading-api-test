# core/send_request.py
"""
HTTP request sender
Responsible for sending API requests and handling responses
"""

import requests
from typing import Dict, Any, Optional
import json
import logging
from config.settings import Config


class SendRequest:
    """HTTP request sender class"""

    def __init__(self):
        self._session = requests.Session()
        self._logger = logging.getLogger(__name__)
        self._current_user = None
        self._csrf_token = None
        # Default Headers
        self._default_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def send(self, case_data: Dict[str, Any]) -> requests.Response:
        """
        Send HTTP request
        
        Args:
            case_data: Test case data dictionary
            
        Returns:
            requests.Response: Response object
        """
        try:
            # Handle authentication
            self._handle_auth(case_data)
            
            # Build request parameters
            method = case_data.get('method', 'GET')
            path = case_data.get('path', '')
            base_url = Config().base_url
            
            # Build full URL
            if path.startswith('http'):
                url = path
            else:
                url = f"{base_url.rstrip('/')}/{path.lstrip('/')}"
            
            # Build Headers
            headers = self._build_headers(case_data)
            
            # Build request data
            data = case_data.get('data', {})
            query_params = case_data.get('query_params', {})
            
            # Handle different Content-Type data
            content_type = case_data.get('content_type', 'application/json')
            request_data = None
            
            if method.upper() in ['POST', 'PUT', 'PATCH']:
                if content_type == 'application/json':
                    request_data = json.dumps(data, ensure_ascii=False)
                elif content_type == 'application/x-www-form-urlencoded':
                    request_data = data
                else:
                    request_data = data
            
            # Send request
            self._logger.info(f"Sending {method} {url}")
            self._logger.debug(f"Headers: {headers}")
            self._logger.debug(f"Data: {data}")
            
            response = self._session.request(
                method=method,
                url=url,
                headers=headers,
                params=query_params,
                data=request_data,
                timeout=30
            )
            
            # Log response
            self._logger.info(f"Response Status: {response.status_code}")
            if response.status_code >= 400:
                self._logger.error(f"Response Body: {response.text}")
            
            return response
            
        except Exception as e:
            self._logger.error(f"Request failed: {str(e)}")
            raise

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
        if 'X-CSRFToken' in self._session.headers:
            headers['X-CSRFToken'] = self._session.headers['X-CSRFToken']
        elif self._csrf_token:
            headers['X-CSRFToken'] = self._csrf_token

        # 4. Set according to Content-Type
        content_type = case_data.get('content_type', 'application/json')
        if content_type and 'Content-Type' not in headers:
            headers['Content-Type'] = content_type

        return headers

    def _handle_auth(self, case_data: Dict[str, Any]):
        """
        Handle authentication requirements
        Decide whether login is needed based on auth_required and auth_type
        """
        auth_required = case_data.get('auth_required', True)
        auth_type = case_data.get('auth_type')

        # If the test case explicitly does not require authentication, skip
        if not auth_required:
            self._logger.debug("Test case does not require authentication, skipping login check")
            return

        # Check if already logged in
        if self._current_user:
            self._logger.debug(f"Already logged in, current user: {self._current_user.get('username')}")
            return

        # Automatically get CSRF token before login
        if not self._csrf_token:
            self._logger.info("Automatically getting CSRF Token before login")
            self.get_csrf_token()

        # Auto-login based on auth_type
        config = Config()
        if auth_type == 'admin':
            # Requires administrator privileges
            user = config.test_users.get('admin', {})
            self.login(user.get('user_type', 'admin'), user.get('username'), user.get('password'))
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

    def get_csrf_token(self) -> str:
        """Get CSRF Token"""
        response = self.send({
            'method': 'GET',
            'path': '/api/users/csrf-token/',
            'auth_required': False
        })

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
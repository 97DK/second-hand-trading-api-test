# testcase/test_user/test_user_api.py
"""
用户认证模块测试
对应YAML: data/user/*.yaml
"""

import pytest
import allure
from testcase.base_test import BaseTest
from core.data_driver import DataDriver
from config.settings import Config
from config.test_data_generator import test_data_generator


@allure.epic("二手交易平台")
@allure.feature("用户认证模块")
class TestUserAPI(BaseTest):
    """用户认证测试类"""

    driver = DataDriver()

    # ==================== 登录接口测试 ====================

    @allure.story("登录接口")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.description("测试用户登录接口的各种场景")
    @pytest.mark.smoke
    @pytest.mark.p0
    @driver.parametrize("user", "login.yaml")
    def test_login(self, case_data):
        """
        测试登录接口
        测试场景：
        - TC-AUTH-001: 学生用户成功登录
        - TC-AUTH-002: 管理员成功登录
        - TC-AUTH-003: 未审核学生登录
        - TC-AUTH-004~012: 各种异常场景
        """
        # 对于登录接口测试，强制清除之前的认证状态
        # 确保每个测试用例都在干净的状态下执行
        self.request.clear_auth()
        
        response = self.execute(case_data)

        # 登录成功后的额外验证
        if response.status_code == 200:
            user_data = response.json().get('user', {})

            # 验证登录状态（Cookie）
            cookies = self.request.get_session_cookies()
            assert 'sessionid' in cookies, "登录后应生成sessionid"
            self.logger.info(f"登录成功，sessionid: {cookies.get('sessionid')[:10]}...")

            # 验证用户信息
            assert user_data.get('id') is not None, "返回数据应包含用户ID"
            assert user_data.get('username') is not None, "返回数据应包含用户名"

            # 根据用例类型记录登录状态
            case_id = case_data.get('id')
            if case_id == 'TC-AUTH-001':
                self.request._current_user = user_data
                self.logger.info(f"学生用户登录: {user_data.get('username')}")
            elif case_id == 'TC-AUTH-002':
                self.request._current_user = user_data
                self.logger.info(f"管理员登录: {user_data.get('username')}")

    # ==================== 注册接口测试 ====================

    @allure.story("注册接口")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("测试用户注册接口的各种场景")
    @pytest.mark.smoke
    @pytest.mark.p0
    @driver.parametrize("user", "register.yaml")
    def test_register(self, case_data, clean_test_data):
        """
        测试注册接口
        测试场景：
        - TC-AUTH-011: 注册成功
        - TC-AUTH-012~023: 各种异常场景
        """
        # 为需要唯一学号和用户名的测试用例生成动态数据
        data = case_data.get('data', {})
        case_id = case_data.get('id')
        
        # 特殊处理：某些测试用例需要部分固定、部分动态的数据
        if case_id == 'TC-AUTH-018':
            # 学号重复测试：使用固定学号，动态用户名
            next_username = test_data_generator.get_next_username()
            case_data['data']['username'] = next_username
            self.logger.info(f"TC-AUTH-018 使用固定学号 + 动态用户名：{next_username}")
        elif case_id == 'TC-AUTH-019':
            # 用户名重复测试：使用固定用户名，动态学号
            next_student_id = test_data_generator.get_next_student_id()
            case_data['data']['student_id'] = next_student_id
            self.logger.info(f"TC-AUTH-019 使用固定用户名 + 动态学号：{next_student_id}")
        elif case_id == 'TC-AUTH-023':
            # 学号长度测试：使用固定长学号，动态用户名
            next_username = test_data_generator.get_next_username()
            case_data['data']['username'] = next_username
            self.logger.info(f"TC-AUTH-023 使用固定长学号 + 动态用户名：{next_username}")
        # 其他测试用例：如果学号和用户名都不是空字符串，则都使用动态生成
        elif data.get('student_id') and data.get('username'):
            # 获取下一个可用的学号和用户名
            next_student_id = test_data_generator.get_next_student_id()
            next_username = test_data_generator.get_next_username()
            
            # 更新测试数据
            case_data['data']['student_id'] = next_student_id
            case_data['data']['username'] = next_username
            
            self.logger.info(f"使用动态生成的数据 - 学号：{next_student_id}, 用户名：{next_username}")
        
        response = self.execute(case_data)

        # 注册成功后的额外验证
        if response.status_code == 201:
            # 从测试数据中提取注册信息
            data = case_data.get('data', {})
            username = data.get('username')
            student_id = data.get('student_id')

            self.logger.info(f"用户注册成功: {username}, 学号: {student_id}")

            # 可以验证数据库（如果有DB工具）
            # user = self.db_utils.fetch_one(
            #     "SELECT * FROM users WHERE username = %s", (username,)
            # )
            # assert user is not None
            # assert user['is_verified'] == 0  # 待审核状态

    # ==================== 登出接口测试 ====================

    @allure.story("登出接口")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("测试用户登出接口的各种场景")
    @pytest.mark.regression
    @pytest.mark.p1
    @driver.parametrize("user", "logout.yaml")
    def test_logout(self, case_data):
        """
        测试登出接口
        测试场景：
        - TC-AUTH-022: 已登录用户登出 (保持认证状态)
        - TC-AUTH-023: 未登录用户登出 (清除认证状态)
        """
        case_id = case_data.get('id')
        
        # TC-AUTH-022: 已登录用户登出 - 保持认证状态
        if case_id == 'TC-AUTH-022':
            self.logger.info("=== 测试场景：已登录用户登出（保持认证状态）===")
            # 强制重新登录以确保认证状态正确
            self.request.clear_auth()  # 先清除现有状态
            config = Config()
            user = config.test_users.get('student', {})
            login_success = self.request.login(user.get('user_type', 'student'), user.get('username'), user.get('password'))
            if login_success:
                self.logger.info(f"为TC-AUTH-022测试重新执行登录: {user.get('username')}")
                # 验证session状态
                cookies = self.request.get_session_cookies()
                self.logger.info(f"登录后Session Cookies: {cookies}")
                assert 'sessionid' in cookies, "登录后必须有sessionid"
            else:
                self.logger.error("TC-AUTH-022测试登录失败")
                raise Exception("无法为TC-AUTH-022测试建立登录状态")
            
        # TC-AUTH-023: 未登录用户登出 - 清除认证状态
        elif case_id == 'TC-AUTH-023':
            self.logger.info("=== 测试场景：未登录用户登出（清除认证状态）===")
            # 主动清除认证状态，模拟未登录用户
            self.request.clear_auth()
            self.logger.info("已清除认证状态，测试未登录用户登出场景")

        response = self.execute(case_data)

        # 验证响应
        self.logger.info(f"登出接口响应状态码: {response.status_code}")
        self.logger.info(f"登出接口响应内容: {response.text}")
        
        # TC-AUTH-022 特殊验证：检查认证状态是否保持
        if case_id == 'TC-AUTH-022' and response.status_code == 200:
            # 检查是否设置了keep_auth=true
            keep_auth = case_data.get('data', {}).get('keep_auth', False)
            cookies = self.request.get_session_cookies()
            
            if keep_auth:
                # 如果设置了keep_auth=true，session应该保持
                assert 'sessionid' in cookies, "保持认证状态下sessionid应该存在"
                self.logger.info(f"认证状态已保持，sessionid: {cookies.get('sessionid', '')[:10]}...")
            else:
                # 正常登出情况下，session应该被清除
                assert 'sessionid' not in cookies, "登出后sessionid应被清除"
                self.logger.info("认证状态已清除")

    # ==================== 密码重置接口测试 ====================

    @allure.story("密码重置接口")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("测试密码重置申请接口的各种场景")
    @pytest.mark.regression
    @pytest.mark.p1
    @driver.parametrize("user", "password_reset.yaml")
    def test_password_reset(self, case_data):
        """
        测试密码重置申请接口
        测试场景：
        - TC-AUTH-026: 提交成功
        - TC-AUTH-027~030: 各种异常场景
        """
        self.execute(case_data)
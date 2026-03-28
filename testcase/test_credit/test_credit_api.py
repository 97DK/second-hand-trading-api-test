# testcase/test_credit/test_credit_api.py
"""
信用分管理模块测试
对应YAML: data/credit/*.yaml
"""

import pytest
import allure
from testcase.base_test import BaseTest
from core.data_driver import DataDriver


@allure.epic("二手交易平台")
@allure.feature("信用分管理模块")
class TestCreditAPI(BaseTest):
    """信用分管理测试类"""

    driver = DataDriver()

    @allure.story("获取信用分")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("测试获取信用分接口的各种场景")
    @pytest.mark.regression
    @pytest.mark.p1
    @driver.parametrize("credit", "get_score.yaml")
    def test_get_credit_score(self, case_data, login_student):
        """
        测试获取信用分
        测试场景：
        - TC-CREDIT-001: 登录用户获取
        - TC-CREDIT-002: 未登录用户
        """
        # 对于未登录用户的测试
        if case_data.get('id') == 'TC-CREDIT-002':
            # 清除认证信息
            self.request.clear_auth()

        response = self.execute(case_data)

        if response.status_code == 200:
            data = response.json()
            assert 'credit_score' in data
            assert 'message' in data
            score = data.get('credit_score')
            assert 0 <= score <= 100, f"信用分应在0-100之间，实际为{score}"
            self.logger.info(f"当前信用分: {score}, {data.get('message')}")

    @allure.story("更新信用分")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("测试管理员更新信用分接口的各种场景")
    @pytest.mark.regression
    @pytest.mark.p1
    @driver.parametrize("credit", "update_score.yaml")
    def test_update_credit_score(self, case_data, login_admin):
        """
        测试更新信用分
        测试场景：
        - TC-CREDIT-003: 管理员更新成功
        - TC-CREDIT-004~008: 各种异常场景
        """
        # 对于非管理员用户的测试
        if case_data.get('auth_type') == 'student':
            # 清除当前认证信息
            self.request.clear_auth()
            # 重新登录学生用户
            self.request.login('student', 'sssass', '123456')

        self.execute(case_data)

    @allure.story("信用申诉")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("测试提交信用申诉接口的各种场景")
    @pytest.mark.regression
    @pytest.mark.p2
    @driver.parametrize("credit", "appeal.yaml")
    def test_credit_appeal(self, case_data, login_student):
        """
        测试提交信用申诉
        测试场景：
        - TC-CREDIT-009: 提交成功
        - TC-CREDIT-010: 申诉内容为空
        - TC-CREDIT-011: 申诉ID不存在
        """
        self.execute(case_data)
# testcase/test_finance/test_finance_api.py
"""
财务管理模块测试
对应YAML: data/finance/*.yaml
"""

import pytest
import allure
from testcase.base_test import BaseTest
from core.data_driver import DataDriver


@allure.epic("二手交易平台")
@allure.feature("财务管理模块")
class TestFinanceAPI(BaseTest):
    """财务管理测试类"""

    driver = DataDriver()

    @allure.story("用户充值")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("测试用户充值接口的各种场景")
    @pytest.mark.smoke
    @pytest.mark.p1
    @driver.parametrize("finance", "recharge.yaml")
    def test_recharge(self, case_data, login_student):
        """
        测试用户充值
        测试场景：
        - TC-FIN-001: 充值成功
        - TC-FIN-002~006: 各种异常场景
        """
        # 获取充值前的余额
        pre_balance = None
        if case_data.get('id') == 'TC-FIN-001':
            profile = self.request.send({
                'method': 'GET',
                'path': '/api/users/profile/',
                'auth_required': True
            })
            pre_balance = float(profile.json().get('balance', 0))
            self.logger.info(f"充值前余额: {pre_balance}")

        response = self.execute(case_data)

        # 充值成功后的余额验证
        if response.status_code == 200 and case_data.get('id') == 'TC-FIN-001':
            amount = case_data.get('data', {}).get('amount', 0)

            # 获取充值后的余额
            profile = self.request.send({
                'method': 'GET',
                'path': '/api/users/profile/',
                'auth_required': True
            })
            post_balance = float(profile.json().get('balance', 0))

            # 验证余额增加
            assert post_balance - pre_balance == amount, "余额增加金额不正确"
            self.logger.info(f"充值后余额: {post_balance}, 增加: {amount}")

    @allure.story("用户提现")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("测试用户提现接口的各种场景")
    @pytest.mark.regression
    @pytest.mark.p1
    @driver.parametrize("finance", "withdraw.yaml")
    def test_withdraw(self, case_data, login_student):
        """
        测试用户提现
        测试场景：
        - TC-FIN-007: 提现成功
        - TC-FIN-008~010: 各种异常场景
        """
        # 获取提现前的余额
        pre_balance = None
        if case_data.get('id') == 'TC-FIN-007':
            profile = self.request.send({
                'method': 'GET',
                'path': '/api/users/profile/',
                'auth_required': True
            })
            pre_balance = float(profile.json().get('balance', 0))
            self.logger.info(f"提现前余额: {pre_balance}")

        response = self.execute(case_data)

        # 提现成功后的余额验证
        if response.status_code == 200 and case_data.get('id') == 'TC-FIN-007':
            amount = case_data.get('data', {}).get('amount', 0)

            profile = self.request.send({
                'method': 'GET',
                'path': '/api/users/profile/',
                'auth_required': True
            })
            post_balance = float(profile.json().get('balance', 0))

            # 验证余额减少
            assert pre_balance - post_balance == amount, "余额减少金额不正确"
            self.logger.info(f"提现后余额: {post_balance}, 减少: {amount}")
# testcase/test_appeal/test_appeal_api.py
"""
申诉管理模块测试
对应YAML: data/appeal/*.yaml
"""

import pytest
import allure
from testcase.base_test import BaseTest
from core.data_driver import DataDriver


@allure.epic("二手交易平台")
@allure.feature("申诉管理模块")
class TestAppealAPI(BaseTest):
    """申诉管理测试类"""

    driver = DataDriver()

    @allure.story("提交申诉")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("测试提交评价申诉接口的各种场景")
    @pytest.mark.regression
    @pytest.mark.p1
    @driver.parametrize("appeal", "submit.yaml")
    def test_submit_appeal(self, case_data, login_student):
        """
        测试提交申诉
        测试场景：
        - TC-APPEAL-001: 申诉成功
        - TC-APPEAL-002: 申诉内容为空
        - TC-APPEAL-003: 评价不存在
        - TC-APPEAL-004: 非卖家用户
        """
        # 对于非卖家用户的测试
        if case_data.get('auth_type') == 'student':
            # 使用另一个学生用户（非卖家）
            self.api_driver.clear_auth()
            self.api_driver.login('student', 'another_student', '12345678')

        self.execute(case_data)

    @allure.story("获取申诉详情")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("测试获取申诉详情接口")
    @pytest.mark.regression
    @pytest.mark.p2
    @driver.parametrize("appeal", "detail.yaml")
    def test_appeal_detail(self, case_data, login_student):
        """测试获取申诉详情"""
        self.execute(case_data)

    @allure.story("获取负面评价")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("测试获取卖家负面评价列表")
    @pytest.mark.regression
    @pytest.mark.p2
    @driver.parametrize("appeal", "negative.yaml")
    def test_negative_evaluations(self, case_data, login_student):
        """测试获取负面评价"""
        response = self.execute(case_data)

        if response.status_code == 200:
            evaluations = response.json()
            assert isinstance(evaluations, list)
            self.logger.info(f"获取到负面评价，共 {len(evaluations)} 条")
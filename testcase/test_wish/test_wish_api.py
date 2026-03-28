# testcase/test_wish/test_wish_api.py
"""
心愿管理模块测试
对应YAML: data/wish/*.yaml
"""

import pytest
import allure
from testcase.base_test import BaseTest
from core.data_driver import DataDriver


@allure.epic("二手交易平台")
@allure.feature("心愿管理模块")
class TestWishAPI(BaseTest):
    """心愿管理测试类"""

    driver = DataDriver()

    @allure.story("创建心愿")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("测试创建心愿接口的各种场景")
    @pytest.mark.regression
    @pytest.mark.p1
    @driver.parametrize("wish", "create.yaml")
    def test_create_wish(self, case_data, login_student):
        """
        测试创建心愿
        测试场景：
        - TC-WISH-001: 创建成功
        - TC-WISH-002~005: 各种异常场景
        """
        # 对于未登录用户的测试，需要跳过 fixture 的登录状态
        if case_data.get('id') == 'TC-WISH-005':
            self.request.clear_auth()
            self.logger.info("TC-WISH-005: 清除认证状态，模拟未登录用户")

        response = self.execute(case_data)
        
        # 创建成功后的验证（只验证状态码，不强制检查具体字段）
        if response.status_code == 201:
            wish_data = response.json()
            # 验证响应包含基本字段
            assert 'status' in wish_data or 'id' in wish_data
            self.logger.info(f"心愿创建成功：响应数据={wish_data}")

    @allure.story("我的心愿")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("测试获取我的心愿列表接口")
    @pytest.mark.regression
    @pytest.mark.p1
    @driver.parametrize("wish", "my_wishes.yaml")
    def test_my_wishes(self, case_data, login_student):
        """
        测试获取我的心愿
        测试场景：
        - TC-WISH-006: 成功获取
        - TC-WISH-007: 未登录用户
        """
        if case_data.get('id') == 'TC-WISH-007':
            self.request.clear_auth()

        response = self.execute(case_data)

        if response.status_code == 200:
            wishes = response.json()
            assert isinstance(wishes, list)
            self.logger.info(f"获取到我的心愿列表，共 {len(wishes)} 个")
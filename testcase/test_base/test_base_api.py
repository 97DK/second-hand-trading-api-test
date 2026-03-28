# testcase/test_base/test_base_api.py
"""
基础接口测试
对应YAML: data/base/*.yaml
"""

import pytest
import allure
from testcase.base_test import BaseTest
from core.data_driver import DataDriver


@allure.epic("二手交易平台")
@allure.feature("基础接口")
class TestBaseAPI(BaseTest):
    """基础接口测试类"""

    driver = DataDriver()

    @allure.story("获取CSRF Token")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("测试获取CSRF Token接口的各种场景")
    @pytest.mark.smoke
    @pytest.mark.p0
    @driver.parametrize("base", "csrf_token.yaml")
    def test_csrf_token(self, case_data):
        """
        测试获取CSRF Token
        测试场景：
        - TC-BASE-001: 正常获取Token
        """
        response = self.execute(case_data)

        # 额外的业务验证
        if response.status_code == 200:
            token = response.json().get('csrfToken')
            assert token is not None, "CSRF Token不应为None"
            assert len(token) > 0, "CSRF Token长度应大于0"

            # 保存到全局，供后续测试使用
            self.request._csrf_token = token
            self.request._session.headers.update({'X-CSRFToken': token})
            self.logger.info(f"CSRF Token 已保存：{token[:10]}...")

